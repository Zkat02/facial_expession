from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from reportlab.lib.utils import ImageReader
from .forms import UserRegisterForm, UserLoginForm, ContactForm, CalculationForm, ProfileForm
from .models import Calculation, UserCalculation, Profile
import logging
from .recognition_script import recognise
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)


def download_pdf(request, pk):  # , calk_pk
    buffer = io.BytesIO()  # Create a file-like buffer to receive PDF data.
    p = canvas.Canvas(buffer)

    calc = Calculation.objects.get(pk=pk)
    logger.debug(f"create PDF of obj: {calc}.")

    img_path = ImageReader(calc.calculation_image)
    strs_to_draw = [f"Result of processing by neural network: emotion on image {calc.result}",
                    f"Additionl info: {calc.info}",
                    "This file and the prediction was made using a neural network by Recognition expression application"]

    # Draw on the PDF
    p.drawImage(img_path, x=100, y=600, width=200, height=200, mask=None)
    for i, str in enumerate(strs_to_draw):
        p.drawString(50, 550 - i * 15, str)

    # Close the PDF object
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='recognition_result.pdf')


def download_json(request, pk):
    calc = Calculation.objects.filter(pk=pk)
    logger.debug(f"create PDF of obj: {calc}.")
    json_str = serializers.serialize('json', calc)
    response = HttpResponse(json_str, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=recognition_result.json'
    return response


def index(request):
    logger.debug("index")
    return render(request, 'recognition_app/index.html')


def create_caluculation(request):
    if request.method == 'POST':
        form = CalculationForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            calc = form.instance
            calc.result = recognise(calc.calculation_image)
            calc.save()
            logger.debug(f"calculaton result: {calc.result}")
            uc = UserCalculation.objects.create(user=user, calculation=calc)
            uc.save()

            return (redirect('view_calculations'))
    else:
        form = CalculationForm()
    return render(request, 'recognition_app/image_form.html', {'form': form})


def view_calculations(request):
    user = request.user
    user_calc = []
    if User.objects.filter(username=user.username).exists():
        user_calc = UserCalculation.objects.filter(user=user)
        profile = Profile.objects.filter(user=user).update(amount_calculations=len(user_calc))
    return render(request, 'recognition_app/view_calculations.html', {'user_calculations': user_calc})


def view_profile(request):
    return render(request, 'recognition_app/profile.html', {'user': request.user})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        # user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():  # \
            # and user_form.is_valid()
            # user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('view_profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        # user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'recognition_app/update_profile.html', {
        # 'user_form': user_form,
        'profile_form': profile_form
    })


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
