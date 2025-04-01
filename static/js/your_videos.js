
let index = 0;
const carouselContainer = document.querySelector(".carousel-container");
const totalVideos = document.querySelectorAll(".carousel-item").length;

function updateCarousel() {
    carouselContainer.style.transform = `translateX(-${index * 50}%)`;
}

function nextSlide() {
    if (index < (totalVideos - 4)/2) {
        index++;
        updateCarousel();
    }

}

function prevSlide() {
    if (index > 0) {
        index--;
        updateCarousel();
    }
}
