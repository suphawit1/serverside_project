from django.urls import path

from product import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="product-list"),
    path("order/", views.SelectSupplierView.as_view(), name="select-supuplier"),
    path("supplier/", views.SupplierAddView.as_view(), name="add-supuplier"),
    path("category/", views.CategoryView.as_view(), name="category"),
    path("addproduct/", views.ProductAddView.as_view(), name="add-product"),
    path("edit/<int:id>/", views.ProductEditView.as_view(), name="edit-product"),
    path("delete/<int:id>/", views.ProductDeleteView.as_view(), name="delete-product"),
]