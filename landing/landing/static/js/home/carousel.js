const carousel = document.querySelector(".carousel");
const carouselPics = document.querySelector(".carousel__pics");
const carouselDots = document.querySelector(".carousel__dots");

const prevBtn = document.querySelector(".carousel__btn.left");
const nextBtn = document.querySelector(".carousel__btn.right");

const state = {
    actual: 0,
    count: carouselPics.children.length,
}

if(state.count == 1) {
    nextBtn.classList.add('hide');
    prevBtn.classList.add('hide');
}

const clean = () => {
    carouselPics.querySelectorAll('img')
        .forEach(pic => pic.classList.remove('active'));
    carouselDots.querySelectorAll('.carousel__dot').forEach(
        dot => dot.classList.remove('active')
    );
}

const define = () => {
    let pic = carouselPics.querySelector(`img:nth-child(${state.actual + 1})`);
    dot = carouselDots.querySelector(`.carousel__dot:nth-child(${state.actual + 1})`)
    dot.classList.add('active');
    pic.classList.add('active');
}

const nextPic = () => {
    clean();
    state.actual++;
    if(state.actual == state.count) state.actual = 0;
    define();
}

const prevPic = () => {
    clean();
    state.actual--;
    define();
}

let pic = carouselPics.querySelector(`img:nth-child(${state.actual + 1})`);
dot = carouselDots.querySelector(`.carousel__dot:nth-child(${state.actual + 1})`)
pic.classList.add('active');
dot.classList.add('active');
if (state.count > 1) setInterval(nextPic, 8000);

for(let i = 0; i < state.count; i++) {
    let dot = document.createElement('div');
    dot.classList.add('carousel__dot');
    carouselDots.appendChild(dot);
}

nextBtn.addEventListener( 'click', nextPic);
prevBtn.addEventListener( 'click', prevPic);