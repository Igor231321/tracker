let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');
let overlay = document.querySelector('.overlay');

btn.onclick = function (event) {
  // Предотвращаем распространение события на другие элементы
  event.stopPropagation();
  sidebar.classList.toggle('active');
  overlay.classList.toggle('active');
};

overlay.onclick = function () {
  if (sidebar.classList.contains('active')) {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
  }
};

// Функция для проверки, является ли устройство мобильным
function isMobile() {
  return window.innerWidth <= 768; // Обычно для мобильных устройств ширина экрана до 768px
}

// Закрытие sidebar при клике вне его (работает только на мобильных устройствах)
document.onclick = function (event) {
  if (isMobile() && sidebar.classList.contains('active') && !sidebar.contains(event.target) && event.target !== btn) {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
  }
};
