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

  document.querySelectorAll(".category-card").forEach(card => {
    card.addEventListener("click", () => {
      const items = card.querySelector(".category-items");
      items.style.display = items.style.display === "flex" ? "none" : "flex";
    });
  });


  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  searchBtn.addEventListener("click", () => {
    const query = searchInput.value.toLowerCase().trim();
    if (!query) return;

    let found = false;

    // Loop through categories
    document.querySelectorAll(".category-card").forEach(card => {
      const items = card.querySelectorAll(".category-items .item");
      items.forEach(item => {
        if (item.textContent.toLowerCase().includes(query)) {
          // Expand category
          const categoryItems = card.querySelector(".category-items");
          categoryItems.style.display = "flex";

          // Highlight the found item
          item.style.background = "#ffd166";
          item.style.fontWeight = "bold";

          // Scroll into view
          item.scrollIntoView({ behavior: "smooth", block: "center" });

          found = true;
        }
      });
    });

    if (!found) {
      alert("Item not found in any category.");
    }
  });
  item.classList.add("highlight");
setTimeout(() => item.classList.remove("highlight"), 3000);


