import uuid
from datetime import timedelta
from celery import shared_task
from django.utils.timezone import now
from .models import User, EmailVerificatiom





@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id= user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerificatiom.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
