// Get elements
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const showSignup = document.getElementById("showSignup");
const showLogin = document.getElementById("showLogin");

// Show Signup Form
showSignup.addEventListener("click", (e) => {
  e.preventDefault();
  loginForm.classList.remove("active");
  signupForm.classList.add("active");
});

// Show Login Form
showLogin.addEventListener("click", (e) => {
  e.preventDefault();
  signupForm.classList.remove("active");
  loginForm.classList.add("active");
});

// Handle Login Form Submission
  document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault(); // stop actual form submission
    
    // Will check credentials with backend
    // For now, just redirect to dashboard.html
    window.location.href = "dashboard.html";
  });


