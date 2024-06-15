# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import UserProfile, Project, Comment, Reply

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
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = User
        fields = ('username', 'email',)  # Add other fields from User model as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            user_profile, created = UserProfile.objects.get_or_create(user=self.instance)
            self.fields['profile_picture'].initial = user_profile.profile_picture

    def save(self, commit=True):
        user = super().save(commit)
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        if created or 'profile_picture' in self.changed_data:
            user_profile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user_profile.save()

        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'role']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name_of_the_project', 'tender_number','project_type',  'name_of_the_contractor', 'handling_officer'] # 'files', is an existing field, can be added

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter handling officers based on their role
        self.fields['handling_officer'].queryset = User.objects.filter(userprofile__role='officer')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
