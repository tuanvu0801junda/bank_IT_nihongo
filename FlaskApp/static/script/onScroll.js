var topBtn = document.getElementById("goTopBtn");
var intervalFunc, x = 1, currentLoct, autoRolling = false;
var accountInfo = document.getElementById("accountInform").style;
var exangeRate = document.getElementById("exchangeRate").style;
var menuBar = document.getElementById("menuBar").style;

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

function changeToFixed() {
    // document.getElementById("menuBar").style.position = "fixed";
    menuBar.position="fixed";

    accountInfo.position = "fixed";
    accountInfo.top = "50px";
    exangeRate.position = "fixed";
    exangeRate.top = "50px";
}

function changeToRelative() {
    menuBar.position = "relative";

    accountInfo.position = "relative";
    accountInfo.top = "0";
    exangeRate.position = "relative";
    exangeRate.top = "0";
}

window.onscroll = function() {scrollFunction()};
function scrollFunction() {
    if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
        changeToFixed();
        if (autoRolling != true)
        topBtn.style.display = "block";
    } else {
        changeToRelative();
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