from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from .models import User, RegistrationToken, Contracts


@receiver(post_save, sender=User) # триггер на изменение статуса пользователя
def track_user_status_change(sender, instance, created, update_fields=None, **kwargs):
    if created:
        return

    if update_fields and 'status' not in update_fields:
        return

    user_status_change(instance)


def user_status_change(instance): # функция изменения группы пользователей в зависимости от изменения статуса
    GROUP_BY_STATUS = {
        'approved': 'user_without_contract',
        'reject': 'deleted_user',
    }

    group_name = GROUP_BY_STATUS.get(instance.status) # проверка есть ли статус в словаре, и присвоение группы
    if group_name:
        instance.groups.clear()
        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(instance)

        if instance.status == 'approved': # отправка mail письма на создание аккаунта
            token = RegistrationToken.objects.create(user=instance)
            link = f"{settings.SITE_URL}/set-password/{token.token}/"

            send_mail(
                subject="регистрация на сайте",
                message=f"Привет {instance.name}, установите пароль по ссылке {link}",
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
            )






