from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from connect.forms import LoginForm, UserForm

@login_required
def index(request):
    context = RequestContext(request) # Get the context of the user request
    return render(request, "connect/index.html", context)

def landing(request):
    return render(request, "connect/landing.html")


def register(request):
    context = RequestContext(request) # Get the context of the user request
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

    return render_to_response(
        'connect/register.html',
        {'user_form': user_form, 'registered': registered},
        context)

def user_login(request):
    context = RequestContext(request)
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
        return render_to_response(
            'connect/login.html',
            {'login_form': login_form},
            context)
