var toastElements = document.querySelectorAll('.toast')
var toastList = [...toastElements].map(function (toastEl) {
  return new bootstrap.Toast(toastEl)
})

toastList.forEach(function (toast) {
  toast.show()
})