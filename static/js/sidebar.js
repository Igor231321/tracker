const toggler = document.querySelector('.toggler-btn')
      const closeSidebarBtn = document.querySelector('#closeSidebar')
      const sidebar = document.querySelector('#sidebar')
      const overlay = document.querySelector('#overlay')
      
      // Toggle sidebar for opening and closing
      toggler.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed')
        overlay.classList.toggle('show')
      })
      
      // Close the sidebar on mobile
      closeSidebarBtn.addEventListener('click', function () {
        sidebar.classList.remove('collapsed')
        overlay.classList.remove('show')
      })
      
      // Close sidebar when clicking overlay
      overlay.addEventListener('click', function () {
        sidebar.classList.remove('collapsed')
        overlay.classList.remove('show')
      })