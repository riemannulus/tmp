import './qrcode.scss';

const imageContainer = document.querySelector('#large-image');

function imageClickHandler(event) {
    let img = event.target;
    let newImg = document.createElement('img');
    newImg.src = img.src;

    imageContainer.innerHTML = null;
    imageContainer.appendChild(newImg);
    imageContainer.style.display = 'block';
}

function closeLargeImage() {
    imageContainer.style.display = '';
}

for (let img of document.querySelectorAll('#plate .locked img')) {
    img.addEventListener('click', imageClickHandler);
}

imageContainer.addEventListener('click', closeLargeImage);
