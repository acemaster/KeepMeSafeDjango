$(document).ready(function(){
	function getnotifications () {
		$.ajax({
        url : "/getnotification/", // the endpoint
        type : "POST", // http method
        data : {'id': 1}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            // console.log(json);
            if(json.success ==1)
            { 
            	Materialize.toast(json.message, 4000);
            	console.log("Success");
            	$.ajax({
        			url : "/recnotification/", // the endpoint
        			type : "POST", // http method
        			data : {'id': json.id}, // data sent with the post request

        // handle a successful response
				    success : function(json) {
				         // remove the value from the input
				        // console.log(json);
				        console.log("Success");    	
				    },

				    // handle a non-successful response
				    error : function(xhr,errmsg,err) {
				        console.log("Error");
				        // Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
				    }
				});
            }     	
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            // Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
	}


function countnotifications () {
        $.ajax({
        url : "/getnotificationcount/", // the endpoint
        type : "POST", // http method
        data : {'id': 1}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            // console.log(json);
            if(json.count != '0'){
                if($('noticount').length > 0)
                    $('noticount').remove();
                var st="<span class='new badge' id='noticount'>"+json.count+"</span>";
                $('#notification').append(st);
            } 
            else{
                if($('noticount').length > 0)
                    $('noticount').remove();
            }     
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            // Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
    }


    

	setInterval(getnotifications,5000);
    setInterval(countnotifications,5000);

})