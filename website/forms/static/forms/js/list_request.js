document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('a');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            if (!confirm('Are you sure you want to navigate to this page?')) {
                event.preventDefault();
            }
        });
    });
});
