
$(document).ready(function(){
// var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
function gotopage(){
			Cookies.set('safe', 1);
			window.location.href = "iamnotsafe";
}

$('#safe-button').click(function(){
			console.log("I am safe");
			clearTimeout(myVar);
			Cookies.set('safe', 1);
			$('#safeoverlay').remove();
		  	$('#safemodal').remove();
});


var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
var timerem=5;
var height=$('nav').height();

$('#sidebar2').css({'top':height});
$('#safeoverlay').css({'top':height});
$('#sidebar2').hide();

$('#logo').click(function(){
	$('#sidebar2').toggle();
	$('#safeoverlay').toggle();
});

function timer(){
	timerem=timerem-1;
	$('#timeout').html(timerem);
}

console.log("Check");
if(Cookies.get('safe')!=1){
	console.log("Not safe");
	var myVar2 = setInterval(timer, 1000);
	var myVar = setTimeout(gotopage, 5000);
}
else{
	$('#safeoverlay').hide();
	$('#safemodal').remove();
}
});


