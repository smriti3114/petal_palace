from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Category, Product,Order

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'is_staff', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email',)
    readonly_fields = ('date_joined',)

    filter_horizontal = ()

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display=('id','cat_name')

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    def product_img(self,obj):
        return format_html('<img src="{}" width="50" height="50">'.format(obj.images.url))
    product_img.short_description = 'Image'

    list_display = ('cat_name', 'desc', 'price', 'category', 'product_img')

# @admin.register(Order)
# class AdminOrder(admin.ModelAdmin):
#     list_display=('user','product','price','category','date_ordered','payment_status','payment_id','address')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'product', 'quantity', 'payment_status', 'address', 'date_ordered')
    list_filter = ('payment_status', 'date_ordered')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'product__name', 'address')
    ordering = ('-date_ordered',)

    # Custom method to show full name
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" or obj.user.email