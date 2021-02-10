from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .utilities import get_timestamp_path
from .utilities import my_slugify
from django_extensions.db.fields import AutoSlugField


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True,
                                       db_index=True,
                                       verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(max_length=30,
                            db_index=True,
                            unique=True,
                            verbose_name='Название')
    order = models.SmallIntegerField(default=0,
                                     db_index=True,
                                     verbose_name='Порядок')
    super_category = models.ForeignKey('SuperCategory',
                                       on_delete=models.PROTECT,
                                       null=True,
                                       blank=True,
                                       verbose_name='Надкатегория')


class SuperCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надкатегория'
        verbose_name_plural = 'Надкатегории'


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return f'{self.super_category.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_category__order',
                    'super_category__name',
                    'order',
                    'name')
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    currency_list = (
        (None, '------------------------------'),
        ('грн.', 'UAH'),
        ('долл.', 'USD'),
        ('ев.', 'EUR'),
    )
    p_countries = (
        (None, '------------------------------'),
        ('UA', 'Украина'),
        ('RU', 'Россия'),
        ('PL', 'Польша'),
        ('BL', 'Белорусь'),
        ('CN', 'Китай'),
    )
    slug = AutoSlugField(populate_from='title', slugify_function=my_slugify)
    title = models.CharField(max_length=50, verbose_name='Название')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    producing_country = models.CharField(null=True, max_length=24,choices=p_countries,
                                         verbose_name='Страна производитель')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(null=True, max_length=8, choices=currency_list, verbose_name='Валюта')
    description = models.TextField(max_length=256, verbose_name='Описание')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name='Категория')

    def delete(self, *args, **kwargs):
        for i in self.additionalimages_set.all():
            i.delete(*args, **kwargs)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-published']


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар')
    author = models.CharField(max_length=50, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    published = models.DateTimeField(auto_now_add=True, db_index=True,
                                     verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-published']


class AdditionalImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Дополнительное изображение'
        verbose_name_plural = 'Дополнительные изображения'

