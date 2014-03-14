from dateutil.parser import parse as parse_datetime


class Base:

    def prepare(self, value):
        return str(value) if value is not None else None

    def clean(self, text):
        if text is not None:
            return text


class String(Base):
    """String values [saml-core § 1.3.1].
    """


class Integer(Base):
    """Integral values.
    """


class Boolean(Base):
    """Boolean values.
    """

    def prepare(self, value):
        if value is None:
            return None

        return 'true' if value else 'false'

    def clean(self, text):
        if not text:
            return None

        return text == 'true'


class DateTime(Base):
    """
    An ISO 8601 formatted, UTC (eg. 2008-01-23T04:56:22Z)
    date-time [saml-core § 1.3.3].
    """

    def prepare(self, value):
        return value.isoformat() if value is not None else None

    def clean(self, text):
        if text is not None:
            return parse_datetime(text, fuzzy=False)
