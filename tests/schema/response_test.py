import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class AssertionTest(unittest.TestCase):
    def setUp(self):
        self.a = saml.Assertion()
        self.a.subject = saml.Subject()
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

        self.p = samlp.Response(assertion=[self.a, self.a, self.a])
        self.p.issuer = saml.Issuer("saml://concordus")
        self.p.in_response_to = "saml://crm"
        self.p.status = samlp.Status()
        self.p.status.code = samlp.StatusCode()
        self.p.status.code.value = samlp.StatusCode.Value.SUCCESS
        self.p.status.message = "Success; yes, that is all."

        self.x = samlp.Response.serialize(self.p)
        self.s = etree.tostring(self.x, pretty_print=True)


    def runTest(self):
        #print self.a

        print(self.s)
        self.e = etree.XML(self.s)
        self.c = samlp.Response.deserialize(self.e)
        print('--------------------------')
        self.x2 = samlp.Response.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)

        print(self.s2)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.s, self.s2, "XML doesn't match")


