import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta


class AssertionTest(unittest.TestCase):
    def setUp(self):
        self.a = saml.Assertion()
        self.a.subject = saml.Subject()
        self.a.subject.id = saml.NameID("leckey.ryan@gmail.com")
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
        self.a.statements.append(saml.AuthenticationStatement())
        self.a.statements[1].session_not_on_or_after = self.a.statements[0].instant + timedelta(minutes=2)
        self.a.statements[1].context = saml.AuthenticationContext()
        self.a.statements[1].context.reference = saml.AuthenticationContext.Reference.PREVIOUS_SESSION
        self.a.statements.append(saml.AuthenticationStatement())
        self.a.statements[2].session_not_on_or_after = self.a.statements[0].instant + timedelta(minutes=2)
        self.a.statemeArtifactResponseTestnts[2].context = saml.AuthenticationContext()
        self.a.statements[2].context.reference = saml.AuthenticationContext.Reference.PREVIOUS_SESSION


    def runTest(self):
        #print self.a

        self.x = saml.Assertion.serialize(self.a)
        self.s = etree.tostring(self.x, pretty_print=True)
        print(self.s)
        self.e = etree.XML(self.s)
        self.c = saml.Assertion.deserialize(self.e)
        print('--------------------------')
        self.x2 = saml.Assertion.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.s, self.s2, "XML doesn't match")

        print(self.s2)

