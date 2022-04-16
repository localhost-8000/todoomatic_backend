from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, URLField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    photoURL = URLField(_("Photo URL of User"), blank=True)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
