import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class LogoutRequestTest(unittest.TestCase):
    def setUp(self):
        self.a = samlp.LogoutRequest()
        self.a.not_on_or_after = datetime.now()
        self.a.reason = "leaving now."
        self.a.session = "1"
#        self.s.destination = 'http://example.com'

    def runTest(self):
        #print self.a

        self.x = samlp.LogoutRequest.serialize(self.a)
        self.s = etree.tostring(self.x, pretty_print=True)
        print(self.s)
        self.e = etree.XML(self.s)
        self.c = samlp.LogoutRequest.deserialize(self.e)
        print('--------------------------')
        self.x2 = samlp.LogoutRequest.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)

        print(self.s2)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.s, self.s2, "XML doesn't match")


