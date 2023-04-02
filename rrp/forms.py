from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model
from django.forms import ClearableFileInput

import os
import pandas as pd

User = get_user_model()

types = [('IL', 'IL'),
         ('FC', 'FC')]
groups = [('Big Cities', 'Big Cities'),
          ('Other', 'Other')]

cities = [('Adana', 'Adana'), ('Afyonkarahisar', 'Afyonkarahisar'), ('Amasya', 'Amasya'), ('Ankara', 'Ankara'),
          ('Antalya', 'Antalya'), ('Aydın', 'Aydın'), ('Balıkesir', 'Balıkesir'), ('Bursa', 'Bursa'),
          ('Denizli', 'Denizli'), ('Diyarbakır', 'Diyarbakır'), ('Edirne', 'Edirne'), ('Elazığ', 'Elazığ'),
          ('Eskişehir', 'Eskişehir'), ('Gaziantep', 'Gaziantep'), ('Karabük', 'Karabük'), ('Kastamonu', 'Kastamonu'),
          ('Kayseri', 'Kayseri'), ('Kocaeli', 'Kocaeli'), ('Konya', 'Konya'), ('Kütahya', 'Kütahya'),
          ('Kırklareli', 'Kırklareli'), ('Muğla', 'Muğla'), ('Sakarya', 'Sakarya'), ('Samsun', 'Samsun'),
          ('Tekirdağ', 'Tekirdağ'), ('Tokat', 'Tokat'), ('Uşak', 'Uşak'), ('İstanbul', 'İstanbul'), ('İzmir', 'İzmir'),
          ('Şanlıurfa', 'Şanlıurfa')]


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
    photo = forms.ImageField(label="Account photo", required=False,
                             widget=ClearableFileInput(attrs={'class': 'file_field'}))
    username = forms.CharField(label='Username', max_length=35, required=False,
                               widget=forms.TextInput(attrs={'class': 'input_field'}))
    first_name = forms.CharField(label="First name", required=False, max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'input_field'}))
    last_name = forms.CharField(label="Last name", required=False, max_length=50,
                                widget=forms.TextInput(attrs={'class': 'input_field'}))
    email = forms.EmailField(label="Email", required=False, max_length=50,
                             widget=forms.EmailInput(attrs={'class': 'input_field'}))
    birth_date = forms.DateField(label="Date of birth", required=False,
                                 widget=AdminDateWidget(attrs={'class': 'input_field'}))
    company = forms.CharField(label="Company", required=False, max_length=45,
                              widget=forms.TextInput(attrs={'class': 'input_field'}))
    additional_data = forms.CharField(label="Extra information", required=False,
                                      widget=forms.Textarea(attrs={'class': 'category_text'}))

    class Meta:
        model = User
        fields = ("photo", "username", "first_name", "last_name", "email", "birth_date", "company", "additional_data")

    def clean_username(self):
        username = self.cleaned_data['username']

        if username == "":
            raise forms.ValidationError("username can\'t be an empty string")

        return username


class UploadFileForm(forms.Form):
    input_file = forms.FileField(label="Input file")
    city_name = forms.CharField(label="City name", required=False,
                                widget=forms.SelectMultiple(attrs={'class': 'input_field'}, choices=cities))
    city_group = forms.ChoiceField(label="City Group", required=False,
                                   widget=forms.RadioSelect(attrs={'class': 'select_field'}), choices=groups)
    restaurant_type = forms.ChoiceField(label="Restaurant Type", required=False,
                                        widget=forms.RadioSelect(attrs={'class': 'select_field'}), choices=types)

    def clean_input_file(self):
        file = self.cleaned_data.get('input_file', None)

        extension = str(os.path.splitext(file.name)[1][1:].lower())

        if extension != 'csv':
            raise forms.ValidationError('File type is not allowed')

        return file

    def clean_city_name(self):
        file = self.cleaned_data.get('input_file', None)
        data = pd.read_csv(file)
        file.seek(0)

        name = self.cleaned_data.get('city_name')
        if 'City' not in data.columns and name == "":
            raise forms.ValidationError('City name field is not filled')
        return name[2: len(name) - 2]

    def clean_city_group(self):
        file = self.cleaned_data.get('input_file', None)
        data = pd.read_csv(file)
        file.seek(0)

        group = self.cleaned_data.get('city_group')
        if 'City Group' not in data.columns and group == "":
            raise forms.ValidationError('City group field is not filled')

        return group

    def clean_restaurant_type(self):
        file = self.cleaned_data.get('input_file', None)
        data = pd.read_csv(file)
        file.seek(0)

        rest_type = self.cleaned_data.get('restaurant_type')
        if 'Type' not in data.columns and rest_type == "":
            raise forms.ValidationError('Type field is not filled')

        return rest_type
