from .widgets import *
from .models import *


class AddProfileForm(forms.ModelForm):

    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'gender', 'birth_date', 'start_date', 'graduate_date')


class ChangeProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('photo', 'username', 'email', 'first_name', 'last_name', 'is_active',
                  'gender', 'birth_date', 'start_date', 'graduate_date')

    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    is_active = forms.BooleanField()

    photo = forms.ImageField(widget=ImageWidget)

    def get_initial_for_field(self, field, field_name):
        profile = self.instance
        if field_name == 'username':
            return profile.user.username
        elif field_name == 'email':
            return profile.user.email
        elif field_name == 'first_name':
            return profile.user.first_name
        elif field_name == 'last_name':
            return profile.user.last_name
        elif field_name == 'is_active':
            return profile.user.is_active
        elif field_name == 'photo':
            return profile.display_clickable_photo

        return super().get_initial_for_field(field, field_name)
