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
                var ul = document.getElementById("users_list");
                if (response.users.length > 0) {
                    $.each(response.users, function(index,user) {
                        var li = document.createElement("li");
                        a = document.createElement('a');
                        a.href =  '#';
                        a.innerHTML = user.first_name + " " + user.last_name;
                        li.appendChild(a);
                        ul.appendChild(li);
                    });
                }
                else {
                     var li = document.createElement("li");
                     a = document.createElement('a');
                     a.href =  '#';
                     a.innerHTML = "No online users at the moment"
                     li.appendChild(a);
                     ul.appendChild(li);
                }
            }
        }).done(function(data){
        });
});

function refreshOnlineUsers() {
    $.ajax({
            type: 'GET',
            url: "/connect/all_users/",
            dataType: "json",
            success: function(response){
                var ul = document.getElementById("users_list");
                $('#users_list li:not(:first)').remove();
                if (response.users.length > 0) {
                    $.each(response.users, function(index,user) {
                        var li = document.createElement("li");
                        a = document.createElement('a');
                        a.href =  '#';
                        a.innerHTML = user.first_name + " " + user.last_name;
                        li.appendChild(a);
                        ul.appendChild(li);
                    });
                }
                else {
                     var li = document.createElement("li");
                     a = document.createElement('a');
                     a.href =  '#';
                     a.innerHTML = "No online users at the moment"
                     li.appendChild(a);
                     ul.appendChild(li);
                }
            }
        }).done(function(data){
        });
}
