$(document).ready(function() {

    updateNotificationsBadge(-1, false);
    updateMessagesBadge(false);

    $('#dropdownULNotifications').on("click.bs.dropdown", function (e) {
        e.stopPropagation();
        e.preventDefault();
    });

    $("#btnSendNotification").click(function(){
                document.getElementById("alert-empty-fields").style.display = "none";
                var message = document.getElementById("notificationMessage").value;
                var place = document.getElementById("notificationPlace").value;
                var time = document.getElementById("notificationTime").value;
                var username = document.getElementById("userSelected").value;
                if (message == "" || place == "" || time == "") {
                    document.getElementById("alert-empty-fields").style.display = "inherit";
                    $("#alert-empty-fields").fadeTo(1000, 500).slideUp(500, function(){
                        $("#alert-empty-fields").slideUp(500);
                    });
                }
                else {
                    $('#notificationModal').modal('hide');
                    $.ajax({
                        type: 'POST',
                        url: "/connect/notification/",
                        data: {
                            message: message,
                            place: place,
                            time: time,
                            username: username,
                            "csrfmiddlewaretoken": document.getElementById("token").value
                            },
                        success: function(response){
                        }
                    }).done(function(data){
                    });
                }
            });

    $("#sidebar-toggle, #sidebar-toggle2").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    $('#notificationMessage').maxlength({
            alwaysShow: true,
            threshold: 140,
            warningClass: "label label-success",
            limitReachedClass: "label label-danger"
        });

    $(".form_datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii"
    });
    refreshOnlineUsers(false);
    setInterval(function(){refreshOnlineUsers(true);}, 10000);

});

function updateNotificationsBadge(messageID, remove) {
            var messages = document.getElementById("messages").name;
            var accepted = (messages.match(/accepted/g) || []).length;
            var rejected = (messages.match(/rejected/g) || []).length;
            var notifications = accepted + rejected;
            if (remove == true) {
                $("li[id^=" + messageID + "]").remove();
                var badgeNumber = document.getElementById("badgeLabelNotifications").innerHTML;
                var remaining = parseInt(badgeNumber) - 1;
                document.getElementById("badgeLabelNotifications").innerHTML = remaining
            }
            else {
                 document.getElementById("badgeLabelNotifications").innerHTML = notifications;
            }
}

function updateMessagesBadge(remove) {
    var messages = document.getElementById("messages").name;
    var total = (messages.match(/Notification/g) || []).length;
    if (remove == false) {
        var accepted = (messages.match(/accepted/g) || []).length;
        var rejected = (messages.match(/rejected/g) || []).length;
        var discard = parseInt(accepted) + parseInt(rejected);
        document.getElementById("badgeLabel").innerHTML = parseInt(total) - parseInt(discard);
    }
    else {
        var badgeNumber = document.getElementById("badgeLabel").innerHTML;
        document.getElementById("badgeLabel").innerHTML = parseInt(badgeNumber) - 1;
    }

    var badgeNumber = document.getElementById("badgeLabel").innerHTML;
}


function dismissAlert(messageID) {
        updateNotificationsBadge(messageID, true);
        $.ajax({
            type: 'POST',
            url: "/connect/dismissAlert/",
            data: {
                id: messageID,
                "csrfmiddlewaretoken": document.getElementById("token").value
            },
            success: function(response){
            }
            }).done(function(data){

            });
}
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

function createPushNotification(userID, userFullName, online) {
    if (online == "true") {
        document.getElementById("notificationMessage").value = "";
        document.getElementById("notificationPlace").value = "";
        document.getElementById("notificationTime").value = "";
        document.getElementById("alert-empty-fields").style.display = "none";
        document.getElementById("user_name").innerHTML = userFullName;
        document.getElementById("userSelected").value = userID;
        $('#notificationModal').modal('show');
    }
    else {
        document.getElementById("alert-offline-user").style.display = "inherit";
        $("#alert-offline-user").fadeTo(2000, 500).slideUp(500, function(){
            $("#alert-offline-user").slideUp(500);
        });
    }
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
                        a.addEventListener("click", function() { createPushNotification(user.username, userFullName, user.online); }, false);
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

        })
}

function readMessage(messageID, choice, recipient, meeting) {
            updateMessagesBadge(true);
            $("div[id^=" + messageID + "]").remove();
            var messagesLeft = $('.thumbnail').length
            if (messagesLeft == 0) {
                document.getElementById("badgeLabel").innerHTML = 0;
                document.getElementById("alert-messages").innerHTML = "You have no available invitations";
            }
            document.getElementById("badgeLabel").innerHTML = messagesLeft;
            $.ajax({
                    type: 'POST',
                    url: "/connect/readMessage/",
                    data: {
                        id: messageID,
                        action: choice,
                        recipient: recipient,
                        meeting: meeting,
                        "csrfmiddlewaretoken": document.getElementById("token").value,
                    },
                    success: function(response){
                    }
                }).done(function(data){
                });
}


