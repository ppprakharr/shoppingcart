from logging import Logger
from core.models import Product,Vendor,Category,ProductImage,ProductReview,CartOrder,CartOrderItems,Wishlist,Address
from django.db.models import Min, Max
from django.contrib import messages
def default(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(min_price=Min('price'),max_price=Max('price'))
    try:
          address = Address.objects.get(user=request.user)
    except:
         address=None
     
    try:
         wishlist = Wishlist.objects.filter(user=request.user)
    except:
          wishlist=None
          messages.warning(request,'You need to login before adding products to wishlist')

    return {
         'categories':categories,
         'address':address,
         'vendors':vendors,
         'min_max_price':min_max_price,
         'wishlist':wishlist
    }