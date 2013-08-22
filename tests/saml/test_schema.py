import saml
from saml import schema
from saml.schema import utils
from datetime import datetime
from lxml import etree
from os import path
from pytest import mark

BASE_DIR = path.abspath(path.dirname(__file__))


def strip(text):
    if not text:
        return None

    text = text.replace('\n', '')
    text = text.strip()

    return text if text else None


def assert_node(expected, result):
    assert expected.tag == result.tag
    assert expected.attrib == result.attrib
    assert strip(expected.text) == strip(result.text)
    assert strip(expected.tail) == strip(result.tail)
    assert len(expected) == len(result)

    for expected, result in zip(expected, result):
        assert_node(expected, result)


def build_assertion_simple():
    # Create the assertion object.
    target = schema.Assertion()
    target.id = 'b07b804c-7c29-ea16-7300-4f3d6f7928ac'
    target.issue_instant = datetime(2004, 12, 5, 9, 22, 5)
    target.issuer = 'https://idp.example.org/SAML2'

    # Create a subject.
    target.subject = subject = schema.Subject()
    subject.principal = '3f7b3dcf-1674-4ecd-92c8-1544f346baf8'
    subject.principal.format = schema.NameID.Format.TRANSIENT
    subject.confirmation = confirmation = schema.SubjectConfirmation()
    confirmation.data = data = schema.SubjectConfirmationData()
    data.in_response_to = 'aaf23196-1773-2113-474a-fe114412ab72'
    data.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    data.recipient = 'https://sp.example.com/SAML2/SSO/POST'
    del data.recipient
    data.recipient = 'https://sp.example.com/SAML2/SSO/POST'

    assert data.recipient == 'https://sp.example.com/SAML2/SSO/POST'

    # Create an authentication statement.
    statement = schema.AuthenticationStatement()
    target.statements.append(statement)
    statement.authn_instant = datetime(2004, 12, 5, 9, 22, 0)
    statement.session_index = 'b07b804c-7c29-ea16-7300-4f3d6f7928ac'
    ref = schema.AuthenticationContextReference.PASSWORD_PROTECTED_TRANSPORT
    statement.context.reference = ref

    # Create a authentication condition.
    target.conditions = conditions = schema.Conditions()
    conditions.not_before = datetime(2004, 12, 5, 9, 17, 5)
    conditions.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    condition = schema.AudienceRestriction()
    condition.audiences = 'https://sp.example.com/SAML2'
    conditions.condition = condition

    # Return the built object.
    return target


def build_authentication_request_simple():
    # Create the authentication request.
    target = schema.AuthenticationRequest()
    target.id = 'aaf23196-1773-2113-474a-fe114412ab72'
    target.issue_instant = datetime(2004, 12, 5, 9, 21, 59)
    target.assertion_consumer_service_index = 0
    target.attribute_consuming_service_index = 0
    target.issuer = 'https://sp.example.com/SAML2'

    # Add a name id policy to the request.
    target.policy = policy = schema.NameIDPolicy()
    policy.allow_create = True
    policy.format = schema.NameID.Format.TRANSIENT

    # Return the built object.
    return target


def build_artifact_resolve_simple():
    # Create the artifact resolution request.
    target = schema.ArtifactResolve()
    target.id = '_cce4ee769ed970b501d680f697989d14'
    target.issue_instant = datetime(2004, 12, 5, 9, 21, 58)
    target.issuer = 'https://idp.example.org/SAML2'
    target.artifact = '''
        AAQAAMh48/1oXIM+sDo7Dh2qMp1HM4IF5DaRNmDj6RdUmllwn9jJHyEgIi8=
    '''.strip()

    # Return the built object.
    return target


def build_artifact_response_simple():
    # Create the artifact response.
    target = schema.ArtifactResponse()
    target.id = '_d84a49e5958803dedcff4c984c2b0d95'
    target.in_response_to = '_cce4ee769ed970b501d680f697989d14'
    target.issue_instant = datetime(2004, 12, 5, 9, 21, 59)
    target.status.code.value = schema.StatusCode.SUCCESS

    # Create an authentication request to stuff inside of the artifact
    # response.
    target.message = message = schema.AuthenticationRequest()
    message.id = '_306f8ec5b618f361c70b6ffb1480eade'
    message.issue_instant = datetime(2004, 12, 5, 9, 21, 59)
    message.destination = 'https://idp.example.org/SAML2/SSO/Artifact'
    message.protocol = schema.Protocol.ARTIFACT
    message.issuer = 'https://sp.example.com/SAML2'
    message.assertion_consumer_service_url = (
        'https://sp.example.com/SAML2/SSO/Artifact')

    # Add a name id policy to the authentication request.
    message.policy = policy = schema.NameIDPolicy()
    policy.allow_create = False
    policy.format = schema.NameID.Format.EMAIL

    # Return the built object.
    return target


def build_response_simple():
    # Create the response.
    target = schema.Response()
    target.id = 'identifier_2'
    target.in_response_to = 'identifier_1'
    target.issue_instant = datetime(2004, 12, 5, 9, 22, 5)
    target.issuer = 'https://idp.example.org/SAML2'
    target.destination = 'https://sp.example.com/SAML2/SSO/POST'
    target.status.code.value = schema.StatusCode.SUCCESS

    # Create an assertion for the response.
    target.assertions = assertion = schema.Assertion()
    assertion.id = 'identifier_3'
    assertion.issue_instant = datetime(2004, 12, 5, 9, 22, 5)
    assertion.issuer = 'https://idp.example.org/SAML2'

    # Create a subject.
    assertion.subject = subject = schema.Subject()
    subject.principal = '3f7b3dcf-1674-4ecd-92c8-1544f346baf8'
    subject.principal.format = schema.NameID.Format.TRANSIENT
    subject.confirmation = confirmation = schema.SubjectConfirmation()
    confirmation.data = data = schema.SubjectConfirmationData()
    data.in_response_to = 'identifier_1'
    data.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    data.recipient = 'https://sp.example.com/SAML2/SSO/POST'

    # Create an authentication statement.
    statement = schema.AuthenticationStatement()
    assertion.statements.append(statement)
    statement.authn_instant = datetime(2004, 12, 5, 9, 22, 0)
    statement.session_index = 'identifier_3'
    ref = schema.AuthenticationContextReference.PASSWORD_PROTECTED_TRANSPORT
    statement.context.reference = ref

    # Create a authentication condition.
    assertion.conditions = conditions = schema.Conditions()
    conditions.not_before = datetime(2004, 12, 5, 9, 17, 5)
    conditions.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    condition = schema.AudienceRestriction()
    condition.audiences = 'https://sp.example.com/SAML2'
    conditions.condition = condition

    # Return the built object.
    return target


def build_logout_request_simple():
    # Create the request.
    target = schema.LogoutRequest()
    target.id = 'identifier_1'
    target.issue_instant = datetime(2008, 6, 3, 12, 59, 57)
    target.issuer = 'myhost'
    target.destination = 'https://idphost/adfs/ls/'
    target.principal = 'myemail@mydomain.com'
    target.principal.format = schema.NameID.Format.EMAIL
    target.principal.name_qualifier = 'https://idphost/adfs/ls/'
    target.session_index = '_0628125f-7f95-42cc-ad8e-fde86ae90bbe'

    # Return the built object.
    return target


def build_logout_response_simple():
    # Create the response.
    target = schema.LogoutResponse()
    target.id = 'identifier_2'
    target.in_response_to = 'identifier_1'
    target.issue_instant = datetime(2004, 12, 5, 9, 22, 5)
    target.issuer = 'https://idp.example.org/SAML2'
    target.destination = 'https://sp.example.com/SAML2/SLO/POST'
    target.status.code.value = schema.StatusCode.SUCCESS

    # Return the built object.
    return target


NAMES = [
    'assertion',
    'authentication-request',
    'response',
    'logout-request',
    'logout-response',
    'artifact-resolve',
    'artifact-response'
]


@mark.parametrize('name', NAMES)
def test_simple_serialize(name):
    # Load the expected result.
    filename = path.join(BASE_DIR, '%s-simple.xml' % name)
    parser = etree.XMLParser(
        ns_clean=True, remove_blank_text=True, remove_comments=True)
    expected = etree.parse(filename, parser).getroot()

    # Build the result.
    build_fn_name = ('build-%s-simple' % name).replace('-', '_')
    target = globals()[build_fn_name]()

    # Serialize the result into an XML object.
    result = target.serialize()

    # Resolve and compare the result against the expected.
    assert_node(expected, result)


@mark.parametrize('name', NAMES)
def test_simple_deserialize(name):
    # Load the result.
    filename = path.join(BASE_DIR, '%s-simple.xml' % name)
    parser = etree.XMLParser(
        ns_clean=True, remove_blank_text=True, remove_comments=True)
    target = etree.parse(filename, parser).getroot()

    # Build the expected result.
    build_fn_name = ('build-%s-simple' % name).replace('-', '_')
    expected = globals()[build_fn_name]().serialize()

    # Deserialize and subsequently serialize the target.
    cls_name = utils.pascalize(name)
    result = getattr(schema, cls_name).deserialize(target).serialize()

    # Compare the nodes.
    assert_node(expected, result)


NAMES = [
    'assertion',
    'response',
    'logout-response',
    'artifact-resolve',
    'artifact-response'
]


@mark.parametrize('name', NAMES)
def test_sign(name):
    # Load the expected result.
    filename = path.join(BASE_DIR, '%s-signed.xml' % name)
    expected = etree.parse(filename).getroot()

    # Build the result.
    build_fn_name = ('build-%s-simple' % name).replace('-', '_')
    target = globals()[build_fn_name]()

    # Serialize the result into an XML object.
    # Round-trips the XML to remove weird spacing.
    result = target.serialize()

    with open(path.join(BASE_DIR, 'rsakey.pem'), 'r') as stream:
        # Sign the result.
        saml.sign(result, stream)

    # print()
    # print(etree.tostring(result).decode('utf8'))
    # print()

    # Compare the nodes.
    assert_node(expected, result)


@mark.parametrize('name', NAMES)
def test_verify(name):
    # Load the SAML XML document to verify.
    filename = path.join(BASE_DIR, '%s-signed.xml' % name)
    expected = etree.parse(filename).getroot()

    # Sign the result.
    with open(path.join(BASE_DIR, 'rsapub.pem'), 'r') as stream:
        assert saml.verify(expected, stream)
