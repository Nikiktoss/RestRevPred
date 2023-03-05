from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model
from django.forms import ClearableFileInput

User = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={'class': 'input_field'}))
    password = forms.CharField(label='Password', required=False, widget=forms.PasswordInput(attrs={'class': 'input_'
                                                                                                            'field'}))


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={'class': 'input_field'}))
    email = forms.EmailField(label="Email", required=False, widget=forms.EmailInput(attrs={'class': 'input_field'}))
    password1 = forms.CharField(label='Password', required=False, widget=forms.PasswordInput(attrs={'class': 'input_'
                                                                                                             'field'}))
    password2 = forms.CharField(label='Confirm Password', required=False,
                                widget=forms.PasswordInput(attrs={'class': 'input_field'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 == "":
            raise forms.ValidationError("password can\'t be an empty string")

        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')

        validate_password(password=password1)

    def clean_username(self):
        username = self.cleaned_data['username']

        if username == "":
            raise forms.ValidationError("username can\'t be an empty string")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That user is already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == "":
            raise forms.ValidationError("email can\'t be an empty string")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with such email is already exist")
        return email


class UserEditForm(forms.ModelForm):
    photo = forms.ImageField(label="Account photo", required=False)
    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={'class': 'input_field'}))
    first_name = forms.CharField(label="First name", required=False,
                                 widget=forms.TextInput(attrs={'class': 'input_field'}))
    last_name = forms.CharField(label="Last name", required=False,
                                widget=forms.TextInput(attrs={'class': 'input_field'}))
    email = forms.EmailField(label="Email", required=False, widget=forms.EmailInput(attrs={'class': 'input_field'}))
    birth_date = forms.DateField(label="Date of birth", required=False,
                                 widget=AdminDateWidget(attrs={'class': 'input_field'}))
    company = forms.CharField(label="Company", required=False, widget=forms.TextInput(attrs={'class': 'input_field'}))
    additional_data = forms.CharField(label="Extra information", required=False,
                                      widget=forms.TextInput(attrs={'class': 'category_text'}))

    class Meta:
        model = User
        fields = ("photo", "username", "first_name", "last_name", "email", "birth_date", "company", "additional_data")
