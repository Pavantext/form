// Form validation
document.querySelector('form').addEventListener('submit', function(e) {
    const ratings = document.querySelectorAll('input[type="radio"]:checked');
    if (ratings.length < 15) { // We have 15 rating categories
        e.preventDefault();
        alert('Please provide ratings for all categories before submitting.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Get all star rating groups
    const ratingGroups = document.querySelectorAll('.rating-group');
    
    ratingGroups.forEach(group => {
        const stars = group.querySelectorAll('input[type="radio"]');
        const commentBox = group.querySelector('.low-rating-comment');
        
        if (!commentBox) return; // Skip if no comment box found
        
        stars.forEach(star => {
            star.addEventListener('change', function() {
                const rating = parseInt(this.value);
                const ratingName = this.name.replace('_rating', '').replace('-', ' ');
                
                if (rating <= 2) {
                    commentBox.style.display = 'block';
                    commentBox.required = true;
                    commentBox.placeholder = `Please tell us why you gave ${rating} star${rating === 1 ? '' : 's'} for ${ratingName} and how we can improve...`;
                } else {
                    commentBox.style.display = 'none';
                    commentBox.required = false;
                    commentBox.value = ''; // Clear the comment
                }
            });
        });
    });
});