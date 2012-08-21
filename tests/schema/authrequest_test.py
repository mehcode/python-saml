import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class AuthRequestTest(unittest.TestCase):
    def setUp(self):
        self.a = samlp.AuthenticationRequest()
        self.a.assertion_consumer_service_index = "0"
        self.a.attribute_consuming_service_index = "0"
        self.a.issuer = saml.Issuer("https://sp.example.com/SAML2")
        self.a.is_forced = True
        self.a.is_passive = True

        self.x = samlp.AuthenticationRequest.serialize(self.a)
        self.a = etree.tostring(self.x, pretty_print=True)


    def runTest(self):
        #print self.a

        print(self.a)
        self.e = etree.XML(self.a)
        self.c = samlp.AuthenticationRequest.deserialize(self.e)
        print('--------------------------')
        self.x2 = samlp.AuthenticationRequest.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)

        print(self.s2)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.a, self.s2, "XML doesn't match")


