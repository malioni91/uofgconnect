from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json, feedparser
from django.views.decorators.csrf import ensure_csrf_cookie

from connect.forms import LoginForm, UserForm, UserProfileForm,EditForm

from datetime import datetime
from django.contrib.auth.models import User
from connect.models import UserProfile

from django.http import JsonResponse
from django.core.cache import cache
from django.http import JsonResponse

from django.contrib.sessions.models import Session
from django.utils import timezone

from .models import UserProfile, Map

@login_required
def index(request):
    request.session.set_test_cookie()
    #user_coordinates = UserProfile.objects.all().exclude(user=request.user)
    feeds = feedparser.parse('http://www.gla.ac.uk/rss/news/index.xml')

    # Get online users
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    online_users = User.objects.filter(id__in=uid_list)
    context_dict = {}


    for user_o in online_users:
        user_coordinates = UserProfile.objects.filter(user=user_o).exclude(user=request.user)
        context_dict = {'coordinates': user_coordinates, 'feeds': feeds}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'connect/index.html', context=context_dict)
    return response


def landing(request):
    feeds = feedparser.parse('http://www.gla.ac.uk/rss/news/index.xml')
    context_dict = {'feeds': feeds}
    return render(request, "connect/landing.html", context=context_dict)


def register(request):
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
    authenticated = False
    login_form = LoginForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                authenticated = True
                # return render(request, 'connect/index.html',
                #               {'login_form': login_form, 'authenticated': authenticated})
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
    return render(request, 'connect/about.html')


def faq(request):
    return render(request, 'connect/faq.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/connect/')


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                                str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
# If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits

@login_required
def user_edit(request):
    userdetails = User.objects.get(username=request.user.username)
    usercourse = UserProfile.objects.get(user=request.user)
    #print usercourse.course
    user_form = EditForm(request.POST,  instance=request.user)
    profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            print '***********1',user_form
            usereditor = user_form.save(commit=False)
            if userdetails.check_password(usereditor.password):
                print 'password should be correct *********************************'
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

                print 'worng password *******************'
                #user_formpassword=userdetails.password
                print 'password:', userdetails.password
                user_form = EditForm(initial={'name': " ".join([userdetails.first_name, userdetails.last_name]),'username':userdetails.username, 'email':userdetails.email})
                profile_form = UserProfileForm(initial={'course' : usercourse.course})
                print(user_form.errors, profile_form.errors)
                return render(request, 'connect/edit.html', {'user_form': user_form , 'profile_form': profile_form})
                print 'paqss0',password

                #print 'passs1',user_formpassword
                #usereditor.set_password(passwordnew)
                #usereditor.save()
        else:
            #form not valid
            print 'form not valid'
            print(user_form.errors, profile_form.errors)
    else:
        user_form = EditForm(initial={'name': " ".join([userdetails.first_name, userdetails.last_name]),'username':userdetails.username, 'email':userdetails.email})
        profile_form = UserProfileForm(initial={'course' : usercourse.course})
        return render(request, 'connect/edit.html', {'user_form': user_form , 'profile_form': profile_form})
        print 'paqss0',password

    #user_formpassword=userdetails.password
    #print 'passs1',user_formpassword

    return render(request, 'connect/edit.html', {'user_form': user_form , 'profile_form': profile_form})



 # A helper method
def get_server_side_cookie(request, cookie, default_val=None):
     val = request.session.get(cookie)
     if not val:
         val = default_val
     return val

 # Updated the function definition
def visitor_cookie_handler(request):
     visits = int(get_server_side_cookie(request, 'visits', '1'))
     last_visit_cookie = get_server_side_cookie(request,
                                                'last_visit',
                                                 str(datetime.now()))

     last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                         '%Y-%m-%d %H:%M:%S')
 # If it's been more than a day since the last visit...
     if (datetime.now() - last_visit_time).days > 0:
         visits = visits + 1
         #update the last visit cookie now that we have updated the count
         request.session['last_visit'] = str(datetime.now())
     else:
         visits = 1
         # set the last visit cookie
         request.session['last_visit'] = last_visit_cookie

     # Update/set the visits cookie
     request.session['visits'] = visits


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
    latitude = request.POST.get('lat')
    longitude = request.POST.get('lng')
    coordinates = {
        'latitude' : latitude,
        'longitude' : longitude
    }
    if request.is_ajax():
        userdetails = UserProfile.objects.get(user__username=request.user.username)
        success = Map.objects.filter(id=userdetails.user_id).update(**coordinates)
        if not success:
            Map.objects.create(**coordinates)
        map_info = Map.objects.get(id=userdetails.user_id)
        userdetails.location = map_info
        userdetails.save()

    return HttpResponse(json.dumps(coordinates), content_type="application/json")


def all_users(request):
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    online_users = User.objects.filter(id__in=uid_list)
    all_users_found = User.objects.all()
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
    print "Hello"
    # Just for testing - remove
    response = render(request, 'connect/index.html')
    return response
