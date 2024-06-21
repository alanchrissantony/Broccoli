from promotion.models import Promotion, Discount, PromotionCategory
from django.dispatch import receiver
from django.db.models.signals import post_save

# Signal Handlers
@receiver(post_save, sender=Discount)
def update_promotion_status(sender, instance, **kwargs):
    if not instance.status:
        Promotion.objects.filter(discount=instance).update(status=False)
        PromotionCategory.objects.filter(discount=instance).update(status=False)