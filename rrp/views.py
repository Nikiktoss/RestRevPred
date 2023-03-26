from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView
from .revenue_model import RevenuePredictionModel

from .forms import LoginUserForm, UserRegistrationForm, UserEditForm, UploadFileForm
from django.contrib.auth import get_user_model, login

import logging
import pandas as pd


logger = logging.getLogger(__name__)
prediction_model = RevenuePredictionModel()
prediction_model.fit_model()


@login_required
def main(request):
    logger.debug('Ok')
    return render(request, 'main.html', context={'user': request.user})


class UserLoginView(LoginView):
    form_class = LoginUserForm
    redirect_authenticated_user = True
    template_name = 'sign_in_page.html'

    def get_success_url(self):
        return reverse_lazy('main_page')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': self.form_class(), 'user': request.user})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]

        if username == "" or password == "":
            return self.form_invalid(self.get_form())
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "You have been successfully logged in RRP")
        logging.info('logged in!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class UserCreateView(CreateView):
    template_name = "sign_up_page.html"
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse_lazy('main_page')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            User = get_user_model()
            user = User.objects.create_user(username=form.cleaned_data["username"], email=form.cleaned_data["email"],
                                            password=form.cleaned_data["password1"])

            messages.success(self.request, "You have been successfully logged in RRP")
            login(request, user)
            return redirect(self.get_success_url())

        return render(request, self.template_name, context={'form': form})


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "accounts.html"


class UserUpdateView(UpdateView):
    form_class = UserEditForm
    template_name = "edit_profile.html"
    model = get_user_model()

    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={'slug': self.request.user.slug})


def calculation_form(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file_content = pd.read_csv(form.cleaned_data['input_file'])
            numeric_data, category_data = prediction_model.divide_data(file_content)
            normalize_data = prediction_model.prepare_data(file_content)
            normalize_cat_data = normalize_data[['City', 'City Group', 'Type']]
            normalize_num_data = normalize_data.drop(['City', 'City Group', 'Type'], axis=1)
            result_revenue = prediction_model.predict_revenue(file_content)
            return render(request, "calculate_form.html", context={'user': request.user, 'is_form': False,
                                                                   'cat_cols': category_data.columns,
                                                                   'num_cols': numeric_data.columns,
                                                                   'num_values': numeric_data.values[0],
                                                                   'cat_values': category_data.values[0],
                                                                   'norm_num_data': normalize_num_data.values[0],
                                                                   'norm_cat_data': normalize_cat_data.values[0],
                                                                   'result_revenue': result_revenue[0]})
        else:
            return render(request, "calculate_form.html", context={'user': request.user, 'form': form, 'is_form': True})
    else:
        form = UploadFileForm()
        return render(request, "calculate_form.html", context={'user': request.user, 'form': form, 'is_form': True})
