// dashboard.js
// Handles navigation from dashboard to report lost page

document.addEventListener('DOMContentLoaded', function() {
  var buttons = document.querySelectorAll('.card button');
  buttons.forEach(function(btn) {
    if (btn.textContent.includes('Report Lost Item')) {
      btn.addEventListener('click', function() {
        window.location.href = 'report-lost-redirect.html';
      });
    }
    if (btn.textContent.includes('Report Found Item')) {
      btn.addEventListener('click', function() {
        window.location.href = 'report-found-redirect.html';
      });
    }
    if (btn.textContent.includes('View Items')) {
      btn.addEventListener('click', function() {
        window.location.href = 'view-items-redirect.html';
      });
    }
  });
});
