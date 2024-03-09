$(document).ready(function() {
    var canvas = document.getElementById("reloj");
    var ctx = canvas.getContext("2d");
    var radius = canvas.height / 2;
    ctx.translate(radius, radius);
    radius = radius * 0.90;

    var startTime = new Date().getTime();

    setInterval(actualizarCronometro, 1000);

    function actualizarCronometro() {
        var now = new Date().getTime();
        var elapsedTime = now - startTime;

        var hours = Math.floor(elapsedTime / (1000 * 60 * 60));
        var minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);

        var timeString = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
        
        ctx.clearRect(-radius, -radius, canvas.width, canvas.height);
        ctx.fillStyle = "white";
        ctx.fill();

        // Mostrar el tiempo transcurrido en el lienzo
        ctx.font = radius * 0.15 + "px Arial";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText(timeString, 0, 0);
    }
});
