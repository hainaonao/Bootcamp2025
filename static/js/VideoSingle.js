document.addEventListener("DOMContentLoaded", function () {
      const bellBtn = document.getElementById("bell-btn");
      const dropdown = document.getElementById("notification-dropdown");
      bellBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        dropdown.classList.toggle("hidden");
      });
      document.addEventListener("click", function () {
        dropdown.classList.add("hidden");
      });
      dropdown.addEventListener("click", function (e) {
        e.stopPropagation();
      });
    });