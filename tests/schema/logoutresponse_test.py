import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class LogoutResponseTest(unittest.TestCase):
    def setUp(self):
        self.a = samlp.LogoutResponse()
        self.a.in_response_to = "_cce4ee768ed970b601f680f697989d14"
        self.a.status = samlp.Status()
        self.a.status.code = samlp.StatusCode()
        self.a.status.code.value = samlp.StatusCode.Value.SUCCESS
        self.a.session = '1'

        self.p = samlp.LogoutResponse(assertion=[self.a, self.a, self.a])
        self.p.issuer = saml.Issuer("saml://concordus")
        self.p.in_response_to = "saml://crm"
        self.p.status = samlp.Status()
        self.p.status.code = samlp.StatusCode()
        self.p.status.code.value = samlp.StatusCode.Value.SUCCESS
        self.p.status.message = "Success; yes, that is all."

        self.x = samlp.LogoutResponse.serialize(self.p)
        self.s = etree.tostring(self.x, pretty_print=True)

    def runTest(self):
        #print self.a

        print(self.s)
        self.e = etree.XML(self.s)
        self.c = samlp.LogoutResponse.deserialize(self.e)
        print('--------------------------')
        self.x2 = samlp.LogoutResponse.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)

        print(self.s2)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.s, self.s2, "XML doesn't match")


