from celery import shared_task
from django.utils.timezone import now
from order.models import GiftCard

@shared_task
def deactivate_expired_gift_cards():
    expired_gift_cards = GiftCard.objects.filter(expiry_date__lt=now(), is_active=True)
    expired_gift_cards.update(is_active=False)
