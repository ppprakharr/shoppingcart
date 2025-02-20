from django.shortcuts import render, redirect
from userauths.models import User
from core.models import Category, CartOrder, Product
from django.db.models import Sum
from useradmin.forms import AddProductForm
import datetime

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

            


# Create your views here.
