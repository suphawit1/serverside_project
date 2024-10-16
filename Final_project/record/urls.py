from django.urls import path

from record import views

urlpatterns = [
    path("",views.RecordView.as_view(), name="record"),
    path("purchaseorders/", views.OrderProductView.as_view(), name="product-order"),
    path("sellorders/", views.SellOrderView.as_view(), name="product-sell"),
    path("productsell/", views.SelectProductSell.as_view(), name="productsell"),
]