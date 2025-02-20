from django.urls import path
from useradmin import views

app_name='useradmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('add_product/', views.add_product_view, name='add_product'),
    path('edit_product/<pid>', views.edit_product_view, name='edit_product'), 
    path('delete_product/', views.delete_product_view, name='delete_product'),
    path('orders/', views.orders_view, name='orders'),
    path('order/<id>', views.order_details_view, name='order_details')
]


