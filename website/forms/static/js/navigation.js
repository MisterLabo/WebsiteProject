document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector(".navbar");
    const toggleButton = document.querySelector(".navbar-toggle");

    toggleButton.addEventListener("click", () => {
        navbar.classList.toggle("hidden");
    });
});
