from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Note
import json


@login_required(redirect_field_name='/login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login')


@login_required
def home(request):
    user_notes = Note.objects.filter(user=request.user)
    if request.method == 'POST':
        note = request.POST.get('note', '')

        if len(note) < 1:
            messages.add_message(request, messages.WARNING, 'Note is too short.')
        else:
            note = Note(data=note, user=request.user)
            note.save()
            messages.add_message(request, messages.SUCCESS, 'Note added!')
    template = loader.get_template('todo/home.html')
    return HttpResponse(template.render({'user_notes': user_notes}, request))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username).exists():
                messages.add_message(request, messages.WARNING, 'Username doesn\'t exist.')
                return HttpResponseRedirect('/login')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Logged in successfully!')
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.WARNING, 'Incorrect password!')
                return HttpResponseRedirect('/login')
        else:
            for err in form.errors:
                for description in form.errors[err]:
                    messages.add_message(request, messages.WARNING, description)
    else:
        form = LoginForm()

    template = loader.get_template('todo/login.html')
    return HttpResponse(template.render({'form': form}, request))


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            if not User.objects.filter(email=email).exists():

                try:
                    user = User.objects.create_user(email=email, username=username, password=password)
                except IntegrityError:
                    messages.add_message(request, messages.WARNING, 'Such name is already exist.')
                    return HttpResponseRedirect('/sign_up')
                user.save()
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Account created!')
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.WARNING, 'Email already exist.')
                return HttpResponseRedirect('/sign_up')
        else:
            for err in form.errors:
                for description in form.errors[err]:
                    messages.add_message(request, messages.WARNING, description)

    else:
        form = RegistrationForm()

    template = loader.get_template('todo/sign_up.html')
    return HttpResponse(template.render({'form': form}, request))


def delete_note(request):
    data = json.loads(request.body)
    note_id = data['noteId']
    note = Note.objects.get(id=note_id)
    if note:
        if note.user == request.user:
            note.delete()
    return HttpResponse(status=200)


