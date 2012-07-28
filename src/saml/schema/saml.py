""" \file saml/schema/saml.py
\brief Defines the XML data types for SAML2 in the saml namespace.

\author Ryan Leckey (mehcode) leckey.ryan@gmail.com

\copyright Copyright © 2012 Concordus Applications, Inc.
           \n \n
           Permission is hereby granted, free of charge, to any person
           obtaining a copy of this software and associated documentation
           files (the "Software"), to deal in the Software without restriction,
           including without limitation the rights to use, copy, modify, merge,
           publish, distribute, sublicense, and/or sell copies of the Software,
           and to permit persons to whom the Software is furnished to do so,
           subject to the following conditions:
           \n \n
           The above copyright notice and this permission notice shall be
           included in all copies or substantial portions of the Software.
           \n \n
           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
           NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
           BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
           ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
           CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
           SOFTWARE.
"""
import abc
from lxml.builder import ElementMaker


## XML schema namespace URI.
NAMESPACE = "urn:oasis:names:tc:SAML:2.0:assertion"


## Instance of ElementMaker tailored to this namespace; used to
## instantiate XML elements.
_E = ElementMaker(namespace=NAMESPACE, nsmap={"saml": NAMESPACE})


class Type:
    def __init__(self):
        pass


class Element:
    @classmethod
    def fromxml(cls, xml):
        pass

    def toxml(self):
        """
        Generates an XML representation of this element from its defined
        attributes and content.
        """


class Attribute:
    pass


class AttributeGroup:
    pass


class IDNameQualifiers(AttributeGroup):

    class NameQualifier(Attribute):
        pass

    class SPNameQualifier(Attribute):
        pass

    attributes = [
        NameQualifier,
        SPNameQualifier]


class BaseIDAbstractType(Type):
    """
    Provides an extension point that allows applications to add new kinds of
    identifiers.
    """

    __metaclass__ = abc.ABCMeta

    attribute_groups = [IDNameQualifiers]


class NameIDType(BaseIDAbstractType):
    """
    Used when an element serves to represent an entity by a string-valued name.
    It is a more restricted form of identifier than the <BaseID> element and
    is the type underlying both the <NameID> and <Issuer> elements.

    In addition to the string content containing the actual identifier, it
    provides the following optional attributes.
    """

    class Format(Attribute):
        """
        A URI reference representing the classification of string-based
        identifier information. See Section 8.3 for the SAML-defined URI
        references that MAY be used as the value of the Format attribute and
        their associated descriptions and processing rules. Unless otherwise
        specified by an element based on this type, if no Format value is
        provided, then the value \ref unspecified is in effect.

        When a Format value other than one specified in Section 8.3 is used,
        the content of an element of this type is to be interpreted according
        to the definition of that format as provided outside of this
        specification. If not otherwise indicated by the definition of the
        format, issues of anonymity, pseudonymity, and the persistence of the
        identifier with respect to the asserting and relying parties
        are implementation-specific.
        """

        ## The interpretation of the attribute name is left to individual
        ## implementations.
        UNSPECIFIED = "urn:oasis:names:tc:SAML:1.0:nameid-format:unspecified"

        ## Indicates that the content of the element is in the form of an email
        ## address.
        EMAIL = "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"

        ## Indicates that the content of the element is in the form specified
        ## for the contents of the <ds:X509SubjectName> element in the XML
        ## Signature Recommendation [XMLSig].
        X509 = "urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName"

        ## Indicates that the content of the element is a Windows domain
        ## qualified name.
        WINDOWS = (
            "urn:oasis:names:tc:SAML:1.1:nameid-format"
            ":WindowsDomainQualifiedName")

        ## Indicates that the content of the element is in the form of a
        ## Kerberos principal name using the format name[/instance]@REALM.
        KEREBOS = "urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos"

        ## Indicates that the content of the element is the identifier of an
        ## entity that provides SAML-based services.
        ENTITY = "urn:oasis:names:tc:SAML:2.0:nameid-format:entity"

        ## Indicates that the content of the element is a persistent opaque
        ## identifier for a principal that is specific to an identity provider
        ## and a service provider or affiliation of service providers.
        PERSISTENT = "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"

        ## Indicates that the content of the element is an identifier with
        ## transient semantics and SHOULD be treated as an opaque and
        ## temporary value by the relying party.
        TRANSIENT = "urn:oasis:names:tc:SAML:2.0:nameid-format:transient"

    class SPProvidedID(Attribute):
        """
        A name identifier established by a service provider or affiliation of
        providers for the entity, if different from the primary name
        identifier given in the content of the element.
        """

    attributes = [
        Format,
        SPProvidedID]

    content = str


class NameID(Element, NameIDType):
    """
    Is of type NameIDType (see Section 2.2.2), and is used in various SAML
    assertion constructs such as the <Subject> and <SubjectConfirmation>
    elements, and in various protocol messages
    """
