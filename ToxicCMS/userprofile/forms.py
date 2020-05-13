from django import forms
from django.contrib.auth.models import User

from userprofile.models import Profile


class UserLoginForm(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date',)
