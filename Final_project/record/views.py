from django.shortcuts import render,redirect
from django.views import View
from record.form import RegisterForm
from django.contrib.auth import logout,login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form':form
        }
        return render(request, "login.html",context)
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
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
            form.save()
            return redirect('login')
        return redirect('register')
        
class ProductList(View):
    def get(self, request):
        return render(request, "product.html")
    