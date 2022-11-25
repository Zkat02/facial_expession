from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photo/%Y/%m/%d', default="../media/profile_photo/profile_icon.png",
                              verbose_name='Фото пользователя')
    amount_calculations = models.IntegerField(default=0, verbose_name='Количество вычислений')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь создавший вычисление', blank=True, null=True)
    title = models.CharField(max_length=20, default="image_%y%m%d", verbose_name='name', db_index=True)
    calculation_image = models.ImageField(upload_to='calculation_image/%Y/%m/%d',
                                          verbose_name='Image for recognition')
    info = models.TextField(verbose_name='Additional Info', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Calculation'
        verbose_name_plural = 'Calculations'
        ordering = ["-created_at", "title"]