// Form validation
document.querySelector('form').addEventListener('submit', function(e) {
    const ratings = document.querySelectorAll('input[type="radio"]:checked');
    if (ratings.length < 15) { // We have 15 rating categories
        e.preventDefault();
        alert('Please provide ratings for all categories before submitting.');
    }
});