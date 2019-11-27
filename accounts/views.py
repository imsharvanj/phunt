from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        # User has info and want an account now
        if request.POST['password1']==request.POST['password2']:
            try:
                user1 = User.objects.get(username=request.POST['username'])
                user2 = User.objects.get(email=request.POST['email'])
                if(user1.username == user2.username):
                    return render(request, 'accounts/login.html', {'error':'you are already a member. Please login.'})
                else:
                    return render(request, 'accounts/signup.html', {'error':'Username and Email already has been taken by different users.'})
            except User.DoesNotExist:
                try:
                    user = User.objects.create_user(username=request.POST['username'], \
                    password=request.POST['password1'], first_name=request.POST['first_name'], \
                    last_name=request.POST['last_name'], email=request.POST['email'])
                    return redirect('home')
                except Exception as e:
                    return render(request, 'accounts/signup.html', {'error': 'Username or Email already has been taken.'})
            except Exception as e:
                return render(request, 'accounts/signup.html', {'error': 'Username already has been taken.'})
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match.'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        usernameoremail = request.POST['usernameoremail'].lower()
        uname = User.objects.get(email=usernameoremail).username if '@' in usernameoremail else usernameoremail
        user = auth.authenticate(username=uname, password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or Password not correct.'})
    else:
        return render(request, 'accounts/login.html')

@login_required
def logout(request):
    # TODO Need to route to home page and logout :)
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

@login_required
def userdetails(request):
    if request.method == 'POST':
        if request.POST['password1']==request.POST['password2']:
            hunter = request.user
            hunter.first_name = request.POST['first_name']
            hunter.last_name = request.POST['last_name']
            hunter.set_password(request.POST['password1'])
            try:
                if hunter.email != request.POST['email']:
                    hunter.email = request.POST['email']
                user1 = User.objects.get(username=request.POST['username'])
                if hunter.username == user1.username:
                    hunter.save()
                    return redirect('home')
                else:
                    return render(request, 'accounts/userdetails.html', {'error': 'Username already taken.'})
            except User.DoesNotExist:
                hunter.username = request.POST['username']
                hunter.save()
                return redirect('home')
            except Exception as e:
                return render(request, 'accounts/userdetails.html', {'error': 'Username or Email already taken.'})
        else:
            return render(request, 'accounts/userdetails.html', {'error': 'Passwords must match.'})
    else:
        hunter = request.user
        return render(request, 'accounts/userdetails.html', {'hunter': hunter})

def changepassword(request):
    return render(request, 'accounts/changepassword.html')
