from django.shortcuts import render,redirect
from django.views import View
from record.form import *
from django.forms import modelformset_factory
from django.db import transaction
from django.db.models import Sum,F,Value


# Create your views here.
class RecordView(View):
    def get(self,request):
        records = Transaction.objects.prefetch_related('purchaseorders__purchaseorders_detail_set', 'sellorder__sellorder_detail_set')
        transactions_data = []
        group = False
        if 'group_products' in request.GET:
            group = True
        
        if "All_button" in request.GET:
            type = "all"
        elif "Buy_button" in request.GET:
            type = "buy"
        elif "Sell_button" in request.GET:
            type = "sell"
        else:
            if 'type' in request.GET:
                type = request.GET.get('type')
            else:
                type = 'all'
        if type != "all":
            records = records.filter(transaction_type=type)

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        if start_date != '' and end_date != '':
            records = records.filter(transaction_date__range=[start_date, end_date])
        
        if group == True:
            purchase_orders_grouped = (
                PurchaseOrders_detail.objects
                .values('product__name')
                .annotate(
                    quantity=Sum('quantity'),
                    total_cost=Sum('total_cost'),
                    type=Value('buy', output_field=models.CharField())
                )
            )
            sell_orders_grouped = (
                SellOrder_detail.objects
                .values('product__name')
                .annotate(
                    quantity=Sum('quantity'),
                    total_cost=Sum('total_cost'),
                    type=Value('sell', output_field=models.CharField())
                )
            )
            if type == 'buy':
                transactions_data = list(purchase_orders_grouped)
            elif type == 'sell':
                transactions_data = list(sell_orders_grouped)
            else:
                transactions_data = list(purchase_orders_grouped) + list(sell_orders_grouped)
            print(transactions_data)
        else:
            for rec in records:
                if rec.transaction_type == 'buy':
                    details = rec.purchaseorders.purchaseorders_detail_set.all()
                    for detail in details:
                        transactions_data.append({
                            'date': rec.transaction_date,
                            'product__name': detail.product.name,
                            'quantity': detail.quantity,
                            'total_cost': detail.unit_cost * detail.quantity,
                            'type': 'buy'
                        })
                elif rec.transaction_type == 'sell':
                    details = rec.sellorder.sellorder_detail_set.all()
                    for detail in details:
                        transactions_data.append({
                            'date': rec.transaction_date,
                            'product__name': detail.product.name,
                            'quantity': detail.quantity,
                            'total_cost': detail.unit_cost * detail.quantity,
                            'type': 'sell'
                        })

        sort = request.GET.get('sort_by')
        sort_order = request.GET.get('sort_order')

        if sort == 'date' and group!= True:
            if sort_order == 'asc':
                transactions_data.sort(key=lambda x: x['date'])
            else:
                transactions_data.sort(key=lambda x: x['date'],reverse=True)
        elif sort == 'amount':
            if sort_order == 'asc':
                transactions_data.sort(key=lambda x: x['quantity'])
            else:
                transactions_data.sort(key=lambda x: x['quantity'],reverse=True)
        elif sort == 'name':
            if sort_order == 'asc':
                transactions_data.sort(key=lambda x: x['product__name'])
            else:
                transactions_data.sort(key=lambda x: x['product__name'],reverse=True)
        elif sort == 'cost':
            if sort_order == 'asc':
                transactions_data.sort(key=lambda x: x['total_cost'])
            else:
                transactions_data.sort(key=lambda x: x['total_cost'],reverse=True)
        if request.GET:
            form = FilterForm(request.GET)
        else:
            form = FilterForm()

        total_profit = sum(item['total_cost'] if item['type'] == 'sell' else -item['total_cost'] for item in transactions_data)

        context = {
            'profit':total_profit,
            'transactions':transactions_data,
            'type':type,
            'form':form
        }
        return render(request,'record.html',context)

class SelectProductSell(View):
    def get(self,request):
        
        query = request.GET
        product = Product.objects.all().order_by('id')
        if query.get("search"):
            product = product.filter(
                name__icontains=query.get("search")
            )

        context = {
            "product":product
        }
        return render(request,'sell_select_order.html',context)
class OrderProductView(View):
    def get(self, request):
        ProductFormSet = modelformset_factory(PurchaseOrders_detail, form=OrderProduct,extra=1)
        formset = ProductFormSet(queryset=PurchaseOrders_detail.objects.none())
        supplier = request.GET.get('supplier')
        sup = Supplier.objects.get(pk=supplier)
        context = {
            'sup':sup,
            'formset':formset
        }
        return render(request,"purchaseOrders.html",context)
    
    @transaction.atomic
    def post(self, request):

        ProductFormSet = modelformset_factory(PurchaseOrders_detail, form=OrderProduct, extra=0)
        formset = ProductFormSet(request.POST)

        supplier = request.GET.get('supplier')
        sup = Supplier.objects.get(pk=supplier)

        context = {
            'sup': sup,
            'formset': formset,
        }
        if "order" in request.POST:
            if formset.is_valid():
                po = PurchaseOrders(
                    supplier=sup,
                    total_cost= request.POST.get('total_price')
                                    )
                po.save()
                transactions = Transaction(
                    purchaseorders = po,
                    transaction_type = 'buy',
                    total_amount = request.POST.get('total_price'),
                )
                transactions.save()

                for form in formset:
                    if form.is_valid():
                        form.instance.purchaseorders = po
                        quantity = form.cleaned_data.get('quantity')
                        product = form.cleaned_data.get('product')
                        product.quantity = product.quantity + quantity
                        product.save()
                formset.save()

                return redirect('product-list')
            
            return render(request,"purchaseOrders.html",context)


        # Check if 'add_product' button was pressed
        elif "add_product" in request.POST:
            current_forms_count = len(formset.forms)
            
            ProductFormSet = modelformset_factory(PurchaseOrders_detail, form=OrderProduct, extra=current_forms_count+1)
            new_formset = ProductFormSet(queryset=PurchaseOrders_detail.objects.none())
            
            for i in range(current_forms_count):
                for field in formset.forms[i].visible_fields():
                    new_formset.forms[i].fields[field.name].initial = field.value()

            context = {
                'sup': sup,
                'formset': new_formset
            }

        elif "delete_product" in request.POST:
            current_forms_count = len(formset.forms)
            
            ProductFormSet = modelformset_factory(PurchaseOrders_detail, form=OrderProduct, extra=current_forms_count-1)
            new_formset = ProductFormSet(queryset=PurchaseOrders_detail.objects.none())
            
            for i in range(current_forms_count-1):
                for field in formset.forms[i].visible_fields(): 
                    new_formset.forms[i].fields[field.name].initial = field.value()

            context = {
                'sup': sup,
                'formset': new_formset
            }

        return render(request, "purchaseOrders.html", context)
    
class SellOrderView(View):
    def get(self, request):
        selected_products = request.GET.getlist('products[]')
        product = Product.objects.filter(id__in=selected_products)

        ProductFormSet = modelformset_factory(SellOrder_detail, form=SellProduct,extra=product.count())
        formset = ProductFormSet(queryset=SellOrder_detail.objects.none())

        for i in range(product.count()):
            formset.forms[i].fields['product'].initial = product[i]
            formset.forms[i].fields['unit_cost'].initial = product[i].price
        context = {
            'formset':formset
        }
        return render(request,"sellOrders.html",context)
    
    @transaction.atomic
    def post(self, request):

        ProductFormSet = modelformset_factory(SellOrder_detail, form=SellProduct, extra=0)
        formset = ProductFormSet(request.POST)

        context = {
            'formset': formset,
        }
        if "order" in request.POST:
            if formset.is_valid():
                so = SellOrder(
                    total_cost= request.POST.get('total_price')
                                    )
                so.save()
                transactions = Transaction(
                    sellorder = so,
                    transaction_type = 'sell',
                    total_amount = request.POST.get('total_price'),
                )
                transactions.save()

                sells = SellOrder_detail.objects.filter(sellorder=so)
                for buy in sells:
                    product = buy.product
                    product.quantity = product.quantity - buy.quantity
                    product.save()

                for form in formset:
                    if form.is_valid():
                        form.instance.sellorder = so
                        quantity = form.cleaned_data.get('quantity')
                        product = form.cleaned_data.get('product')
                        if product.quantity >= quantity:
                            product.quantity -= quantity
                            product.save()
                        else:
                            quantitys = product.quantity
                            error_message = f"ไม่สามารถลดจำนวนสินค้าได้ เนื่องจากจำนวนสินค้าที่มีน้อยเกินไป มีอยู่ {quantitys} ชิ้น"
                            form.add_error('quantity', error_message)
                            return render(request,"sellOrders.html",context)

                formset.save()
                
                return redirect('productsell')
            
            return render(request,"sellOrders.html",context)


        # Check if 'add_product' button was pressed
        elif "add_product" in request.POST:
            current_forms_count = len(formset.forms)
            
            ProductFormSet = modelformset_factory(SellOrder_detail, form=SellProduct, extra=current_forms_count+1)
            new_formset = ProductFormSet(queryset=PurchaseOrders_detail.objects.none())
            
            for i in range(current_forms_count):
                for field in formset.forms[i].visible_fields():
                    new_formset.forms[i].fields[field.name].initial = field.value()

            context = {
                'formset': new_formset
            }

        elif "delete_product" in request.POST:
            current_forms_count = len(formset.forms)
            
            ProductFormSet = modelformset_factory(SellOrder_detail, form=SellProduct, extra=current_forms_count-1)
            new_formset = ProductFormSet(queryset=SellOrder_detail.objects.none())
            
            for i in range(current_forms_count-1):
                for field in formset.forms[i].visible_fields(): 
                    new_formset.forms[i].fields[field.name].initial = field.value()

            context = {
                'formset': new_formset
            }

        return render(request, "sellOrders.html", context)