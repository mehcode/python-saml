from lxml import etree
from saml import schema
from saml.schema import saml, samlp
from datetime import datetime, timedelta

a = saml.Assertion()
a.subject = saml.Subject()
a.subject.id = saml.NameID("leckey.ryan@gmail.com")
a.subject.id.format = saml.NameID.Format.EMAIL
a.subject.confirm = saml.SubjectConfirmation()
a.subject.confirm.method = "..bearer.."
a.subject.confirm.data = saml.SubjectConfirmationData()
a.subject.confirm.data.address = "127.0.0.1"
a.subject.confirm.data.in_response_to = "saml://crm"
a.subject.confirm.data.not_before = datetime.utcnow()
a.subject.confirm.data.not_on_or_after = datetime.utcnow()
a.issuer = saml.Issuer("saml://concordus")
a.statements = []
a.statements.append(saml.AuthnStatement())
a.statements[0].session_not_on_or_after = a.statements[0].instant + timedelta(minutes=2)
a.statements[0].context = saml.AuthnContext()
a.statements[0].context.class_ref = saml.AuthnContext.ClassRef.PREVIOUS_SESSION

p = samlp.Response(assertion=a)
p.in_response_to = "saml://crm"
p.status = samlp.Status()
p.status.code = samlp.StatusCode()
p.status.code.value = samlp.StatusCode.Value.SUCCESS
p.status.message = "Success; yes, that is all."

s = etree.tostring(schema.Element(0, samlp.Response).toxml(p), pretty_print=True)
print(s.decode('utf-8'))

r = samlp.AuthnRequest()
r.issuer = saml.Issuer("saml://crm")

s = etree.tostring(schema.Element(0, samlp.AuthnRequest).toxml(r), pretty_print=True)
print(s.decode('utf-8'))

