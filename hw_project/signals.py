from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Task

@receiver(pre_save, sender=Task)
def notify_task_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        prev = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    old_status = prev.status
    new_status = instance.status

    if old_status == new_status:
        return

    author = getattr(instance, "author", None)
    if not author or not getattr(author, "email", None):
        return

    subject = f"Задача '{instance.title}' изменила статус"
    message = (
        f"Здравствуйте, {author.username}!\n\n"
        f"Статус вашей задачи \"{instance.title}\" изменился: {old_status} -> {new_status}.\n\n"
        "Если это сообщение пришло по ошибке, проигнорируйте его."
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [author.email])


    if hasattr(instance, "last_notified_status"):
        instance.last_notified_status = new_status