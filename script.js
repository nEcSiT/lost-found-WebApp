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


 
  const fileInput = document.getElementById("photo-upload");
  const preview = document.getElementById("preview");

  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.innerHTML = `<img src="${e.target.result}" 
                                alt="Preview" 
                                style="max-width:200px; margin-top:10px; border-radius:8px;">`;
      };
      reader.readAsDataURL(file);
    }
  });

  // Check if "capture" is supported
  if (!("capture" in document.createElement("input"))) {
    console.log("⚠️ Capture not supported — falling back to file picker.");
    // Optionally, show a message
    // preview.insertAdjacentHTML("beforebegin", "<p>Please upload a photo from your device.</p>");
}

    files.forEach(file => {
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = document.createElement("img");
          img.src = e.target.result;
          preview.appendChild(img);
        };
        reader.readAsDataURL(file);
      }
    });
  
  const photoUpload = document.getElementById("photo-upload");
  const previewGrid = document.getElementById("preview");
  const reportForm = document.getElementById("report-form");

  let approvedFiles = [];

  photoUpload.addEventListener("change", function () {
    previewGrid.innerHTML = "";
    approvedFiles = [];

    Array.from(this.files).forEach((file) => {
      const reader = new FileReader();
      reader.onload = function (e) {
        const previewItem = document.createElement("div");
        previewItem.classList.add("preview-item");

        previewItem.innerHTML = `
          <img src="${e.target.result}" alt="Preview">
          <div class="preview-actions">
            <button type="button" class="approve-btn">Approve</button>
            <button type="button" class="reject-btn">Reject</button>
          </div>
        `;

        previewItem.querySelector(".approve-btn").addEventListener("click", () => {
          if (!approvedFiles.includes(file)) {
            approvedFiles.push(file);
          }
          previewItem.style.border = "3px solid #28a745";
        });

        previewItem.querySelector(".reject-btn").addEventListener("click", () => {
          previewItem.remove();
          approvedFiles = approvedFiles.filter(f => f !== file);
        });

        previewGrid.appendChild(previewItem);
      };
      reader.readAsDataURL(file);
    });
  });

  reportForm.addEventListener("submit", function (e) {
    e.preventDefault();

    if (approvedFiles.length === 0) {
      alert("Please approve at least one photo before submitting.");
      return;
    }

    const formData = new FormData(reportForm);

    // Replace default file input with only approved ones
    approvedFiles.forEach((file) => {
      formData.append("approvedPhotos[]", file);
    });

    fetch(reportForm.action, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.text())
      .then((data) => {
        alert("Report submitted successfully!");
        console.log(data);
      })
      .catch((err) => console.error("Upload error:", err));
  });


  



