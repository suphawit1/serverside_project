from django.shortcuts import redirect, render
from django.views import View
from product.form import *
from django.forms import modelformset_factory
from django.db import transaction

# Create your views here.
class ProductList(View):
    def get(self, request):
        query = request.GET
        product = Product.objects.all().order_by('id')

        if query.get("search"):
            product = product.filter(
                name__icontains=query.get("search")
            )

        context = {
            "product":product
        }
        return render(request, "product.html",context)
    
class SelectSupplierView(View):
    def get(self, request):
        form = SelectSupplier()
        context = {
            'form':form
        }
        return render(request,"order_supplier.html",context)
    
class SupplierAddView(View):
    def get(self, request):
        form = AddSupplier()
        context = {
            'form':form
        }
        return render(request,"add_supplier.html",context)
    def post(self, request):
        form = AddSupplier(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-order')
        context = {
            'form': form
        }
        return render(request, "add_supplier.html", context)

class CategoryView(View):
    def get(self, request):
        form = AddCategory()
        context = {
            'form':form
        }
        return render(request,"category.html",context)
    def post(self, request):
        form = AddCategory(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
        context = {
            'form': form
        }
        return render(request, "category.html", context)
    
class ProductAddView(View):
    def get(self, request):
        form = AddProduct()
        context = {
            'form':form
        }
        return render(request,"add_product.html",context)
    def post(self, request):
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')
        context = {
            'form': form
        }
        return render(request, "add_product.html", context)
    
class ProductEditView(View):

    def get(self,request,id):
        product = Product.objects.get(pk=id)
        form = AddProduct(instance=product)
        context = {
            'form':form
        }
        return render(request,"edit_product.html",context)
    
    def post(self,request,id):
        product = Product.objects.get(pk=id)
        form = AddProduct(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
        context = {
            'form': form
        }
        return render(request, "edit_product.html", context)
    
class ProductDeleteView(View):
    def get(self,request,id):
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('product-list')

