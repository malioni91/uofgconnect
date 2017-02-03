from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from connect.forms import LoginForm, UserForm, UserProfileForm,EditForm,ContactForm

from datetime import datetime
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        user_form = EditForm(request.POST,  instance=request.user)
        if user_form.is_valid():
            usereditor = user_form.save()
            print "usereditorpassword" , usereditor.password
            print "userdetailspassword", userdetails.password
            print userdetails.check_password(usereditor.password)
            if userdetails.check_password(usereditor.password):
                password1 = usereditor.password
                print "password1" , password1
                print "old", userdetails.password

                username = request.POST.get('username')
                password = request.POST.get('password')
                passwordnew = request.POST.get('new_password')
                print "passwordnew ", passwordnew

                print "old", userdetails.password
                print "passwordform", usereditor.password

                print "pass", usereditor.email
                usereditor.set_password(passwordnew)
                print "new", usereditor.password
                usereditor.save()
                return render(request, 'connect/edit.html', {'user_form': user_form})
            #else:
                #print user_edit.errors
        else:
            print user_edit.errors
    else:
        user_form = EditForm(initial={'name': " ".join([userdetails.first_name, userdetails.last_name]),'username':userdetails.username, 'email':userdetails.email})
        return render(request, 'connect/edit.html', {'user_form': user_form})

    return render(request, 'connect/edit.html')



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
