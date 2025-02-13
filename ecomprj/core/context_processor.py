from logging import Logger
from core.models import Product,Vendor,Category,ProductImage,ProductReview,CartOrder,CartOrderItems,Wishlist,Address
from django.db.models import Min, Max
def default(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(min_price=Min('price'),max_price=Max('price'))
    print('price range',min_max_price)
    try:
          address = Address.objects.get(user=request.user)
    except:
         address=None
    return {
         'categories':categories,
         'address':address,
         'vendors':vendors,
         'min_max_price':min_max_price
    }