from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.utils import timezone

from connect.forms import LoginForm, UserForm, UserProfileForm,EditForm
from connect.models import UserProfile, Map

from datetime import datetime
from notifications.signals import notify
from notifications.models import Notification

import json, feedparser

@login_required
def index(request):
    """The index page view"""
    request.session.set_test_cookie()
    user_coordinates = UserProfile.objects.all().exclude(user=request.user)
    user = User.objects.get(username=request.user.username)
    messages = user.notifications.unread()
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    online_users = User.objects.filter(id__in=uid_list, is_superuser=False)
    users_records = []
    for user in online_users:
        if user.username != request.user.username:
            users_records.append(user)
    feeds = feedparser.parse('http://www.gla.ac.uk/rss/news/index.xml')
    context_dict = {'coordinates': users_records, 'feeds': feeds, 'messages': messages}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'connect/index.html', context=context_dict)

def landing(request):
    """The landing page view that anonymous users see
    when they arrive to the webiste"""
    return render(request, "connect/landing.html")

@login_required
def messages(request):
    """The messages view that shows all the received messages from other peers """
    user = User.objects.get(username=request.user.username)
    messages = user.notifications.unread() # get the unread messages
    return render(request, "connect/messages.html", {'messages': messages})

def register(request):
    """The registration view that enables the users to register """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # Hash the password
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'connect/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    """The login view that enables users to login to the platform """
    authenticated = False
    login_form = LoginForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) # authenticate user
        if user:
            if user.is_active:
                login(request, user)
                authenticated = True
                return redirect('index')
            else:
                print(login_form.errors)
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
    else:
        login_form = LoginForm()

    return render(request, 'connect/login.html',
                  {'login_form': login_form, 'authenticated': authenticated})


def about(request):
    """The about page view that shows general infromation about the authors """
    messages = []
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        messages = user.notifications.unread()
    return render(request, "connect/about.html", {'messages': messages})


def faq(request):
    """The faq page that shows general infromation about frequent questions """
    messages = []
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        messages = user.notifications.unread()
    return render(request, 'connect/faq.html', {'messages': messages})


@login_required
def user_logout(request):
    """The user logout view"""
    logout(request)
    return HttpResponseRedirect('/connect/')

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    """Function to retrieve the server side cookie"""
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    """The cookie handler view"""
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                                str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit
    # update the last visit cookie now that we have updated the count
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits

@login_required
def user_edit(request):
    """The user profile edit view where users update their information"""
    userdetails = User.objects.get(username=request.user.username)
    messages = userdetails.notifications.unread()
    usercourse = UserProfile.objects.get(user=request.user)
    user_form = EditForm(request.POST,  instance=request.user)
    profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            usereditor = user_form.save(commit=False)
            if userdetails.check_password(usereditor.password):
                username = request.POST.get('username')
                passwordnew = request.POST.get('new_password')
                usereditor.set_password(passwordnew)
                usereditor.save()
                profile = profile_form.save(commit=False)
                profile.user = usereditor
                profile.save()
                user = authenticate(username=username, password=passwordnew)
                login(request,user)
            else:
                user_form = EditForm(initial={'name': " ".join([userdetails.first_name, userdetails.last_name]),'username':userdetails.username, 'email':userdetails.email})
                profile_form = UserProfileForm(initial={'course' : usercourse.course})
                return render(request, 'connect/edit.html', {'user_form': user_form , 'profile_form': profile_form, 'messages': messages})
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = EditForm(initial={'name': " ".join([userdetails.first_name, userdetails.last_name]),'username':userdetails.username, 'email':userdetails.email})
        profile_form = UserProfileForm(initial={'course' : usercourse.course})
        return render(request, 'connect/edit.html', {'user_form': user_form , 'profile_form': profile_form, 'messages': messages})

    return render(request, 'connect/edit.html', {'user_form': user_form , 'profile_form': profile_form, 'messages': messages})

def users(request):
    found = False
    try:
        user_found = User.objects.get(email=request.GET.get('email'))
        full_name = user_found.get_full_name()
        found = True
    except User.DoesNotExist:
        full_name = ""

    user = {
        'full_name': full_name,
        'found': found
    }
    return JsonResponse(user)


@login_required
def pos_map(request):
    """View that is used to set the coordinates to the users"""
    latitude = request.POST.get('lat')
    longitude = request.POST.get('lng')
    coordinates = {
        'latitude' : latitude,
        'longitude' : longitude
    }
    if request.is_ajax():
        userdetails = UserProfile.objects.get(user__username=request.user.username)
        success = Map.objects.filter(id=userdetails.user_id).update(**coordinates) # update the coordinates of the user
        if not success:
            Map.objects.create(**coordinates) # create user entry if the user does not have any coordinates
        map_info = Map.objects.get(id=userdetails.user_id)
        userdetails.location = map_info
        userdetails.save()
    return HttpResponse(json.dumps(coordinates), content_type="application/json")


def all_users(request):
    """Get only the online users from the sessions"""
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []
    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    online_users = User.objects.filter(id__in=uid_list, is_superuser=False)
    all_users_found = User.objects.filter(is_superuser=False)
    users_dict = {}
    users_records = []
    for user in all_users_found:
        if user.username != request.user.username:
            if user in online_users:
                record = {"first_name": user.first_name, "last_name": user.last_name, "username": user.username, "online": "true"}
            else:
                record = {"first_name": user.first_name, "last_name": user.last_name, "username": user.username, "online": "false"}
            users_records.append(record)
    users_dict["users"] = users_records
    return JsonResponse(users_dict)

def notification(request):
    """Notification view used to send messages to the users"""
    message = request.POST.get('message')
    place = request.POST.get('place')
    time = request.POST.get('time')
    username = request.POST.get('username')
    if request.is_ajax():
        recipient = User.objects.get(username=username)
        # send message(message,place,time) to the peer
        notify.send(request.user, recipient=recipient, description='%s | %s' % (place, time), verb=message)
    return HttpResponseRedirect('/')

def readMessage(request):
    """View that sends back the action of the user"""
    message_id = request.POST.get('id')
    action = request.POST.get('action')
    recipient_username = request.POST.get('recipient')
    meeting = request.POST.get('meeting')
    if request.is_ajax():
        message =  Notification.objects.get(id=int(message_id))
        message.mark_as_read() # since there's an action, mark the message as read
        message.save()
        invitation_status = "rejected" # mark invitation rejected until proven otherwise
        if action == "accept":
            invitation_status = "accepted"
        recipient = User.objects.get(username=recipient_username)
        # send alert about your decision to the peer that invited you
        notify.send(request.user, recipient=recipient, description=meeting, verb=invitation_status)
    return HttpResponseRedirect('/')

def dismissAlert(request):
    """Dismiss alert view that marks the alerts as read """
    message_id = request.POST.get('id')
    if request.is_ajax():
        alert =  Notification.objects.get(id=int(message_id))
        alert.mark_as_read()
        alert.save()
    return HttpResponseRedirect('/')
