import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class ArtifactResponseTest(unittest.TestCase):
    def setUp(self):
        self.a = samlp.ArtifactResponse()
        #self.a.in_response_to = "_cce4ee768ed970b601f680f697989d14"
        #self.a.status = samlp.Status()
        #self.a.status.code = samlp.StatusCode()
       # self.a.status.code.value = samlp.StatusCode.Value.SUCCESS
       # self.a.
        self.x = samlp.ArtifactResponse.serialize(self.a)
        self.a = etree.tostring(self.x, pretty_print=True)


    def runTest(self):
        #print self.a

        print(self.a)
        self.e = etree.XML(self.a)
        self.c = samlp.ArtifactResponse.deserialize(self.e)
        print('--------------------------')
        self.x2 = samlp.ArtifactResponse.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)

        print(self.s2)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.a, self.s2, "XML doesn't match")


