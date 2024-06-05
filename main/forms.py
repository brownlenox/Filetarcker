from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('register', 'Register'))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)  # Add other fields from User model as needed

    # Additional fields from UserProfile model
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the form with data from both User and UserProfile models
        if self.instance.pk:
            user_profile, created = UserProfile.objects.get_or_create(user=self.instance)
            self.fields['profile_picture'].initial = user_profile.profile_picture

    def save(self, commit=True):
        # Save data to both User and UserProfile models
        user = super().save(commit)

        # Check if UserProfile already exists for this user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # If UserProfile was created, update its fields
        if created:
            user_profile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user_profile.save()

        return user
