from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Q
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.core.paginator import Paginator

from .models import AdvUser
from .models import Product
from .models import AdditionalImages
from .models import Category
from .models import SubCategory
from .models import Comment

from .forms import ChangeUserInfoForm
from .forms import RegisterUserForm
from .forms import SearchForm
from .forms import UserCommentForm

from cart.forms import CartAddProductForm


def other_page(request, page):
    try:
        template = get_template(page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('products:reg_successful')


class RegisterSuccessfulView(TemplateView):
    template_name = 'register_successful.html'


@login_required
def profile(request):
    return render(request, 'profile.html')


class PLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('products:index')


class PLogoutView(LoginRequiredMixin,
                  LogoutView):
    template_name = 'logout.html'


class ChangeUserInfoView(SuccessMessageMixin,
                         LoginRequiredMixin,
                         UpdateView):
    model = AdvUser
    template_name = 'change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('products:profile')
    success_message = 'Информация о пользователе изменена'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset,
                                 pk=self.user_id)


class PChangePasswordView(SuccessMessageMixin,
                          LoginRequiredMixin,
                          PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('products:profile')
    success_message = 'Пароль успешно изменен'


class PDeleteUserView(LoginRequiredMixin,
                      DeleteView):
    model = AdvUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('products:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset,
                                 pk=self.user_id)


def search_keyword(request, products_obj):
    keyword = ''
    products = products_obj
    if 'search_keyword' in request.GET:
        keyword = request.GET['search_keyword']
        q = Q(title__contains=keyword) | Q(description__contains=keyword)
        products = products_obj.filter(q)
    return {'keyword': keyword,
            'products': products}


def my_paginator(request, objects, items_in_page=1):
    paginator = Paginator(objects, items_in_page)
    if 'page' in request.GET:
        page_number = request.GET['page']
    else:
        page_number = 1
    return paginator.get_page(page_number)


def index(request):
    template = 'index.html'
    keyword = search_keyword(request=request,
                             products_obj=Product.objects.all())
    form = SearchForm(initial={
        'search_keyword': keyword['keyword']
    })
    page = my_paginator(request=request,
                        objects=keyword['products'],
                        items_in_page=3)
    context = {
        'products': page.object_list,
        'form': form,
        'page': page
    }

    return render(request, template, context=context)


class InCategoryView(ListView):
    """in category"""
    template_name = 'in_category.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs['pk']
        keyword = search_keyword(request=self.request,
                                 products_obj=self.model.objects.filter(category__super_category_id=category_pk))
        form = SearchForm(initial={
            'search_keyword': keyword['keyword'],
        })
        page = my_paginator(request=self.request,
                            objects=keyword['products'],
                            items_in_page=2)
        context['sub_categories'] = SubCategory.objects.filter(super_category_id=category_pk)
        context['category'] = Category.objects.get(pk=category_pk)
        context['products'] = page.object_list
        context['form'] = form
        context['page'] = page
        return context


class InSubCategoryView(ListView):
    """in sub category"""
    template_name = 'in_sub_category.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sub_category_pk = self.kwargs['pk']
        keyword = search_keyword(request=self.request,
                                 products_obj=self.model.objects.filter(category_id=sub_category_pk))
        form = SearchForm(initial={
            'search_keyword': keyword['keyword']
            })
        page = my_paginator(request=self.request,
                            objects=keyword['products'],
                            items_in_page=2)
        category = SubCategory.objects.get(pk=sub_category_pk)
        context['sub_category'] = category
        context['sub_categories'] = SubCategory.objects.filter(super_category_id=category.super_category.pk)
        context['products'] = page.object_list
        context['form'] = form
        context['page'] = page
        return context


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        other_images = AdditionalImages.objects.filter(product_id=self.object.pk)
        initial = {'product': self.object}
        if self.request.user.is_authenticated:
            initial['author'] = self.request.user.username
        else:
            initial['author'] = 'Anonymous user'
        comments = Comment.objects.filter(product=self.object)
        comment_page = my_paginator(request=self.request, objects=comments, items_in_page=4)
        context['cart_form'] = CartAddProductForm()
        context['page'] = comment_page
        context['comments'] = comment_page.object_list
        context['comment_form'] = UserCommentForm(initial=initial)
        context['images'] = other_images
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(*args, **kwargs)
        if 'add_comment' in self.request.POST:
            form = UserCommentForm(self.request.POST)
            if form.is_valid():
                form.save()
                context['form'] = form
                messages.add_message(request=self.request, level=messages.SUCCESS,
                                     message='Комментарий добавлен')
            else:
                context['form'] = UserCommentForm(request.POST)
                messages.add_message(request=self.request, level=messages.WARNING,
                                     message='Возникла ошибка при добавлении комментария')
        return self.render_to_response(context)
