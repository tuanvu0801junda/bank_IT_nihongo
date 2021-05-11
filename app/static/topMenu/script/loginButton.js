var logStatus = '{{logStatus}}';

//0 : Da dang nhap, 1 : Chua dang nhap

if (logStatus == 0) {
    var logBtn = document.getElementById("logBtn");
    logBtn.style.visibility = "visible";
}
else {
    var logBtn = document.getElementById("logBtn");
    logBtn.style.visibility = "hidden";
}