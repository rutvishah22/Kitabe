document.addEventListener('DOMContentLoaded', function() {
    const checkoutBtn = document.querySelector('.checkout-btn');
    
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            // In a real app, this would redirect to a checkout page
            alert('Checkout functionality would be implemented here.');
        });
    }
});