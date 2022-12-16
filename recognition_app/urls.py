from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('download_pdf/<int:pk>', download_pdf, name='download_pdf'),  # <int:pk>
    path('download_json/<int:pk>', download_json, name='download_json'),
    path('registration/', register, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('profile/update_profile>', update_profile, name='update_profile'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/calculations', view_calculations, name='view_calculations'),
    path('analise_image/>', create_caluculation, name='analise_image'),
]
