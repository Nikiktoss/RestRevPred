import logging

import pandas as pd
import numpy as np
import json
import fpdf

from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from django.http import HttpResponse


from .forms import LoginUserForm, UserRegistrationForm, UserEditForm, UploadFileForm
from django.contrib.auth import get_user_model, login
from.revenue_model import cb, normalizer, get_result_data
from.html_code_generator import HTMlCodeGenerator
from.pdf_output import PDF, generate_pdf_file
from.json_output import JSON
from.models import PredictionResult


logger = logging.getLogger(__name__)
html_generator = HTMlCodeGenerator()


@login_required
def main(request):
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
        logger.info(f'User {self.request.user.username} logged in successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        logger.info("Invalid username or password")
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
            logger.info(f'User {self.request.user.username} logged in successfully')
            return redirect(self.get_success_url())

        logger.info(f'Invalid values while creating account')
        return render(request, self.template_name, context={'form': form})


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "accounts.html"


class UserUpdateView(UpdateView):
    form_class = UserEditForm
    template_name = "edit_profile.html"
    model = get_user_model()

    def get_success_url(self):
        logger.debug(f'User {self.request.user.username} updates personal data')
        return reverse_lazy('profile_page', kwargs={'slug': self.request.user.slug})


class CalculationForm(FormView):
    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, "calculate_form.html", context={'user': request.user, 'form': form, 'is_form': True})

    @staticmethod
    def get_form_data(form):
        data = pd.read_csv(form.cleaned_data['input_file'])

        if data.shape[0] > 1:
            data = pd.DataFrame(np.array(data.values[0]).reshape(1, len(data.columns)), columns=data.columns)

        if 'City' not in data.columns:
            data['City'] = form.cleaned_data['city_name']

        if 'City Group' not in data.columns:
            data['City Group'] = form.cleaned_data['city_group']

        if 'Type' not in data.columns:
            data['Type'] = form.cleaned_data['restaurant_type']

        return data

    @staticmethod
    def generate_files(*args):
        pdf = PDF()
        js = JSON()

        pdf_content = None
        try:
            generate_pdf_file(pdf, args[0], args[1], args[2], args[3], args[4])
            pdf_content = pdf.output()
        except fpdf.FPDFException:
            logger.error(f'Error while generating pdf')
        json_content = js.create_result_object(args[0], args[1], args[2], args[3], args[4])

        return pdf_content, json.dumps(json_content)

    @staticmethod
    def update_data(request, revenue, pdf_file, json_file):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        user.number_of_predictions += 1
        user.save()

        revenue_result = PredictionResult(user=user, revenue=revenue[0])
        revenue_result.save()
        if pdf_file is not None:
            revenue_result.pdf_file.save(f'revenue_result_{revenue_result.pk}.pdf', ContentFile(pdf_file))
        revenue_result.json_file.save(f'revenue_result_{revenue_result.pk}.json', ContentFile(json_file))
        revenue_result.save()

        return revenue_result

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            logger.info(f'get data from user {request.user.username}')

            data = self.get_form_data(form)
            num_data, cat_data, normalize_num_data, normalize_cat_data, revenue = get_result_data(cb, normalizer, data)
            html_output = html_generator.generate_html(num_data, cat_data, normalize_num_data, normalize_cat_data,
                                                       revenue[0])
            # try:
            pdf_content, json_content = self.generate_files(num_data, cat_data, normalize_num_data, normalize_cat_data,
                                                            revenue)
            # except fpdf.FPDFException:
            #     logger.error(f'Error in generating pdf file for user {request.user.username}')

            obj = self.update_data(request, revenue, pdf_content, json_content)
            id_json, id_pdf = obj.pk, obj.pk

            if not obj.pdf_file:
                id_pdf = -1

            return render(request, "calculate_form.html", context={'user': request.user, 'is_form': False,
                                                                   'content': mark_safe(html_output),
                                                                   'id_json': id_json, 'id_pdf': id_pdf})
        else:
            logger.info(f'Error values in send data from user {request.user.username}')
            return render(request, "calculate_form.html", context={'user': request.user, 'form': form, 'is_form': True})


def send_pdf_file(request, pk):
    pdf_path = f'media/pdf_files/user_{request.user.pk}/revenue_result_{pk}.pdf'

    with open(pdf_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="revenue_prediction_{request.user.username}_' \
                                          f'{request.user.number_of_predictions}.pdf"'

    logger.info(f'User {request.user.username} download result via .pdf file')
    return response


def send_json_file(request, pk):
    json_path = f'media/json_files/user_{request.user.pk}/revenue_result_{pk}.json'
    with open(json_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="revenue_prediction_{request.user.username}_' \
                                          f'{request.user.number_of_predictions}.json"'

    logger.info(f'User {request.user.username} download result via .json file')
    return response
