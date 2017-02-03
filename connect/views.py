from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

from connect.forms import LoginForm, UserForm, UserProfileForm,EditForm,ContactForm

from datetime import datetime
from django.contrib.auth.models import User
from connect.models import UserProfile

@login_required
def index(request):
    request.session.set_test_cookie()
    context_dict = {}

    visitor_cookie_handler(request)

    context_dict['visits'] = request.session['visits']

    response = render(request, 'connect/index.html', context=context_dict)
    return response



def landing(request):
    return render(request, "connect/landing.html")


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
                return render(request, 'connect/index.html',
                              {'login_form': login_form, 'authenticated': authenticated})
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


def contact(request):
    form_class = ContactForm

    return render(request, 'connect/contact.html', {
        'form': form_class,
    })

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

def pos_map(request):
    return HttpResponse(json.dumps({'key': 'value'}), mimetype="application/json")

