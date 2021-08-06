from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


import django_filters


class BaseFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(BaseFilterSet, self).__init__(*args, **kwargs)
        self.form.label_suffix = ""
