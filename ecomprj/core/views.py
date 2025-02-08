from django.http import HttpResponse
from django.shortcuts import render
from core.models import Product,Vendor,Category,ProductImage,ProductReview,CartOrder,CartOrderItems,Wishlist,Address
def index(request):
    # products = Product.objects.all().order_by('-date')
    products = Product.objects.filter(featured=True, product_status='published')
    context={
        'products':products
    }
    return render(request,'core/index.html',context)

def product_list_view(request):
    products = Product.objects.filter(product_status='published')
    context={
        'products':products
    }
    return render(request,'core/product-list.html',context)
# Create your views here.
