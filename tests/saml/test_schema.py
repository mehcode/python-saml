from saml import schema
from datetime import datetime
from lxml import etree
from os import path
from pytest import mark

BASE_DIR = path.abspath(path.dirname(__file__))


def assert_node(expected, result):
    assert expected.tag == result.tag
    assert expected.attrib == result.attrib
    assert expected.text == result.text
    assert expected.tail == result.tail
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
    subject.id = schema.NameID('3f7b3dcf-1674-4ecd-92c8-1544f346baf8')
    subject.id.format = schema.NameID.Format.TRANSIENT
    subject.confirmation = confirmation = schema.SubjectConfirmation()
    confirmation.data = data = schema.SubjectConfirmationData()
    data.in_response_to = 'aaf23196-1773-2113-474a-fe114412ab72'
    data.not_on_or_after = datetime(2004, 12, 5, 9, 27, 5)
    data.recipient = 'https://sp.example.com/SAML2/SSO/POST'

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


def build_authn_request_simple():
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


@mark.parametrize('name', [
    'assertion',
    'authn-request',
    'artifact-resolve',
    'artifact-response'])
def test_simple_serialize(name):
    # Load the expected result.
    filename = path.join(BASE_DIR, 'expected', '%s-simple.xml' % name)
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
