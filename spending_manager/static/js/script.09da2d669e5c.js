
function aktualnyCzas() {
    var today = new Date();
    var godzina = today.getHours();
    var minuta = today.getMinutes();
    var sekundy = today.getSeconds();
    var el = document.getElementById('1').innerHTML = godzina + ":" + minuta + ":" + sekundy;
    var clock = setTimeout(aktualnyCzas, 1000);
}

var message = "test raz dwa trzy";
var el = document.getElementById('2').innerHTML = message;