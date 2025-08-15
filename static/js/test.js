document.querySelector('.search-bar input').addEventListener('input', function(e) {
    let searchQuery = e.target.value.toLowerCase();
    let videoItems = document.querySelectorAll('.video-item');

    videoItems.forEach(function(item) {
        let title = item.querySelector('h3').textContent.toLowerCase();
        if (title.includes(searchQuery)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});
