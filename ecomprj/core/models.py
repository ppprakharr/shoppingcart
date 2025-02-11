from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

STATUS_CHOICE=(
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered")
)

STATUS=(
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("in_review","In Review"),
    ("rejected","rejected"),
    ("published","Published")
)

RATING=(
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★")
)

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)

class Category(models.Model):
    cid = ShortUUIDField(length=10, max_length=20, unique=True, alphabet = 'abcdefghij1234560789',prefix='cat')
    title = models.CharField(max_length=100,default='product')
    image = models.ImageField(upload_to='category',default='categor.jpg')

    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, prefix="ven",max_length=20, length=10, alphabet='abcdefghi0123456789')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path,default='vendor.jpg')
    # description = models.TextField(null=True, blank=True,default='I am a Vendor')
    description = RichTextUploadingField(null=True, blank=True,default='I am a Vendor')
    address= models.CharField(max_length=100, default='123 Main road, India')
    contact= models.CharField(max_length=100, default='+12 (345) 6789')
    chat_resp_time= models.CharField(max_length=100, default='100')
    shipping_on_time= models.CharField(max_length=100, default='100')
    authentic_rating= models.CharField(max_length=100, default='100')
    days_return= models.CharField(max_length=100, default='100')
    warranty_period= models.CharField(max_length=100, default='100')
    date = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(max_length=20, length=10,unique=True,alphabet='abcdefghij1234567890')
    title = models.CharField(max_length=100,default='this is the prod title')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL,null=True,related_name='products')
    image = models.ImageField(upload_to=user_directory_path,default='product.jpg')
    # description = models.TextField(default='This is the product',null=True,blank=True)
    description = RichTextUploadingField(default='This is the product',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=999999,decimal_places=2,default='1.99')
    old_price = models.DecimalField(max_digits=999999,decimal_places=2,default='1.99')
    # specifications = models.TextField(null=True,blank=True)
    specifications = RichTextUploadingField(null=True,blank=True)
    type= models.CharField(max_length=100,default='Organic',null=True,blank=True)
    mfd=models.DateTimeField(auto_now_add=False,null=True,blank=True)
    stock_count = models.CharField(max_length=100,default='10',null=True,blank=True)
    life=models.CharField(max_length=100,default='100 days',null=True,blank=True)
    tags = TaggableManager(blank=True)
    # tags = models.ForeignKey(Tags,on_delete=models.SET_NULL, null=True)
    product_status= models.CharField(choices=STATUS,max_length=10,default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False) 
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(max_length=10,length=4,unique=True,prefix='sku',alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Products'
    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def get_percentage(self):
        new_price = ((self.old_price - self.price)/(self.old_price))*100
        return new_price

    
    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    images = models.ImageField(upload_to='product-images',default='product.jpg')
    product = models.ForeignKey(Product,related_name='p_image',on_delete=models.SET_NULL,null=True)
    date  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Product Images'

#######################cart,oder,ordertiems, address############################
#######################cart,oder,ordertiems, address############################
#######################cart,oder,ordertiems, address############################

class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    paid_status = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=999999,decimal_places=2,default='1.99')
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='processing')

    class Meta:
        verbose_name_plural  = 'Cart order'

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    item=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    qty=models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999,decimal_places=2,default='1.99')
    total = models.DecimalField(max_digits=999999,decimal_places=2,default='1.99')

    class Meta:
        verbose_name_plural = 'Cart order Items'
    def order_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING,default=0)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Product Review'
    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Wishlists'

    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=200,null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'

    

    






        
# Create your models here.
