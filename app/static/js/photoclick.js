'use strict';

window.addEventListener('DOMContentLoaded', () => {

    const upperitems = document.querySelectorAll('.upper-coruselitem');
    const downitems = document.querySelectorAll('.down-coruselitem');

    const up_container = document.querySelector('.upper-photocontainer');
    const down_container = document.querySelector('.down-photocontainer');

    Array.from(upperitems).forEach((it) => {
        it.addEventListener('click', (e) => {
            const img = e.currentTarget.querySelector('img');
            
            //вот тут логика отправления на бэк
            const api_to_improve = '/clearbin/';
            const image_url = img.src.split('/').slice(3, img.src.split('/').length).join('/');
            const uploadToBackend = async () => {
                const blob = await fetch(/*api_to_improve +*/ img.src) //раскоментить, если будет на беке обработка и отправка фото
                    .then(res => res.blob());
                console.log(blob);
                const impoved_image = URL.createObjectURL(blob);
                up_container.style.backgroundImage = `url(${impoved_image})`;
            };
            uploadToBackend();
        });
    });

    Array.from(downitems).forEach((it) => {
        it.addEventListener('click', (e) => {
            const img = e.currentTarget.querySelector('img');

            //вот тут логика отправления на бэк
            const api_to_improve = '/faces/';
            const image_url = img.src.split('/').slice(3, img.src.split('/').length).join('/');
            const uploadToBackend = async () => {
                const blob = await fetch(/*api_to_improve +*/ img.src)
                    .then(res => res.blob());
                console.log(blob);
                const impoved_image = URL.createObjectURL(blob);
                down_container.style.backgroundImage = `url(${impoved_image})`;
            };
            uploadToBackend();
        });
    });
});