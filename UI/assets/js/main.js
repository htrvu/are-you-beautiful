const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);

const nonFaceText = 'Rất tiếc, chúng tôi không thể xác định được...'
const errorTexts = ["Có gì đó sai sai trong ảnh... Hy vọng là sai 🤣", "Khoan! Dừng khoảng chừng 2 giây... Bạn chắc chưa? 😥", "Ở đây có trẻ lạc... 🧐", "Hmmmmm? 😳"]
const outputText = 'Tôi sẽ không chịu trách nhiệm về bất kì hậu quả nào... 😅'

Dropzone.autoDiscover = false

function init() {
  let dz = new Dropzone("#dropzone", {
    url: "/",
    maxFiles: 1,
    dictDefaultMessage: "Some Message",
    autoProcessQueue: false,
    thumbnailWidth: 250,
    thumbnailHeight: 250,
  })

  dz.on("addedfile", function () {
    if (dz.files[1] != null) {
      dz.removeFile(dz.files[0])
    }
  })

  dz.on("complete", async function (file) {
    const imgData = file.dataURL

    const api = "http://127.0.0.1:5000/judge_imgs"
    // demo with ngrok
    // const api = "https://b84f-2001-ee0-4bcb-e7c0-183d-8b17-c770-10aa.ngrok.io/judge_imgs"
    
    const response = await fetch(api, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"imgData": imgData})
    });
    
    const data = await response.json();

    query('.drag-field').style.display = 'none'
    query('.result-wrapper').style.display = 'flex'
    query('.output-img').src = data['imgData']

    let text = ''
    if (data['non-face'] == true) {
      text = nonFaceText
    } else if (data['errorCnt'] > 0) {
      text = errorTexts[Math.round(Math.random() * 100) % 4]
    } else {
      text = outputText
    }
    query('.output-text').innerText = text

  })

  query(".submit").addEventListener("click", () => {
    dz.processQueue()
  })

  query(".try-again").addEventListener("click", () => {
    Dropzone.forElement('#dropzone').removeAllFiles(true)
    query('.drag-field').style.display = 'block'
    query('.result-wrapper').style.display = 'none'
  })
}

window.addEventListener('DOMContentLoaded', () => {
  init()
});