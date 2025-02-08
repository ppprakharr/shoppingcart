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

def category_list_view(request):
    categories = Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'core/category-list.html', context)

def category_product_list_view(request,cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status = 'published',category=category)
    context={
        'category':category,
        'products':products
    }
    return render(request,'core/category-product-list.html',context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context={
        'vendors':vendors
    }
    return render (request,'core/vendor-list.html',context)

def vendor_details_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status='published',vendor=vendor)
    context={
        'products':products,
        'vendor':vendor
    }
    return render(request,'core/vendor-details-view.html',context)
# Create your views here.
