$(document).ready(function() {

    $(".form_datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii"
    });

    refreshOnlineUsers(false);
});

function filterUsers() {
    var input, filter, ul, li, a, i;
    input = document.getElementById('filter');
    filter = input.value.toUpperCase();
    ul = document.getElementById("users_list");
    li = $("#users_list li");
    // Loop through all list items, and hide those who don't match the search query
    for (i = 1; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function createPushNotification(userID, userFullName) {
    document.getElementById("notificationMessage").value = "";
    document.getElementById("notificationPlace").value = "";
    document.getElementById("notificationTime").value = "";
    document.getElementById("alert-empty-fields").style.display = "none";
    document.getElementById("user_name").innerHTML = userFullName;
    $('#notificationModal').modal('show');
}


function refreshOnlineUsers(refresh) {
    document.getElementById("filter").value = "";
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
                        li.appendChild(a);
                        i = document.createElement('i');
                        i.className = "glyphicon glyphicon-map-marker";
                        sp = document.createElement('span');
                        sp.innerHTML = userFullName;
                        if (user.online == "true")
                            i.style = "color:green; padding-right:25px";
                        else
                            i.style = "color:red; padding-right:25px";
                        ul.appendChild(li);
                        $('#' + user.username).prepend(sp).prepend(i);
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

