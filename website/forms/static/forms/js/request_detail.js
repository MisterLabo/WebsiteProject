document.addEventListener('DOMContentLoaded', () => {
    const backButton = document.querySelector('.btn-secondary');

    backButton.addEventListener('click', (event) => {
        if (!confirm('Are you sure you want to go back to the list? Unsaved changes will be lost.')) {
            event.preventDefault();
        }
    });
});
