from django.shortcuts import render

def sign_in(request):
    return render(request,'User/sign_in.html')
    

def register(request):
    return render(request,'User/register.html')
