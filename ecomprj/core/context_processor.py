from core.models import Product,Vendor,Category,ProductImage,ProductReview,CartOrder,CartOrderItems,Wishlist,Address

def default(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return {
         'categories':categories,
         'products':products
    }