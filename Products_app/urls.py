from django.urls import path
from .views import index
from .views import other_page
from .views import PLoginView
from .views import PLogoutView
from .views import profile
from .views import ChangeUserInfoView
from .views import PChangePasswordView
from .views import RegisterUserView
from .views import RegisterSuccessfulView
from .views import PDeleteUserView
from .views import InCategoryView
from .views import InSubCategoryView
from .views import ProductDetailView

app_name = 'products'
urlpatterns = [
    path('accounts/register/successful', RegisterSuccessfulView.as_view(), name='reg_successful'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/change_password/', PChangePasswordView.as_view(), name='change_password'),
    path('accounts/profile/change_info/', ChangeUserInfoView.as_view(), name='profile_change_info'),
    path('accounts/profile/delete/', PDeleteUserView.as_view(), name='delete_profile'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', PLoginView.as_view(), name='login'),
    path('accounts/logout/', PLogoutView.as_view(), name='logout'),
    path('category/sub/<int:pk>/', InSubCategoryView.as_view(), name='in_sub_category'),
    path('category/<int:pk>/', InCategoryView.as_view(), name='in_category'),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('about/<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
