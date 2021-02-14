from django.contrib import admin
from Products_app.models import AdvUser

from .models import Product
from .models import AdditionalImages
from .models import SuperCategory
from .models import SubCategory
from .forms import SubCategoryForm


class SubCategoryInLine(admin.TabularInline):
    model = SubCategory


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInLine,)


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


class AdditionalImagesInline(admin.TabularInline):
    model = AdditionalImages


class ProductAdmin(admin.ModelAdmin):
    fields = ('category',
              'image',
              'title',
              'in_stock',
              'producing_country',
              'price',
              'currency',
              'description',
              )

    list_display = ('in_stock',
                    'category',
                    'title',
                    'price',
                    'currency',
                    'published')
    inlines = (AdditionalImagesInline,)


admin.site.register(Product, ProductAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(AdvUser)


from .models import Comment, CommentRating
admin.site.register(Comment)
admin.site.register(CommentRating)
