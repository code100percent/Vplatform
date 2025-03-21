from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout


def sign_in_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None :
            request.session.flush()
            login(request, user)
            return redirect('home')
        else:
            return render(request,'User/sign_in.html',{'server_response':'username or password incorrect'})
    isregisted = request.session.get('isregistered','info_not_avaiable')
    if isregisted == 'yes':
        return render(request,'User/sign_in.html',{'server_response':'you have succesfully registered now sign in'})
    return render(request,'User/sign_in.html')
    
def register_page(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists() :
            return render(request,'User/register.html',{'warning':'email already exists'}) 
        if User.objects.filter(username=username).exists():
            return render(request,'User/register.html',{'warning':'username already exists'})

        User.objects.create_user(username,email,password)
        request.session['isregistered'] = 'yes'
        return redirect('sign_in')

    return render(request,'User/register.html')
def logout_user(request):
    logout(request)
    return redirect('home')