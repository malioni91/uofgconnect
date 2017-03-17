$(document).ready(function() {
    $("#btnSearch").click(function(){
        document.getElementById("alert-not-found").style.display = "none";
        var email = document.getElementById("inpEmail").value;
        $.ajax({
            type: 'GET',
            url: "/connect/users/",
            data: {email: email}, //passing some input here
            dataType: "json",
            success: function(response){
                if (response.found) {
                    document.getElementById("user_name").innerHTML = response.full_name;
                }
                else {
                    document.getElementById("alert-not-found").style.display = "inherit";
                }
            }
        }).done(function(data){
        });
    });

    $.ajax({
            type: 'GET',
            url: "/connect/all_users/",
            dataType: "json",
            success: function(response){
                alert("response");
            }
        }).done(function(data){
        });
});
