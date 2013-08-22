from saml import schema
import saml.schema.saml
from datetime import datetime
from lxml import etree
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))


def assert_node(x, y):
    assert x.tag == y.tag
    assert x.attrib == y.attrib
    assert x.text == y.text
    assert x.tail == y.tail
    assert len(x) == len(y)

    for i, j in zip(x, y):
        assert_node(i, j)


def compare(name, result):
    # Load the expected result.
    filename = path.join(BASE_DIR, 'expected', '%s.xml' % name)
    parser = etree.XMLParser(
        ns_clean=True, remove_blank_text=True, remove_comments=True)

    xml = etree.parse(filename, parser).getroot()

    # Resolve and compare the result against the expected.
    assert_node(xml, result)


def test_simple_assertion():
    # Create the assertion object.
    target = schema.saml.Assertion()
    target.id = 'b07b804c-7c29-ea16-7300-4f3d6f7928ac'
    target.issue_instant = datetime(2004, 12, 5, 9, 22, 5)
    target.issuer = schema.saml.Issuer('https://idp.example.org/SAML2')

    # Create a subject.
    target.subject = subject = schema.saml.Subject()
    subject.id = schema.saml.NameID('3f7b3dcf-1674-4ecd-92c8-1544f346baf8')
    subject.id.format = schema.saml.NameID.Format.TRANSIENT
    subject.confirmation = confirmation = schema.saml.SubjectConfirmation()
    confirmation.data = data = schema.saml.SubjectConfirmationData()
    data.in_response_to = 'aaf23196-1773-2113-474a-fe114412ab72'
    data.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    data.recipient = 'https://sp.example.com/SAML2/SSO/POST'

    # Create an authentication statement.
    statement = schema.saml.AuthenticationStatement()
    target.statements.append(statement)
    statement.authn_instant = datetime(2004, 12, 5, 9, 22, 0)
    statement.session_index = 'b07b804c-7c29-ea16-7300-4f3d6f7928ac'
    ref = schema.saml.AuthenticationContextReference
    statement.context.reference = ref.PASSWORD_PROTECTED_TRANSPORT

    # Create a authentication condition.
    target.conditions = conditions = schema.saml.Conditions()
    conditions.not_before = datetime(2004, 12, 5, 9, 17, 5)
    conditions.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    condition = schema.saml.AudienceRestriction()
    condition.audiences = 'https://sp.example.com/SAML2'
    conditions.condition = condition

    # Serialize it into XML.
    result = target.serialize()

    # Compare it against the expected result.
    compare('assertion-simple', result)
