
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.urls import reverse_lazy

from users.models import User
from django.forms import BooleanField, ModelForm


# class StyleFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")





class UserUpdateForm(StyleFormMixin, ModelForm):

    class Meta:
        model = User
        fields = "__all__"
        exclude = ("token",)

        success_url = reverse_lazy("users:users")
