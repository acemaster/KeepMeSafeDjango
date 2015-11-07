var l=[]

function getcLocation() {
  console.log("Hello");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getlatlongt);
    } else {
       console.log("Not found");
    }
}


function getlatlongt(position) {
    console.log("Getting current location........");
    lat=position.coords.latitude;
    longt=position.coords.longitude;
    l.push(lat);
    l.push(longt);
    console.log(l);
}

getcLocation();
function initialize() {
      console.log(l);
      var myLatlng = new google.maps.LatLng(l[0], l[1]);
      var myOptions = {
        zoom: 8,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      }
      map = new google.maps.Map(document.getElementById("googleMap"), myOptions);
    }

    function loadScript() {
      var script = document.createElement("script");
      script.type = "text/javascript";
      script.src = "http://maps.google.com/maps/api/js?sensor=false&callback=initialize";
      document.body.appendChild(script);
    }

function isLocationFree(lat,longt) {
  for (var i = 0, l = lookup.length; i < l; i++) {
    if (lookup[i][0] === lat && lookup[i][1] === longt) {
      return false;
    }
  }
  return true;
}

var lookup = [];

function getLocation() {
  console.log("Hello");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
       console.log("Not found");
    }
}


function showPosition(position) {
    lat=position.coords.latitude;
    longt=position.coords.longitude;
    var myLatlng = new google.maps.LatLng(lat,longt);
    var marker = new google.maps.Marker({
          position: myLatlng,
        title:"Hello World!"
    });
    map.setCenter(myLatlng);
    $.ajax({
        url : "/updatelatlongt/", // the endpoint
        type : "POST", // http method
        data : {'lat': lat, 'longt': longt}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error"); // provide a bit more info about the error to the console
        }
    });
    if(isLocationFree(lat,longt) == true)
    {
        marker.setMap(map);
        lookup.push([lat,longt])
    }
    else
      console.log("False");

}


$('#getlocation').click(getLocation);


window.onload = loadScript;