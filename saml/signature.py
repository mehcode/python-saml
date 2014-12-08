# -*- coding: utf-8 -*-


def sign(xml, stream, password=None):
    # Import xmlsec here to delay initializing the C library in
    # case we don't need it.
    import xmlsec

    # Resolve the SAML/2.0 element in question.
    from saml.schema.base import _element_registry
    element = _element_registry.get(xml.tag)

    # Create a signature template for RSA-SHA1 enveloped signature.
    signature_node = xmlsec.template.create(
        xml,
        xmlsec.Transform.EXCL_C14N,
        xmlsec.Transform.RSA_SHA1)

    # Add the <ds:Signature/> node to the document.
    xml.insert(element.meta.signature_index, signature_node)

    # Add the <ds:Reference/> node to the signature template.
    ref = xmlsec.template.add_reference(
        signature_node, xmlsec.Transform.SHA1)

    # Add the enveloped transform descriptor.
    xmlsec.template.add_transform(ref, xmlsec.Transform.ENVELOPED)

    # Create a digital signature context (no key manager is needed).
    ctx = xmlsec.SignatureContext()

    # Load private key (assuming that there is no password).
    key = xmlsec.Key.from_memory(stream, xmlsec.KeyFormat.PEM)

    # Set the key on the context.
    ctx.key = key

    # Sign the template.
    ctx.sign(signature_node)


def verify(xml, stream):
    # Import xmlsec here to delay initializing the C library in
    # case we don't need it.
    import xmlsec

    # Find the <Signature/> node.
    signature_node = xmlsec.tree.find_node(xml, xmlsec.Node.SIGNATURE)

    # Create a digital signature context (no key manager is needed).
    ctx = xmlsec.SignatureContext()

    # Load the public key.
    key = xmlsec.Key.from_memory(stream, xmlsec.KeyFormat.PEM)

    # Set the key on the context.
    ctx.key = key

    # Verify the signature.
    return ctx.verify(signature_node)
