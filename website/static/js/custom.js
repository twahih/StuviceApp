$('#myForm').submit(function() {
    var password = $('#password').val();
    var confirm_password = $('#confirm_password').val();
  
    if (password != confirm_password) {
      alert('Passwords do not match.');
      return false;
    }
  });

// Get all the tab links
var tabLinks = document.querySelectorAll('.list-inline li a');

// Add a click event listener to each link
tabLinks.forEach(function(link) {
  link.addEventListener('click', function() {
    // Get the href of the clicked link
    var href = this.getAttribute('href');

    // Show the corresponding tab pane
    document.querySelector(href).classList.add('show', 'active');

    // Hide all other tab panes
    var allTabPanes = document.querySelectorAll('.tab-pane');
    allTabPanes.forEach(function(pane) {
      if (pane.id !== href.substring(1)) {
        pane.classList.remove('show', 'active');
      }
    });
  });
});

