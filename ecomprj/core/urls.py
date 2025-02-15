from django.urls import path
from core import views
app_name='core'

urlpatterns=[
    path("",views.index, name="index"),
    path('products/',views.product_list_view,name='product-list'),
    path('product/<pid>',views.product_details_view,name='product-details-page'),
    path('category/',views.category_list_view,name='category-list'),
    path('category/<cid>',views.category_product_list_view,name='category_product_list_view'),
    path('vendors/',views.vendor_list_view,name='vendor-list-view'),
    path('vendors/<vid>', views.vendor_details_view,name='vendor-details-page'),
    path('products/tag/<tag_slug>/',views.tag_list,name='tags'),
    path('ajax-add-review/<pid>',views.ajax_add_review,name='ajax-add-review'),
    path('search/',views.search_view,name='search'),
    path('filter-products/',views.filter_product,name='filter-product'),
    path('add-to-cart/',views.add_cart_view,name='add-to-cart'),
    path('cart/',views.cart_view,name='cart'),
    path('delete-from-cart/',views.delete_product_from_cart,name='delete-from-cart'),
    path('update-cart/',views.update_from_cart,name='update-from-cart'),
    path('checkout/',views.checkout_view,name='checkout')
]