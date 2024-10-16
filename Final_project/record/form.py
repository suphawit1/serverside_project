from django.forms import ModelForm
from django import forms
from record.models import *
from product.models import *
from django.core.exceptions import ValidationError

class OrderProduct(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),widget=forms.Select(attrs={'class': 'form-control js-states product-select'}),required=True)
    class Meta:
        model = PurchaseOrders_detail
        fields = [
            'product',
            'quantity',
            'unit_cost',
            ]
        widgets = {
            'quantity': forms.TextInput(attrs={
                'class': 'form-control product_quantity',
                'placeholder': 'ระบุจำนวนสินค้า',
                'type':'number'
                }),
            'unit_cost': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ระบุราคาต่อชิ้น',
                'type':'number'
                }),
        }
        labels = {
            'product': 'ชื่อสินค้า',
            'quantity': 'จำนวนสินค้า',
            'unit_cost': 'ราคาต่อชิ้น'
        }
        
    def clean_product(self):
        product = self.cleaned_data.get('product')
        print(f"Product in clean_product: {product}")
        if product is None:
            raise ValidationError("โปรดเลือกสินค้า")
        return product
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            raise ValidationError("โปรดระบุจำนวนสินค้า")
        elif quantity <= 0:
            raise ValidationError("จำนวนสินค้าต้องมีค่ามากกว่า 0")
        return quantity
    def clean_unit_cost(self):
        unit_cost = self.cleaned_data.get('unit_cost')
        if unit_cost is None:
            raise ValidationError("โปรดระบุราคาต่อหน่วย")
        elif unit_cost < 0:
            raise ValidationError("ราคาต่อหน่วยไม่สามารถเป็นค่าลบได้")
        return unit_cost
        

class SellProduct(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),widget=forms.Select(attrs={'class': 'form-control js-states product-select',}))
    class Meta:
        model = SellOrder_detail
        fields = [
            'product',
            'quantity',
            'unit_cost',
            ]
        widgets = {
            'quantity': forms.TextInput(attrs={
                'class': 'form-control product_quantity',
                'placeholder': 'ระบุจำนวนสินค้า',
                'type':'number'
                }),
            'unit_cost': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ระบุราคาต่อชิ้น',
                'type':'number'
                }),
        }
        labels = {
            'product': 'ชื่อสินค้า',
            'quantity': 'จำนวนสินค้า',
            'unit_cost': 'ราคาต่อชิ้น'
        }

    def clean_product(self):
        product = self.cleaned_data.get('product')

        if not product:
            raise ValidationError("โปรดเลือกสินค้า")
        return product
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if not quantity:
            raise ValidationError("โปรดระบุจำนวนสินค้า")
        elif quantity <= 0:
            raise ValidationError("จำนวนสินค้าต้องมีค่ามากกว่า 0")
        return quantity
    def clean_unit_cost(self):
        unit_cost = self.cleaned_data.get('unit_cost')
        if not unit_cost:
            raise ValidationError("โปรดระบุราคาต่อหน่วย")
        elif unit_cost < 0:
            raise ValidationError("ราคาต่อหน่วยไม่สามารถเป็นค่าลบได้")
        return unit_cost

class FilterForm(forms.Form):
    SORT_FIELDS = [
        ('date', 'เวลา'),
        ('amount', 'จำนวนสินค้า'),
        ('name','ชื่อสินค้า'),
        ('cost','ราคารวม')
    ]

    SORT_ORDER = [
        ('asc', 'จากน้อยไปมาก'),
        ('desc', 'จากมากไปน้อย'),
    ]
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
        label="ตั้งแต่"
        )
    end_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
        label="ถึง"
        )
    sort_by = forms.ChoiceField(
        choices=SORT_FIELDS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="เรียงลำดับตาม"
        )
    sort_order = forms.ChoiceField(
        choices=SORT_ORDER, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="เรียงลำดับตาม"
        )
    group_products = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input form-control'}),
        label="รวมกลุ่มสินค้า"
    )
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise ValidationError('วันสิ้นสุดต้องไม่อยู่ก่อนวันเริ่มต้น')
        
        return cleaned_data
    