$(document).ready(function(){

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
    $.ajax({
        url : "/checklocation/", // the endpoint
        type : "POST", // http method
        data : {'lat': lat, 'longt': longt}, // data sent with the post request
        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); // log the returned json to the console
            if(json.success == 1){
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
    			console.log("Updated location");
    			$.ajax({
        			url : "/sendmessage/", // the endpoint
        			type : "POST", // http method
        			data : {'id':1,'lat': lat, 'longt': longt}, // data sent with the post request

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


            } 
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error"); // provide a bit more info about the error to the console
        }
    });
    
}

setInterval(getcLocation, 5000);


// function __log(e, data) {
//     console.log("\n" + e + " " + (data || ''));
//   }
//   var audio_context;
//   var recorder;
//   function startUserMedia(stream) {
//     var input = audio_context.createMediaStreamSource(stream);
//     __log('Media stream created.');
//     // Uncomment if you want the audio to feedback directly
//     //input.connect(audio_context.destination);
//     //__log('Input connected to audio context destination.');
    
//     recorder = new Recorder(input);
//     __log('Recorder initialised.');
//   }

//   function startRecording() {
//     recorder && recorder.record();
//     __log('Recording...');
//   }
//   function stopRecording() {
//     recorder && recorder.stop();
//     __log('Stopped recording.');
    
//     // create WAV download link using audio data blob
//     createDownloadLink();
    
//     recorder.clear();
//   }
//   function createDownloadLink() {
//     recorder && recorder.exportWAV(function(blob) {
//       var url = URL.createObjectURL(blob);
//       var li = document.createElement('li');
//       var au = document.createElement('audio');
//       var hf = document.createElement('a');
      
//       au.controls = true;
//       au.src = url;
//       hf.href = url;
//       hf.download = new Date().toISOString() + '.wav';
//       hf.innerHTML = hf.download;
//       li.appendChild(au);
//       li.appendChild(hf);
//       recordingslist.appendChild(li);
//     });
//   }


// function init() {
//     try {
//       // webkit shim
//       window.AudioContext = window.AudioContext || window.webkitAudioContext;
//       navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
//       window.URL = window.URL || window.webkitURL;
      
//       audio_context = new AudioContext;
//       __log('Audio context set up.');
//       __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
//       startRecording();
//     } catch (e) {
//       alert('No web audio support in this browser!');
//     }
    
//     navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
//       __log('No live audio input: ' + e);
//     });
//   }


//   init();
});