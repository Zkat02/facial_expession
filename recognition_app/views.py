from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserLoginForm, ContactForm, CalculationForm  # , UserForm, ProfileForm
from .models import User, Profile, Calculation


def index(request):
    return render(request, 'recognition_app/index.html')


# def analise_image(request):
#     return render(request, 'recognition_app/analise_image.html')

# def analise_image(request):
#     if request.method == 'POST':
#         form = AnaliseImageForm(request.POST)
#         print(form.cleaned_data)
#         if form.is_valid():
#             print("111111111111111111111")
#             print(**form.cleaned_data)
#             calculation = form.save()
#             messages.success(request, 'data received successfully!')
#             return redirect('calculation')
#         else:
#             print("333333333333333333")
#             messages.error(request, 'error!')
#     else:
#         print("222222222222222222")
#         form = AnaliseImageForm()
#     return render(request, 'recognition_app/image_form.html', {'form': form})

# @login_required
# def CreateCaluculation(request):
#     if request.method == 'POST':
#         form = CalculationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Education Added Successfully')
#             return redirect('home')
#     else:
#         form = CalculationForm()
#     context = { 'form': form, }
#     return render(request, 'recognition_app/image_form.html', context)

# class CreateCaluculation(LoginRequiredMixin,CreateView):
#     def post(self):
#         user = self.request.user
#         form_class = CalculationForm
#         template_name = 'recognition_app/image_form.html'
#         success_url = reverse_lazy('home')

@login_required
def CreateCaluculation(request):
    form = CalculationForm(request.user, request.POST or None)
    if form.is_valid():
        calc = form.save(commit=False)
        calc.user = request.user
        calc.save()
        return redirect('home')

    return render(request, 'recognition_app/image_form.html', {'form': form})


# class CreateCaluculation(LoginRequiredMixin,CreateView):
#     def post(self):
#         user = self.request.user
#         model = Calculation
#         form_class = CalculationForm
#         template_name = 'recognition_app/image_form.html'
#         if form_class.is_valid():
#             form_class.save()
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)


def view_calculation(request):
    user = request.user
    user_calc = [Calculation.objects.get(user_id=user)]
    print(user_calc)
    return render(request, 'recognition_app/view_calculations.html', {'user': user, 'calculations': user_calc})


def view_profile(request):
    return render(request, 'recognition_app/profile.html', {'user': request.user})

# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Ваш профиль был успешно обновлен!')
#             return redirect('recognition_app/profile.html')
#         else:
#             messages.error(request, 'Пожалуйста, исправьте ошибки.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'recognition_app/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                             'zkatdjango@gmail.com', ['id.a1430@gmail.com'], fail_silently=True)

            if mail:
                messages.success(request, 'Ваше письмо успешно отправлено!')
                return redirect('home')
            else:
                messages.error(request, 'Ошибочка! Не удалось отправить Ваше письмо!')
    else:
        form = ContactForm()
    return render(request, 'recognition_app/contact.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибочка! Не удалось зарегистрироваться!')
    else:
        form = UserRegisterForm()

    return render(request, 'recognition_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # !!! data = request.POST
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибочка! Не удалось войти!')
    else:
        form = UserLoginForm()
    return render(request, 'recognition_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
