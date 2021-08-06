class ConvertNoneToStringSerializerMixin:

    """
    Mixin to convert None to empty strings.

    This must be added as the first inherited class. The property `Meta.none_to_str_fields` must
    be defined in order for this to have any effect. This only applies to representations,
    when we export our instance data, not when we acquire and validate data.
    """

    def get_none_to_str_fields(self):
        meta = getattr(self, "Meta", None)
        return getattr(meta, "none_to_str_fields", [])

    def to_representation(self, instance):
        fields = self.get_none_to_str_fields()
        data = super().to_representation(instance)

        if not fields or not isinstance(data, dict):
            return data

        for field in fields:
            if field in data and data[field] is None:
                data[field] = ""

        return data
