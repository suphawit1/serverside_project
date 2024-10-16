from django.shortcuts import render,redirect
from django.views import View
from authen.form import *
from django.contrib.auth import logout,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash


# Create your views here.
class Login(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form':form
        }
        return render(request, "login.html",context)
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('product-list')
        context = {
            'form': form
        }
        return render(request, "login.html", context)
    
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')

class Register(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            "form": form
        }
        return render(request, "register.html",context)
    
    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(id=request.POST.get("group"))
            user.groups.add(group)
            return redirect('profile')
        context = {
            'form': form
        }
        return render(request, "register.html", context)
    
class Profile(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,request):
        return render(request,"profile.html")
    
class Change_Username_Password(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,request):
        username_form = UsernameChangeForm()
        password_form = NewPasswordForm(request.user)
        context = {
            "user_form":username_form,
            "pass_form":password_form
        }
        return render(request,'change_profile.html',context)
    
    def post(self,request):
        username_form = UsernameChangeForm(request.POST, instance=request.user)
        password_form = NewPasswordForm(request.user, request.POST)

        if username_form.is_valid() and password_form.is_valid():
            username_form.save()

            user = password_form.save()

            update_session_auth_hash(request, user)
            return redirect('profile')
        
        context = {
            "user_form":username_form,
            "pass_form":password_form
        }
        return render(request,'change_profile.html',context)