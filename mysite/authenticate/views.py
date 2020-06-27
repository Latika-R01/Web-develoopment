from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm , UserChangeForm, PasswordChangeForm
from .forms import SighUpForm, EditProfileForm, NewEntry
from django.contrib import messages
from .models import Entry

def home(request):
    return render(request, 'authenticate/base.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,('You have been logged in !!'))
            return redirect('home')

        else:
            messages.success(request, ('Error in login - Please try again'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out !'))
    return redirect('home')

def register_user(request):
    if request.method =='POST':
        form = SighUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been successfully registered !'))
            return redirect('home')
    else:
        form = SighUpForm()
    context = {'form': form}

    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
    if request.method =='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You have Edited your profile !'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'authenticate/edit_profile.html',context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You have Changed your password !'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'authenticate/change_password.html', context)


def dear_diary(request):
    entries = Entry.objects.order_by('-date_posted')
    context = {'entries' : entries}
    return render(request, 'authenticate/dear_diary.html', context)

def new_entry(request):
    if request.method == 'POST':
        new_entries = NewEntry(request.POST)
        if new_entries.is_valid():
            new_entries.save()
            return redirect('dear_diary')
    else:
        new_entries = NewEntry()
    context = {'new_entries': new_entries}
    return render(request, 'authenticate/new_entry.html', context)







