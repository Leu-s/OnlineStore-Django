from django.urls import path
from .views import cart_detail
from .views import cart_add
from .views import cart_remove

app_name = 'cart'
urlpatterns = [
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('', cart_detail, name='cart_detail'),
]
