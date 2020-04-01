from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout, update_session_auth_hash
from library.models import BookInstance


def register(request):
    message = ''

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm__password']

        if User.objects.filter(username=username).exists():
            message = 'username already exists'
            return render(request, 'users/register.html', {'message': message})

        if password == confirm_password:
            user = User.objects.create_user(username, email, password)
            if user:
                profile = Profile()
                profile.user = user
                is_library_staff = request.POST.get('is_library_staff', False)
                if is_library_staff:
                    profile.is_library_staff = True
                    profile.save()
                else:
                    profile.save()
                return HttpResponseRedirect(reverse('users:login'))
                message = 'profile created!'
        else:
            message = 'passwords did not match'

    return render(request, 'users/register.html', {'message': message})


def login(request):
    message = ''

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            user_profile = Profile.objects.get(user=user)
            is_library_staff = user_profile.is_library_staff
            if is_library_staff:
                return HttpResponseRedirect(reverse('users:staff_profile'))
            else:
                return HttpResponseRedirect(reverse('users:profile'))
        else:
            message = 'wrong username or password'
    return render(request, 'users/login.html', {'message': message})


def logout(request):
    dj_logout(request)
    return render(request, 'users/login.html')


def profile(request):
    owner_books = BookInstance.objects.filter(current_owner=request.user)
    context = {
        'books': owner_books
    }

    return render(request, 'users/profile.html', context)


def change_password(request):
    context = {}
    print(request.user)

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        user = get_object_or_404(User, username=request.user.username)
        if user.check_password(old_password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                context = {'message': 'Password updated successfully '}
                update_session_auth_hash(request, user)
            else:
                context = {'message': 'Passwords did not match'}
        else:
            context = {'message': 'old password is incorrect'}

    return render(request, 'users/change_password.html', context)


def delete_profile(request):
    user = User.objects.get(pk=request.user.pk)
    user.delete()
    return HttpResponseRedirect(reverse('users:register'))


def staff_profile(request):
    all_loaned_books = BookInstance.objects.all()
    context = {
        'books': all_loaned_books
    }
    return render(request, 'users/staff_profile.html', context)

