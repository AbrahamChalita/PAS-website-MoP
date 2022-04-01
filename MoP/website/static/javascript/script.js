// Funcion para invocar video trailer
var isBodyClicked = false;
function openVideo() {
    if(isBodyClicked === false){
      document.getElementById("trailer").innerHTML = "<video style='position:absolute;height:620px;top:215px;left:400px' controls> <source src='video/cuphead.mp4 type='video/mp4'> <source src='video/cuphead.mp4' type=''video/ogg'>Your browser does not support the video tag.</video>"
      document.body.removeEventListener('click', openVideo);
    }

    isBodyClicked = true;

}


// Funcion de estilo de footer
$(document).ready(function(){
	$(".slide").hide();
	// Run the effect
	$(".first").show('drop', 1000);
	
	if($("body").height() < $(window).height()){
		$("footer").css({
			"position":"absolute",
			"bottom":"0px"
		});
	};
});

$( function() {
    function runEffect(slide) {
      // Run the effect
      $( slide ).show('drop', 1000);
    };
 
    // Set effect from select menu value
    $( "#radio1" ).on( "click", function() {
      $(".taima").hide();
      runEffect(".miwok");
    });

    $( "#radio2" ).on( "click", function() {
      $(".miwok").hide();
      runEffect(".taima");
    });
});

// Funcion para dropear datos de personajes
// $( function() {
//     // run the currently selected effect
//     function runEffect() {
//       // Run the effect
//       $( ".effect" ).hide( 'drop', {}, 1000, callback );
//     };
 
//     // Callback function to bring a hidden box back
//     function callback() {
//       setTimeout(function() {
//         $( ".effect" ).removeAttr( "style" ).hide().fadeIn();
//       }, 1000 );
//     };
 
//     // Set effect from select menu value
//     $( "#button" ).on( "click", function() {
//       runEffect();
//     });
//   } );
