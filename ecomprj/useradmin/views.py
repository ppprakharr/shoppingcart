from django.shortcuts import render, redirect
from userauths.models import User
from core.models import Category, CartOrder, Product, CartOrderItems
from django.db.models import Sum
from useradmin.forms import AddProductForm
import datetime
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

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

def products(request):
    products = Product.objects.all()
    category=Category.objects.all()

    context={
        'products':products,
        'category':category
    }

    return render(request,'useradmin/products.html',context)


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

def orders_view(request):
    orders = CartOrder.objects.all()
    context={
        'orders':orders
                }
    return render(request,'useradmin/orders.html',context)

def order_details_view(request,id):
    order=CartOrder.objects.get(id=id)
    cart_order = CartOrderItems.objects.filter(order=order)
    context={
        'order':order,
        'cart_order':cart_order
        }
    
    return render(request,'useradmin/order-details.html',context)

def change_order_status_view(request,oid):
    if request.method=='POST':
        status = request.POST['status']
        order=CartOrder.objects.get(oid=oid)
        order.product_status = status
        order.save()
        messages.success(request,'Order status changed successfully')
        return redirect('useradmin:order_details',id=order.id)


