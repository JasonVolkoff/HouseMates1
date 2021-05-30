import re
from .models import User, Message, Comment
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

################### Login Methods ###################


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validation(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['this_userid'] = new_user.id
        request.session['this_first_name'] = new_user.first_name
        messages.success(request, "You have successfully registered!")
        return redirect('/wall')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['this_userid'] = user.id
    request.session['this_first_name'] = user.first_name
    messages.success(request, "You have successfully logged in!")
    return redirect('/wall')


def logout(request):
    request.session.clear()
    return redirect('/')
