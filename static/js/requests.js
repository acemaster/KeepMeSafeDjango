function acceptreq(id) {
	$.ajax({
        url : "/acceptreq/", // the endpoint
        type : "POST", // http method
        data : {'id': id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); 
            Materialize.toast('Request Accepted', 4000);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
}


function rejectreq(id) {
	$.ajax({
        url : "/rejectreq/", // the endpoint
        type : "POST", // http method
        data : {'id': id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); 
            Materialize.toast('Request Rejected', 4000);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
}