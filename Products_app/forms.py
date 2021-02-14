from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import AdvUser
from .models import SuperCategory
from .models import SubCategory
from .models import Comment


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')
    password_1 = forms.CharField(label='Пароль',
                                 widget=forms.PasswordInput,
                                 help_text=password_validation.password_validators_help_text_html())
    password_2 = forms.CharField(label='Повторите пароль',
                                 widget=forms.PasswordInput,
                                 help_text='Введите тот же самый пароль еще раз')

    def clean_password1(self):
        password_1 = self.cleaned_data['password_1']
        if password_1:
            password_validation.validate_password(password_1)
        return password_1

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']

        if password_1 and password_2 and password_1 != password_2:
            errors = {
                'password_2': ValidationError(
                    'Пароли не совпадают', code='password_mismatch'
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = (
            'username',
            'email',
            'password_1',
            'password_2',
            'first_name',
            'last_name',
        )


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(
        queryset=SuperCategory.objects.all(),
        empty_label=None,
        label='Надкатегория',
        required=True,
    )

    class Meta:
        model = SubCategory
        fields = '__all__'


class SearchForm(forms.Form):
    search_keyword = forms.CharField(required=False, max_length=40, label='')


class UserCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = 'text', 'author', 'product'
        widgets = {
            'product': forms.HiddenInput,
            'author': forms.HiddenInput,}
