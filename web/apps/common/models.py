from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy


from simple_history.models import HistoricalRecords
import ulid
import uuid


def generate_ulid():
    return str(ulid.ULID())


def generate_uuid():
    return str(uuid.uuid4())


class HistoryMixin(models.Model):
    history = HistoricalRecords(inherit=True)

    def get_history(self):
        return_data = []
        all_histories = self.history.all()
        for history in all_histories:
            delta = history.diff_against(history.prev_record)
            for change in delta.changes:
                if change.old:
                    comment = (
                        f"{change.field} changed from {change.old} to {change.new}"
                    )
                else:
                    comment = f"{change.field} set to {change.new}"
            return_data.append(
                {
                    "date": history.history_date,
                    "user": history.history_user,
                    "comment": comment,
                }
            )
        return return_data

    class Meta:
        abstract = True


class AbstractBaseModel(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        default=generate_uuid,
        unique=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    active = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in self.__class__._meta.fields
        ]

    class Meta:
        abstract = True
        ordering = [
            "created_at",
        ]


class ImmutableBaseModel(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=36,
        default=generate_uuid,
        unique=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in self.__class__._meta.fields
        ]

    class Meta:
        abstract = True
        ordering = [
            "created_at",
        ]


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# SETTINGS
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


class Settings(AbstractBaseModel):
    def __str__(self):
        return f"Common app settings"
