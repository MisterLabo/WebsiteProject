document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    form.addEventListener('submit', (event) => {
        if (!confirm('Are you sure you want to submit this request?')) {
            event.preventDefault();
        }
    });
});
