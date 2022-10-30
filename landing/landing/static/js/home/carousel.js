const carousel = document.querySelector(".carousel");
const carouselPics = document.querySelector(".carousel__pics");

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

const nextPic = () => {
    carouselPics.querySelectorAll('img')
        .forEach(pic => pic.classList.remove('active'));

    state.actual++;
    if(state.actual == state.count) state.actual = 0;
    let pic = carouselPics.querySelector(`img:nth-child(${state.actual + 1})`);
    pic.classList.add('active');
}

const prevPic = () => {
    carouselPics.querySelectorAll('img')
        .forEach(pic => pic.classList.remove('active'));

    state.actual--;
    if(state.actual < 0) state.actual += state.count;
    let pic = carouselPics.querySelector(`img:nth-child(${state.actual + 1})`);
    pic.classList.add('active');
}

if (state.count > 1) setInterval(nextPic, 4000);