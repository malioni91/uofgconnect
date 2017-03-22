$(document).ready(function() {

    /** Update of the notifications badge on page load **/
    updateNotificationsBadge(-1, false);
    /** Update of the messages badge on page load **/
    updateMessagesBadge(false);

    /** Avoid closing dropdown on clicking inside **/
    $('#dropdownULNotifications').on("click.bs.dropdown", function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $('#notificationsToggle').on("click", function (e) {
       var badgeNumber = document.getElementById("badgeLabelNotifications").innerHTML;
       if (badgeNumber == 0) {
           e.stopPropagation();
           e.preventDefault();
       }
    });


    /** Sends message to selected user **/
    /** All fields are required **/
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

    /** Clicking one of the two buttons, toggles the sidebar **/
    $("#sidebar-toggle, #sidebar-toggle2").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    /** Message text maxlength plugin initialization **/
    $('#notificationMessage').maxlength({
            alwaysShow: true,
            threshold: 140,
            warningClass: "label label-success",
            limitReachedClass: "label label-danger"
        });
    /** Datetime field picker plugin initialized **/
    $(".form_datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii"
    });

    /** Load online users in sidebar on page load **/
    refreshOnlineUsers(false);
    /** Update the list of users every 10 secs **/
    setInterval(function(){refreshOnlineUsers(true);}, 10000);

});

/** Notification badge gets updated on page load **/
/** and when a notification is dismissed by the user **/
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
                if (remaining == 0)
                    $('.dropdown.open').removeClass('open');
            }
            else {
                 document.getElementById("badgeLabelNotifications").innerHTML = notifications;
                 if (notifications == 0)
                    $('.dropdown.open').removeClass('open');
            }
}

/** Message badge gets updated on page load **/
/** and when a message is accepted or rejected by the user **/
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

/** Dismiss notification and mark it as read **/
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

/** User filtering in the sidebar based on the name provided **/
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

/** Initialize modal to send a message **/
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

/** Refresh sidebar with online users **/
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

/** Function is called when a message is **/
/** accepted/rejected to mark it as read in the backend **/
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


