from user.models import Avatar
import random
from django.core.exceptions import ObjectDoesNotExist


def get_random_avatar_url():
    try:
        avatars = Avatar.objects.all()
        if avatars.exists():
            return random.choice(avatars).image.url
        else:
            return None  # Or a default image URL if no avatars are available
    except ObjectDoesNotExist:
        return None  # Or a default image URL