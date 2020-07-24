function RaceTimer() {

  var race_end = json_data.heat_end
  var countDownDate = new Date(race_end).getTime();
  // console.log(race_end);

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="race_timer"
  document.getElementById("race_timer").innerHTML = "Time Left:" + hours + "h "
  + minutes + "m " + seconds + "s ";

  // If the count down is finished, write some text
  if (distance < 0) {
//    clearInterval(timer_interval);
    document.getElementById("race_timer").innerHTML = "Time Left: 00:00";
  }
}


// Update the count down every 1 second
var timer_interval = setInterval(function(){ RaceTimer();}, 900);


