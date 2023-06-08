// script.js
const movieImages = document.querySelectorAll('.movie-image');

movieImages.forEach((image) => {
    image.addEventListener('mouseenter', () => {
        image.style.transform = 'scale(1.1)';
    });

    image.addEventListener('mouseleave', () => {
        image.style.transform = 'scale(1)';
    });
});
