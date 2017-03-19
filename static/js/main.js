$(document).ready(function() {

    $(".form_datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii"
    });

    refreshOnlineUsers(false);
});

function createPushNotification(userID, userFullName) {
    document.getElementById("notificationMessage").value = "";
    document.getElementById("notificationPlace").value = "";
    document.getElementById("notificationTime").value = "";
    document.getElementById("alert-empty-fields").style.display = "none";
    document.getElementById("user_name").innerHTML = userFullName;
    $('#notificationModal').modal('show');
}


function refreshOnlineUsers(refresh) {
    $.ajax({
            type: 'GET',
            url: "/connect/all_users/",
            dataType: "json",
            success: function(response){
                var ul = document.getElementById("users_list");
                if (refresh == true)
                    $('#users_list li:not(:first)').remove();
                if (response.users.length > 0) {
                    $.each(response.users, function(index,user) {
                        var li = document.createElement("li");
                        var userFullName = user.first_name + " " + user.last_name;
                        a = document.createElement('a');
                        a.id = user.username;
                        a.addEventListener("click", function() { createPushNotification(user.username, userFullName); }, false);
                        a.href =  '#';
                        a.innerHTML = userFullName;
                        li.appendChild(a);
                        sp = document.createElement('span');
                        sp.className = "glyphicon glyphicon-map-marker";
                        if (user.online == "true")
                            sp.style = "color:green; float: left; vertical-align:middle";
                        else
                            sp.style = "color:red; float: left; vertical-align:middle";
                        ul.appendChild(li);
                        $('#' + user.username).prepend(sp);
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

