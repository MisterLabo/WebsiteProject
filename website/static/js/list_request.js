// Confirm action before approving or rejecting a request
document.addEventListener('DOMContentLoaded', () => {
    const approveButtons = document.querySelectorAll('.btn-success');
    const rejectButtons = document.querySelectorAll('.btn-danger');

    approveButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            if (!confirm('Are you sure you want to approve this request?')) {
                event.preventDefault();
            }
        });
    });

    rejectButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            if (!confirm('Are you sure you want to reject this request?')) {
                event.preventDefault();
            }
        });
    });
});
