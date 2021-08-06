from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver, Signal
from django.utils.html import mark_safe
from django.utils.translation import ugettext as _


# ––– PROJECT IMPORTS
from apps.common import models as common_models


# ––– PARAMETERS


# ––– MODELS


class User(PermissionsMixin, AbstractBaseUser, common_models.AbstractBaseModel):
    username_validator = UnicodeUsernameValidator()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    email = models.EmailField("Email address", blank=True)
    is_active = models.BooleanField("Active", default=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    full_name = models.CharField(max_length=80, null=True, blank=True)
    username = models.CharField(
        "Username", max_length=255, unique=True, validators=[username_validator]
    )

    objects = UserManager()

    class Meta:
        ordering = [
            "username",
            "full_name",
        ]

    def __str__(self):
        return f"{self.username}"


class Profile(common_models.AbstractBaseModel):
    """Settings for individual user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.user} | profile"

    class Meta:
        ordering = [
            "user",
        ]


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# SETTINGS
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


class Settings(common_models.AbstractBaseModel):
    def __str__(self):
        return f"Settings for Users app"

    class Meta:
        verbose_name_plural = "Settings"


@receiver(post_save, sender=User)
def create_profile_on_user_creation(sender, created, instance, **kwargs):
    """
    Create profile upon User instance creation
    """
    from apps.users.models import Profile

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_settings_on_initial_user_creation(sender, created, instance, **kwargs):
    """Create settings(Module) for all relevant project apps upon initial user creation"""
    from django.apps import registry

    if User.objects.all().count() == 1:
        for app in settings.PROJECT_APPS:
            APPS_WITHOUT_SETTINGS = [
                "apps.common",
                "apps.api",
            ]
            if app in APPS_WITHOUT_SETTINGS:
                continue
            app_label = app.split(".")[1]
            try:
                settings_model = registry.apps.get_model(app_label, "Settings")
            except LookupError:
                continue
            if settings_model.objects.all().count() == 0:
                settings_model.objects.create()
        return
    else:
        return
