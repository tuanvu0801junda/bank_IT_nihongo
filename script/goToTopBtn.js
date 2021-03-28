var topBtn = document.getElementById("goTopBtn");
var intervalFunc, x = 1, currentLoct, autoRolling = false;

function tickFunction() {
    currentLoct -= x;
    document.body.scrollTop = currentLoct;
    document.documentElement.scrollTop = currentLoct;
    if (x == 0) {
        clearInterval(intervalFunc);
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
        autoRolling = false;
    }
    else x-=2;
}

window.onscroll = function() {scrollFunction()};
function scrollFunction() {
    if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
        if (autoRolling != true)
        topBtn.style.display = "block";
    } else {
        topBtn.style.display = "none";
    }
}

function topFunction() {
    autoRolling = true;
    x = 0;
    tickCount = 0;
    topBtn.style.display = "none";
    
    currentLoct = document.documentElement.scrollTop;
    while ((x+2)*((x+2)/2+1)/2 <= currentLoct) x+=2;
    intervalFunc = setInterval (tickFunction, 5);
}