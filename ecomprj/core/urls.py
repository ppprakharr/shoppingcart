from django.urls import path
from core import views
app_name='core'

urlpatterns=[
    path("",views.index, name="index"),
    path('products/',views.product_list_view,name='product-list'),
    path('category/',views.category_list_view,name='category-list'),
    path('category/<cid>',views.category_product_list_view,name='category_product_list_view'),
    path('vendors/',views.vendor_list_view,name='vendor-list-view'),
    path('vendors/<vid>', views.vendor_details_view,name='vendor-details-page')
]