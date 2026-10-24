from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True   # ✅ IMPORTANT
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Email is required')
        
        if not password:
            raise ValueError('Password is required')

        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=12)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class Category(models.Model):
    cat_name=models.CharField(max_length=255, unique=True, verbose_name="Name of Category")
    def __str__(self):
        return self.cat_name
class Product(models.Model):
    images= models.ImageField(upload_to='shop/pimg')
    cat_name=models.CharField(max_length=255, verbose_name="Name of the Item")
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    desc=models.CharField(max_length=255, verbose_name='Category Short Description')
    price=models.IntegerField()
    def __str__(self):
        return self.cat_name
    

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)

	def _str_(self):
		return f'{self.quantity} x {self.product.name}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    address=models.TextField()
