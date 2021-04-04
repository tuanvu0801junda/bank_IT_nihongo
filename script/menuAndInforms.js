var accountInfo = document.getElementById("accountInform");
var menuBar = document.getElementById("menuBar");

window.onscroll = function() {scrollFunction()};
function scrollFunction() {
    if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
        menuBar.className += " menuBarFixed";
        for (var i = 0; i < informs.length; i++) {
            informs[i].className += " informDivFixed";
        }
    } else {
        informs.style.display = "none";
    }
}