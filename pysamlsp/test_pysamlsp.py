import unittest
from expecter import expect
from datetime import datetime
from lxml import etree
import string
from pysamlsp import *

def setUpmodule():
  pass

class TestUtilityFunctions(unittest.TestCase):
  def test_iso_now_no_microseconds(self):
    dt = datetime(2013, 4, 17, 14, 15, 53, 32711)
    expect(iso_no_microseconds(dt)) == '2013-04-17T14:15:53'

class TestPysamlspAuthnRequestRoot(unittest.TestCase):
  def test_the_root_element_namespace(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar.tag) == '{urn:oasis:names:tc:SAML:2.0:protocol}AuthnRequest'
  def test_the_root_ProtocolBinding_attribute(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar.get('ProtocolBinding')) == 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'
  def test_the_root_Version_attribute(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar.get('Version')) == '2.0'
  def test_the_root_IssueInstant_attribute(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar.get('IssueInstant')) == iso_no_microseconds(datetime.utcnow())
  def test_the_root_ID_attribute(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(all(c in string.hexdigits for c in ar.get('ID')))
    expect(len(ar.get('ID'))) == 32
  def test_the_root_AssertionConsumerServiceURL_attribute(self):
    sp = Pysamlsp({'assertion_consumer_service_url': 'http://localhost'})
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar.get('AssertionConsumerServiceURL')) == 'http://localhost'

class TestPysamlspIssuerElement(unittest.TestCase):
  def test_the_element_namespace(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar[0].tag) == '{urn:oasis:names:tc:SAML:2.0:assertion}Issuer'
  def test_the_element_text(self):
    sp = Pysamlsp({'issuer': 'http://localhost/SAML'})
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar[0].text) == 'http://localhost/SAML'

class TestPysamlspRequestedAuthnContextElement(unittest.TestCase):
  def test_the_element_namespace(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar[1].tag) == \
      '{urn:oasis:names:tc:SAML:2.0:protocol}RequestedAuthnContext'
  def test_the_element_Comparison_attribute(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar[1].get('Comparison')) == 'exact'
  def test_the_child_element_text(self):
    sp = Pysamlsp()
    ar = etree.fromstring(sp.authnrequest_maker())
    expect(ar[1][0].text) == \
      'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport'