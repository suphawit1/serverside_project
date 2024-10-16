from django.forms import ModelForm
from django import forms
from product.models import *

from record.models import *

class SelectSupplier(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supplier"].widget.attrs.update({"class": "form-select"})
        self.fields['supplier'].empty_label = "--- เลือกผู้จัดจำหน่าย ---"
    
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())

class AddCategory(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ชื่อหมวดหมู่สินค้า'
                }),
        }
        labels = {
            'name': 'ชื่อหมวดหมู่สินค้า',
        }

class AddSupplier(ModelForm):

    class Meta:
        model = Supplier
        fields = [
            'name',
            'contact',
            'address',
            ]
        
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ใส่ชื่อผู้จัดจำหน่าย'
                }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'เบอร์ติดต่อ'
                }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ที่อยู่',
                }),
            }
        labels = {
            'name': 'ชื่อผู้จัดจำหน่าย',
            'contact': 'เบอร์ติดต่อ',
            'address': 'ที่อยู่'
        }
        
    
class AddProduct(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-select",'multiple':"multiple",'id':"categories"})

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'quantity',
            'category',
            'image'
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ใส่ชื่อสินค้า'
                }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ใส่ราคาตั้งต้น',
                'type':'number'
                }),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Initial quantity',
                'type':'number'
                }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'ชื่อสินค้า',
            'price': 'ราคา',
            'quantity': 'จำนวนสินค้า',
            'image': 'รูปภาพ',
            'category': 'หมวดหมู่สินค้า'
        }


    