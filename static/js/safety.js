$(document).ready(function(){
$.ajax({
        url : "/getlist/", // the endpoint
        type : "POST", // http method
        data : {'search_term': ''}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); 
            var us=json.users;
            console.log(us);
            console.log(us.length);// log the returned json to the console
            console.log("success");
            var i=0;
            for(i=0;i<us.length;i++)
            {
                $('#results').append('<li class="collection-item avatar"><img src="'+us[i]['picture']+'" alt="" class="circle"><span class="title">'+us[i]['name']+'</span><p><br></p><p onclick="makefriend('+us[i]['id']+')" class="secondary-content"><i class="material-icons">stars</i></p></li>');
            } // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error"); // provide a bit more info about the error to the console
        }
});

});


$('#searchbar').on('input',function(){
    var search_term=$('#searchbar').val();
    $.ajax({
        url : "/getlist/", // the endpoint
        type : "POST", // http method
        data : {'search_term': search_term}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#results').empty();
            var us=json.users;
            console.log(us);
            console.log(us.length);// log the returned json to the console
            console.log("success");
            var i=0;
            for(i=0;i<us.length;i++)
            {
                $('#results').append('<li class="collection-item avatar"><img src="'+us[i]['picture']+'" alt="" class="circle"><span class="title">'+us[i]['name']+'</span><p><br></p><p class="secondary-content"><i class="material-icons">stars</i></p></li>');
            } // another sanity check

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error"); // provide a bit more info about the error to the console
        }
});


    

});
function makefriend (id) {
$.ajax({
        url : "/makefriend/", // the endpoint
        type : "POST", // http method
        data : {'id': id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
             // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success");
            Materialize.toast('Safety List Request Sent', 4000) // another sanity check

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("Error"); // provide a bit more info about the error to the console
        }
});
}