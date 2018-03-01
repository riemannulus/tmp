import './sky.scss';

const containerElem = document.querySelector('.container');
const cubeElem = document.querySelector('.cube');
const TIME = 5000;

let timestamp = null;
let tmp = 0;


function almost(value, expected, threshold) {
    return Math.abs(expected - value) <= threshold;
}

// https://tovotu.de/tests/compass/index.html

function rotate(vec, axis, angle) {
    let c = Math.cos(angle * Math.PI / 180);
    let s = Math.sin(angle * Math.PI / 180);
    let [x, y, z] = axis;

    // rotation matrix form
    let rm00 =    c + x*x * (1-c);
    let rm10 =  z*s + y*x * (1-c);
    let rm20 = -y*s + z*x * (1-c);
    let rm01 = -z*s + x*y * (1-c);
    let rm11 =    c + y*y * (1-c);
    let rm21 =  x*s + z*y * (1-c);
    let rm02 =  y*s + x*z * (1-c);
    let rm12 = -x*s + y*z * (1-c);
    let rm22 =    c + z*z * (1-c);

    return Array(
        rm00 * vec[0] + rm01 * vec[1] + rm02 * vec[2],
        rm10 * vec[0] + rm11 * vec[1] + rm12 * vec[2],
        rm20 * vec[0] + rm21 * vec[1] + rm22 * vec[2]
    );
}

function motionHandler(event) {

    let b = event.beta;
    let g = -event.gamma;
    let a = event.alpha;
    let defaultAngle = 0;

    let defaultZ = Array(0, 0, 1);
    let defaultX = rotate(Array(1, 0, 0), defaultZ, defaultAngle);
    let defaultY = rotate(Array(0, 1, 0), defaultZ, defaultAngle);

    let axisY = defaultY;
    let axisX = rotate(defaultX, axisY, g);
    let axisZ = rotate(rotate(defaultZ, axisY, g), axisX, b);

    cubeElem.style.transform = (
        `rotate3d(${axisZ.join(', ')}, ${a}deg)` +
        `rotate3d(${axisX.join(', ')}, ${b}deg)` +
        `rotate3d(${axisY.join(', ')}, ${g}deg)`);

    if (event.beta > 140 &&
        almost(event.gamma, 0, 10)) {
        if (timestamp) {
            tmp = Math.min(Date.now() - timestamp, TIME);
        } else {
            timestamp = Date.now();
        }
    } else {
        timestamp = null;
        tmp = 0;
    }

    containerElem.style.background = `rgba(255, 0, 0, ${tmp / TIME})`;

}

if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', motionHandler);
} else {
    document.body.style.background = 'black';
}
