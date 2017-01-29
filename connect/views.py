from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from connect.forms import LoginForm, UserForm
from datetime import datetime

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
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # Hash the password
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render(request, 'connect/register.html', {'user_form': user_form, 'registered': registered})


def user_login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your UofGConnect account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'connect/login.html', {'login_form': login_form})


def about(request):
    return render(request, 'connect/about.html')

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