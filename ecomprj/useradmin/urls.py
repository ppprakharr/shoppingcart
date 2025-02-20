from django.urls import path
from useradmin import views

app_name='useradmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('add_product/', views.add_product_view, name='add_product'),
]


