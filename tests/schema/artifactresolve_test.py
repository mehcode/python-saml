import unittest
from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta
"""UNFINISHED"""

class ArtifactResolveTest(unittest.TestCase):
    def setUp(self):
        self.a = samlp.ArtifactResolve()
        self.a.destination = "https://sp.example.com/SAML2/ArtifactResolution"
        self.a.issuer = saml.Issuer("https://idp.example.org/SAML2")
        self.a.artifact = "AAQAAMh48/1oXIM+sDo7Dh2qMp1HM4IF5DaRNmDj6RdUmllwn9jJHyEgIi8="

        # BUG: IndexError: list index out of range
        #      If simple elements aren't set

        self.x = samlp.ArtifactResolve.serialize(self.a)
        self.a = etree.tostring(self.x, pretty_print=True)


    def runTest(self):
        #print self.a

        print(self.a)
        self.e = etree.XML(self.a)
        self.c = samlp.ArtifactResolve.deserialize(self.e)
        print('--------------------------')
        self.x2 = samlp.ArtifactResolve.serialize(self.c)
        self.s2 = etree.tostring(self.x2, pretty_print=True)

        print(self.s2)
        self.s2 = etree.tostring(self.x2, pretty_print=True)
        self.assertEquals(self.a, self.s2, "XML doesn't match")


