// scripts.js

// Function to toggle the navigation menu on smaller screens
function toggleNav() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('active');
}

// Close the navigation menu when a link is clicked
function closeNavOnClick() {
    const navLinks = document.querySelectorAll('#navMenu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const navMenu = document.getElementById('navMenu');
            navMenu.classList.remove('active');
        });
    });
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.getElementById('navToggle');
    if (navToggle) {
        navToggle.addEventListener('click', toggleNav);
    }
    closeNavOnClick();
});