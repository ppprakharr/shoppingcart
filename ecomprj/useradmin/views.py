from django.shortcuts import render, redirect
from userauths.models import User, Profile
from core.models import Category, CartOrder, Product, CartOrderItems,Vendor,ProductReview
from django.db.models import Sum
from useradmin.forms import AddProductForm
import datetime
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from useradmin.decorators import admin_required

@admin_required
def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum('price'))
    total_orders_count = CartOrder.objects.count()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customer = User.objects.all().order_by('-id')
    latest_orders = CartOrder.objects.all().order_by('-id')
    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum('price'))

    context={
        'revenue':revenue,
        'total_orders_count':total_orders_count,
        'all_products':all_products,
        'all_categories':all_categories,
        'new_customer':new_customer,
        'latest_orders':latest_orders,
        'monthly_revenue':monthly_revenue
    }
    return render(request,'useradmin/dashboard.html',context)

@admin_required
def products(request):
    products = Product.objects.all()
    category=Category.objects.all()

    context={
        'products':products,
        'category':category
    }

    return render(request,'useradmin/products.html',context)

@admin_required
def add_product_view(request):
    if request.method=='POST':
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user=request.user
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:products')
    else:
        form=AddProductForm()
    context={'form':form}
    return render(request,'useradmin/add-product.html',context)


@admin_required
def edit_product_view(request,pid):
    product = Product.objects.get(pid=pid)
    if request.method=='POST':
        form = AddProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user=request.user
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:products')
    else:
        form=AddProductForm(instance=product)
    context={
             'product':product,
             'form':form}
    return render(request,'useradmin/edit-product.html',context)

@admin_required
def delete_product_view(request):
    id=request.GET['id']
    product = Product.objects.get(id=id)
    product.delete()
    products  = Product.objects.all()
    context={
        'products':products,
        'bool':True}
    
    data = render_to_string('useradmin/async/products.html',context)
    

    return JsonResponse({'data':data})


@admin_required
def orders_view(request):
    orders = CartOrder.objects.all()
    context={
        'orders':orders
                }
    return render(request,'useradmin/orders.html',context)


@admin_required
def order_details_view(request,id):
    order=CartOrder.objects.get(id=id)
    cart_order = CartOrderItems.objects.filter(order=order)
    context={
        'order':order,
        'cart_order':cart_order
        }
    
    return render(request,'useradmin/order-details.html',context)


@admin_required
def change_order_status_view(request,oid):
    if request.method=='POST':
        status = request.POST['status']
        order=CartOrder.objects.get(oid=oid)
        order.product_status = status
        order.save()
        messages.success(request,'Order status changed successfully')
        return redirect('useradmin:order_details',id=order.id)
    

@admin_required  
def vendor_page_view(request):
    vendor = Vendor.objects.filter(user=request.user).first()
    total_revenue=CartOrderItems.objects.filter(vendor=vendor,order__paid_status=True).aggregate(total=Sum('total'))
    total_orders = CartOrderItems.objects.filter(vendor=vendor).aggregate(sales=Sum('qty'))
    products = Product.objects.filter(vendor=vendor,status=True)
    context={
        'vendor':vendor,
        'total_revenue':total_revenue,
        'total_orders':total_orders,
        'products':products
    }
    return render(request,'useradmin/vendor-page.html',context)


@admin_required
def review_page_view(request):
    vendor = Vendor.objects.filter(user=request.user).first()
    products = Product.objects.filter(vendor=vendor)
    reviews = ProductReview.objects.filter(product__in=products)
    context={'products':products
             ,'reviews':reviews}
    return render(request,'useradmin/review-page.html',context)


@admin_required
def settings_view(request):
    profile = Profile.objects.get(user=request.user) 
    context={'profile':profile}
    return render(request,'useradmin/settings.html',context)


@admin_required
def update_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    if (request.method=='POST'):
        full_name = request.POST['full_name']
        bio = request.POST['bio']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        username=request.POST['username']
        profile.full_name = full_name
        profile.bio = bio
        profile.mobile = mobile
        profile.image = image
        profile.user.username = username
        profile.save()
        messages.success(request,'Profile updated successfully')
        return redirect('useradmin:settings')
    

@admin_required    
@login_required
def change_password_view(request):
    if request.method=='POST':
        current_password = request.POST['current_pwd']
        new_password = request.POST['new_pwd']
        confirm_password = request.POST['confirm_pwd']
        if new_password != confirm_password:
            messages.error(request,'New password and confirm password does not match')
            return redirect('useradmin:password_change')
        if check_password(current_password,request.user.password):
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request,'Password changed successfully')
            return redirect('useradmin:password_change')
        else:
            messages.error(request,'Current password is incorrect')
            return redirect('useradmin:password_change')
        
    else:
        return render(request,'useradmin/change-password.html')



