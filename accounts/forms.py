from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import UserProfile


class EditProfileForm(UserChangeForm):
    template_name='/something/else'
    image = forms.ImageField(label = 'Image', required =False)
    image.widget.attrs.update({'class':'form-control'})
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )
        


