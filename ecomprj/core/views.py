from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag
from django.template.loader import render_to_string
from core.forms import ProductReviewForm
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

def product_details_view(request,pid):
    product = Product.objects.get(pid=pid)
    product_images = product.p_image.all()
    make_review=True

    if request.user.is_authenticated:
        review_count = ProductReview.objects.filter(product=product,user=request.user).count()
        if review_count > 0:
            make_review = False
    products  = Product.objects.filter(category = product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    #getting average rating
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    ratings_form = ProductReviewForm()
    context = {
        'product':product,
        'make_review': make_review,
        'product_images':product_images,
        'ratings_form':ratings_form,
        'average_rating':average_rating,
        'related_products':products,
        'reviews':reviews

    }
    return render(request,'core/product-details-page.html',context)

def tag_list(request,tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')
    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context={
        'products':products,
        'tags':tag
    }
    return render(request,'core/tags.html',context)

def ajax_add_review(request,pid):
    product  = Product.objects.get(pid=pid)
    user=request.user
    review = ProductReview.objects.create(
        user=user,
        product= product,
        review = request.POST['review'],
        rating=request.POST['rating']
    )
    context={
        'user':user.username,
        'review': request.POST['review'],
        'rating':request.POST['rating']
    }

    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool':True,
            'context':context,
            'average_rating':average_rating
        }
    )

def search_view(request):
    query = request.GET['q']
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    context={
        'products':products,
        'query':query
    }
    return render(request,'core/search.html',context)

def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    products = Product.objects.filter(product_status='published').order_by('-id').distinct()

    if len(categories)>0:
        products = products.filter(category__id__in = categories).distinct()
    if len(vendors)>0:
        vendors = products.filter(vendor__id__in = vendors).distinct()

    data = render_to_string('core/async/product-list.html',{'products':products})
    return JsonResponse({
        'data':data
    })


# Create your views here.
