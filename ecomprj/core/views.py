from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.functions import ExtractMonth
from taggit.models import Tag
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.core import serializers
from core.forms import ProductReviewForm
import calendar
from userauths.models import Profile
from core.models import Product,Vendor,Category,Coupons,ProductImage,ProductReview,CartOrder,CartOrderItems,Wishlist,Address
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
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    products = Product.objects.filter(product_status='published').order_by('-id').distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories)>0:
        products = products.filter(category__id__in = categories).distinct()
    if len(vendors)>0:
        vendors = products.filter(vendor__id__in = vendors).distinct()

    data = render_to_string('core/async/product-list.html',{'products':products})
    return JsonResponse({
        'data':data
    })

def add_cart_view(request):
    cart_product={}
    cart_product[str(request.GET['id'])]={
        'title':request.GET['title'],
        'quantity':request.GET['quantity'],
        'price':request.GET['price'],
        'pid':request.GET['pid'],
        'image': request.GET['image']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity']+=int(cart_product[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj']=cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({
        'data':request.session['cart_data_obj'],
        'totalcartitems':len(request.session['cart_data_obj'])
    })

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+= int(item['quantity'])*float(item['price'])
        return render(request,'core/cart.html',{'cart_data':request.session['cart_data_obj'],
        'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    else:
       messages.warning(request,'Your cart is empty')
       return redirect('core:index')
    

def delete_product_from_cart(request):
    product_id=str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data  = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+= int(item['quantity'])*float(item['price'])
        
    context = render_to_string('core/async/cart-list.html',{'cart_data':request.session['cart_data_obj'],
        'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({'data':context,'totalcartitems':len(request.session['cart_data_obj'])})

def update_from_cart(request):
    product_id=str(request.GET['id'])
    product_quantity = request.GET['quantity']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data  = request.session['cart_data_obj']
            cart_data[product_id]['quantity']=product_quantity
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+= int(item['quantity'])*float(item['price'])
        
    context = render_to_string('core/async/cart-list.html',{'cart_data':request.session['cart_data_obj'],
        'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({'data':context,'totalcartitems':len(request.session['cart_data_obj'])})

def save_checkout_info_view(request):
    cart_total_amount = 0
    total_amount=0
    if request.method=='POST':
        full_name = request.POST['full_name']
        email=request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        request.session['full_name']=full_name
        request.session['email']=email
        request.session['mobile']=mobile
        request.session['address']=address
        request.session['city']=city
        request.session['state']=state
        request.session['country']=country

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount+= int(item['quantity'])*float(item['price'])
        order = CartOrder.objects.create(
            user=request.user,
            full_name=request.session['full_name'],
            email=request.session['email'],
            mobile=request.session['mobile'],
            address=request.session['address'],
            city=request.session['city'],
            state=request.session['state'],
            country=request.session['country'],
            price=total_amount
        )    

        del request.session['full_name']
        del request.session['email']
        del request.session['mobile']
        del request.session['address']  
        del request.session['city']
        del request.session['state']
        del request.session['country']
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+= int(item['quantity'])*float(item['price'])

            cart_order_items = CartOrderItems.objects.create(
                order=order,
                invoice_no= 'INVOICE_NO_'+str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['quantity'],
                price=item['price'],
                total=int(item['quantity'])*float(item['price'])
            )
        return redirect('core:checkout',order.oid)
    return redirect('core:checkout',order.oid)

def checkout_view(request,oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    if request.method=='POST':
        code=request.POST['code']
        coupon = Coupons.objects.filter(code=code).first()

        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request,'Coupon already applied')
                return redirect('core:checkout',order.oid)
            else:
                messages.success(request,'Coupon applied successfully')
                discount=order.price * coupon.discount/100
                order.price-=discount
                order.saved+=discount
                order.save()
                order.coupons.add(coupon)
                return redirect('core:checkout',order.oid)
        else:
            messages.warning(request,'Invalid coupon code')
            return redirect('core:checkout',order.oid)

    context={
        'order_items':order_items,
        'order':order
    }
    return render(request,'core/checkout.html',context)
    



@login_required  
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['quantity'])*float(item['price'])

        return render(request, 'core/payment-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})

@login_required
def payment_failed_view(request):
    return render(request,'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    orders  = CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth('order_date')).values('month').annotate(total=Count('id')).values('month','total')
    month=[]
    item_count=[]

    for o in orders:
        month.append(calendar.month_name[o['month']])
        item_count.append(o['total'])
        

    address = Address.objects.filter(user=request.user)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        address = request.POST['address']
        mobile  = request.POST['phone']
        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile
        )
        messages.success(request,'Address added successfully')
        return redirect('core:dashboard')
    context={
        'orders_list': orders_list,
        'address': address,
        'user_profile':user_profile,
        'month':month,
        'item_count':item_count
    }

        
    return render(request,'core/customer-dashboard.html',context)

@login_required
def order_details_view(request, id):
    order=CartOrder.objects.get(user=request.user, id=id)
    product =CartOrderItems.objects.filter(order=order)
    context={
        'order_items':product
    }
    return render(request,'core/order-details.html',context)

def make_address_default(request):
    id=request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({
        'boolean':True
    })

@login_required
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.all()
    except:
        wishlist=None
    context={
        'wishlist':wishlist
    }
    return render(request,'core/wishlist.html',context)

def add_to_wishlist(request):
    product_id=request.GET['id']
    product = Product.objects.get(id=product_id)
    context={}
    wishlist_count = Wishlist.objects.filter(user=request.user,product=product).count()

    if wishlist_count>0:
        context={
            'bool':True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user=request.user,
            product=product
        )
        context={
            'bool':True
        }
    return JsonResponse(
        context
    )


@login_required
def remove_from_wishlist_view(request):
    product_id=request.GET['id']
    product = Product.objects.get(id=product_id)
    wishlist=Wishlist.objects.filter(user=request.user)
    Wishlist.objects.filter(user=request.user,product=product).delete()
    context={
        'bool':True,
        'wishlist':wishlist
        }
    json_wishlist = serializers.serialize('json',wishlist)

    # wishlist = Wishlist.objects.filter(user=request.user,product=product)
    data=render_to_string('core/async/wishlist.html',context)
    return JsonResponse({'data':data,'object':json_wishlist,'bool':True})


    


# Create your views here.
