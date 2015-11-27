$(document).ready(function(){
    console.log("Forgot password");
function forgotpasswordcode() {
        var email=$('#email').val();
        $.ajax({
        url : "/forgot1/", // the endpoint
        type : "POST", // http method
        data : {'email': email}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); 
            $('#forgot1').hide();
             $('#forgot2').show();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            // Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
}

function validatecode() {
        var code=$('#code').val();
        var email=$('#email').val();
        $.ajax({
        url : "/forgot2/", // the endpoint
        type : "POST", // http method
        data : {'code': code, 'email':email}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); 
            $('#forgot2').hide();
             $('#forgot3').show();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            // Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
}

function reset() {
        var code=$('#password').val();
        var email=$('#email').val();
        $.ajax({
        url : "/forgot3/", // the endpoint
        type : "POST", // http method
        data : {'password':code, 'email':email}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); 
            window.location.href = "/login";
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error");
            $('#forgot3').hide();
            // Materialize.toast('Server Error', 4000); // provide a bit more info about the error to the console
        }
});
}
$('#forgot2').hide();
$('#forgot3').hide();
$('#forgot1_but').click(forgotpasswordcode);
$('#forgot2_but').click(validatecode);
$('#forgot3_but').click(reset);

});