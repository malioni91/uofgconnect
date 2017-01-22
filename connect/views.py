from django.shortcuts import render, render_to_response
from django.template import RequestContext

from connect.forms import UserForm


def index(request):
    return render(request, "connect/index.html")


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
