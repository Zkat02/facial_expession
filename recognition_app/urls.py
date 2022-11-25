from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', index, name='home'),
    path('registration/', register, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    # path('analise_image/', analise_image, name='analise_image'),
    #path('profile/<int:user_id>', view_profile, name='profile'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/calculations', view_calculation, name='view_calculation'),
    # path('analise_image/>', CreateCaluculation.as_view(), name='analise_image'),
    path('analise_image/>', CreateCaluculation, name='analise_image'),
]