import uuid

from django.utils.six import with_metaclass
from django.db.models import (
    AutoField,
    SubfieldBase
)
from django.utils.translation import ugettext_lazy as _


class AutoFieldUUID(with_metaclass(SubfieldBase, AutoField)):
    description = _('UUID')

    default_error_messages = {
        'invalid': _("'%(value)s' value must be a valid UUID."),
    }

    def to_python(
        self,
        value
    ):
        if isinstance(value, uuid.UUID):
            return str(value)

        else:
            return value

    def get_prep_value(self, value):
        value = super(AutoField, self).get_prep_value(value)
        if (
            value is None or
            isinstance(value, uuid.UUID)
        ):
            return value

        return uuid.UUID(value)

    def get_internal_type(self):
        return 'AutoFieldUUID'

    def get_auto_value(self):
        return uuid.uuid4()

    def value_to_string(self, value):
        if isinstance(value, basestring):
            return value

        try:
            return str(value)

        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
