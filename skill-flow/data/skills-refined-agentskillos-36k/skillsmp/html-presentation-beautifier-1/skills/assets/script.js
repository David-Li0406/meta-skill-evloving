let currentSlide = 1;
let totalSlides = 0;

function init() {
    const slides = document.querySelectorAll('.slide');
    totalSlides = slides.length;
    document.getElementById('totalSlides').textContent = totalSlides;

    document.addEventListener('keydown', handleKeyPress);
}

function navigate(direction) {
    const newSlide = currentSlide + direction;

    if (newSlide >= 1 && newSlide <= totalSlides) {
        document.querySelector(`.slide[data-slide="${currentSlide}"]`).classList.remove('active');
        currentSlide = newSlide;
        document.querySelector(`.slide[data-slide="${currentSlide}"]`).classList.add('active');
        document.getElementById('currentSlide').textContent = currentSlide;
        updateNavButtons();
    }
}

function handleKeyPress(e) {
    if (e.key === 'ArrowRight' || e.key === ' ') {
        navigate(1);
    } else if (e.key === 'ArrowLeft') {
        navigate(-1);
    } else if (e.key === 'Escape') {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    }
}

function updateNavButtons() {
    document.getElementById('prevBtn').disabled = currentSlide === 1;
    document.getElementById('nextBtn').disabled = currentSlide === totalSlides;
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

document.addEventListener('DOMContentLoaded', init);
