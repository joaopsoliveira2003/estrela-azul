document.onreadystatechange = () => {
let toastList = [].slice.call(document.querySelectorAll('.toast')).map((toastEl) => {
  return new bootstrap.Toast(toastEl, {
    animation: true,
    autohide: false,
    delay: 500
  })
})
toastList.forEach(toast => toast.show())
setInterval(toast_counter, 1000)
}

let seg_total = 0
const toast_counter = () => {
text = ""
seg_total++
let seg = seg_total

let horas = Math.trunc(seg/3600)
seg -= (3600 * horas)
let min = Math.trunc(seg/60)

if(horas > 0)
  text += horas + "h"

if(min > 0){
  if(horas > 0)
    text += " "
  text += min + " min"
} else
  text = "agora"
  document.getElementById("toast_timer").innerHTML = text
}