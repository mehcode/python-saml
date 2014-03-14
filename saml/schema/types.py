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

    @staticmethod
    def to_iso8601(when):
        text = when.strftime("%Y-%m-%dT%H:%M:%SZ")
        return text

    @staticmethod
    def from_iso8601(when):
        return parse_datetime(when)

    def prepare(self, value):
        return DateTime.to_iso8601(value) if value is not None else None

    def clean(self, text):
        if text is not None:
            return DateTime.from_iso8601(text)
