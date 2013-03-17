import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class AssertionTest(unittest.TestCase):

    def test_simple(self):
        self.a = saml.Assertion()
        self.a.subject = saml.Subject(id=saml.NameID('12345'))
        self.a.subject.id.format = saml.NameID.Format.EMAIL
        self.a.subject.confirm = saml.SubjectConfirmation()
        self.a.subject.confirm.data = saml.SubjectConfirmationData()
        self.a.subject.confirm.data.address = "127.0.0.1"
        self.a.subject.confirm.data.in_response_to = "saml://crm"
        self.a.subject.confirm.data.not_before = datetime.utcnow()
        self.a.subject.confirm.data.not_on_or_after = datetime.utcnow()
        self.a.issuer = saml.Issuer("saml://concordus")
        self.a.statements = []
        self.a.statements.append(saml.AuthenticationStatement())
        self.a.statements[0].session_not_on_or_after = self.a.statements[0].instant + timedelta(minutes=2)
        self.a.statements[0].context = saml.AuthenticationContext()
        self.a.statements[0].context.reference = saml.AuthenticationContext.Reference.PREVIOUS_SESSION

        self.p = samlp.Response(assertion=self.a)
        self.p.issuer = saml.Issuer("saml://concordus")
        self.p.in_response_to = "saml://crm"
        self.p.status = samlp.Status()
        self.p.status.code = samlp.StatusCode()
        self.p.status.code.value = samlp.StatusCode.Value.SUCCESS
        self.p.status.message = "Success; yes, that is all."

        self.x = samlp.Response.serialize(self.p)
        self.s = etree.tostring(self.x)

        #print self.a

        # print(self.s)
        self.e = etree.XML(self.s)
        self.c = samlp.Response.deserialize(self.e)
        # import ipdb; ipdb.set_trace()
        print(self.c.assertion.subject.id.text)
        # print('--------------------------')
        self.x2 = samlp.Response.serialize(self.c)
        self.s2 = etree.tostring(self.x2)
        # raise Exception()
        # print(self.s2)
        self.s2 = etree.tostring(self.x2)
        self.assertEquals(self.s, self.s2, "XML doesn't match")

    def test_text(self):
        text = '''
<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ID="_08dc80934b4246d7949032c33896e7b4" IssueInstant="2013-03-17T20:41:05Z" Version="2.0" InResponseTo="_5c0ea65029c246ff953397eed09f5e85">
    <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" Format="urn:oasis:names:tc:SAML:1.0:nameid-format:entity">saml://identity</saml:Issuer>
    <samlp:Status>
      <samlp:StatusCode>urn:oasis:names:tc:SAML:2.0:status:Success</samlp:StatusCode>
    </samlp:Status>
    <saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="_0d43ee138d304cfdbf8d131400296bf7" IssueInstant="2013-03-17T20:41:05Z" Version="2.0">
      <saml:Issuer Format="urn:oasis:names:tc:SAML:1.0:nameid-format:entity">saml://identity</saml:Issuer>
      <saml:Subject>
         <saml:NameID Format="urn:oasis:names:tc:SAML:1.0:nameid-format:persistent">04c6f9c9-81af-406b-a62e-99beed5020f0</saml:NameID>
         <saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
            <saml:SubjectConfirmationData NotBefore="2013-03-17T20:41:05Z" NotOnOrAfter="2013-03-17T21:41:05Z" Recipient="http://localhost:8000/saml/portal/acs" />
         </saml:SubjectConfirmation>
      </saml:Subject>
      <saml:AuthnStatement AuthnInstant="2013-03-17T20:41:05Z">
         <saml:AuthnContext>
            <saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml:AuthnContextClassRef>
         </saml:AuthnContext>
      </saml:AuthnStatement>
    </saml:Assertion>
</samlp:Response>
        '''

        xml = etree.XML(text)
        response = samlp.Response.deserialize(xml)

        self.assertEquals(response.issuer.text, 'saml://identity')
        self.assertEquals(response.assertion.id, '_0d43ee138d304cfdbf8d131400296bf7')
        self.assertEquals(response.assertion.subject.id.text, '04c6f9c9-81af-406b-a62e-99beed5020f0')
