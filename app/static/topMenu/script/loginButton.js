var logStatus = '{{logStatus}}';

if (logStatus == 0) {
    var logBtn = document.getElementById("loginBtn");
    logBtn.id = "logoutBtn";
}
else {
    var logBtn = document.getElementById("logoutBtn");
    logBtn.id = "loginBtn";
}