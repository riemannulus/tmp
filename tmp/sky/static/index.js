const alphaElem = document.querySelector('#alpha');
const betaElem = document.querySelector('#beta');
const gammaElem = document.querySelector('#gamma');
const tmpElem = document.querySelector('#tmp');

let timestamp = null;
let tmp = 0;


function almost(value, expected, threshold) {
    return Math.abs(expected - value) <= threshold;
}

function motionHandler(event) {
    alphaElem.innerText = Math.round(event.alpha);
    betaElem.innerText = Math.round(event.beta);
    gammaElem.innerText = Math.round(event.gamma);
    tmpElem.innerText = tmp;

    if (event.beta > 140 &&
        almost(event.gamma, 0, 10)) {
        if (timestamp) {
            tmp = Math.min(Date.now() - timestamp, 1000);
        } else {
            timestamp = Date.now();
        }
    } else {
        timestamp = null;
        tmp = 0;
    }

    document.body.style.background = `rgba(255, 0, 0, ${tmp / 1000})`;

}

if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', motionHandler);
} else {
    document.body.style.background = 'black';
}
