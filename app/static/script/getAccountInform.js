var logStatus = document.getElementById('logStatus');

if (logStatus == 0) {
    var card_number = document.getElementById('card_number');
    var card_holder = document.getElementById('card_holder');
    var ballance = document.getElementById('ballance');

    card_number.innerHTML = '{{card_number}}';
    card_holder.innerHTML = '{{card_holder}}';
    ballance.innerHTML = '{{balance}}';
    alert("card_holder : " + '{{card_holder}}');
}