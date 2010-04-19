

from mock import Mock
#  CONSIDER  django-test-extensions needs to work w/o django
import unittest
from pprint import pformat
from decimal import Decimal


class MerchantGatewaysUtilitiesTestSuite(unittest.TestCase):

    def mock_get_webservice(self, returns):
        self.gateway.get_webservice = Mock(return_value=returns)

    def mock_post_webservice(self, returns):
        self.gateway.post_webservice = Mock(return_value=returns)

    def assert_success(self):
        #  TODO assert is_test
        self.assertTrue(isinstance(self.response, self.gateway_response_type()))
        self.assertTrue(self.response.success, 'Response should not fail: ' + pformat(self.response.__dict__))

    def assert_failure(self):
        self.assertTrue(isinstance(self.response, self.gateway_response_type()))
            #~ clean_backtrace do
        self.assertFalse(self.response.success, 'Response should fail: ' + pformat(self.response.__dict__))

    def assert_raises_(self, except_cls, callable_, *args, **kw):  #  CONSIDER  merge with django-test-extensions' assert_raises?
        try:
            callable_(*args, **kw)
            assert False, "Callable should raise an exception"  #  TODO  assertFalse, with complete diagnostics
        except except_cls, e:
            return e

    def _xml_to_tree(self, xml, forgiving=False):
        from lxml import etree
        self._xml = xml

        if not isinstance(xml, basestring):
            self._xml = str(xml)  #  CONSIDER  tostring
            return xml

        if '<html' in xml[:200]:
            parser = etree.HTMLParser(recover=forgiving) #  ERGO uh, strict?
            return etree.HTML(str(xml), parser)
        else:
            parser = etree.XMLParser(recover=forgiving)
            return etree.XML(str(xml))

    def assert_xml(self, xml, xpath, **kw):
        'Check that a given extent of XML or HTML contains a given XPath, and return its first node'

        tree = self._xml_to_tree(xml, forgiving=kw.get('forgiving', False))
        nodes = tree.xpath(xpath)
        self.assertTrue(len(nodes) > 0, xpath + ' should match ' + self._xml)
        node = nodes[0]
        if kw.get('verbose', False):  self.reveal_xml(node)  #  "here have ye been? What have ye seen?"--Morgoth
        return node

    def reveal_xml(self, node):
        'Spews an XML node as source, for diagnosis'

        from lxml import etree
        print etree.tostring(node, pretty_print=True)  #  CONSIDER  does pretty_print work? why not?

    def deny_xml(self, xml, xpath):
        'Check that a given extent of XML or HTML does not contain a given XPath'

        tree = self._xml_to_tree(xml)
        nodes = tree.xpath(xpath)
        self.assertEqual(0, len(nodes), xpath + ' should not appear in ' + self._xml)

    def assert_match_xml(self, reference, sample):
        import re
        reference = re.sub(r'\n\s*', '\n', reference)
        sample = re.sub(r'\n\s*', '\n', sample)
        self.assertEqual(reference, sample, "\n%s\nshould match:%s" % (reference, sample))  #  CONSIDER  use XPath to rotorouter the two samples!

    def assert_none(self, *args, **kwargs):
        "assert you ain't nothin'"

        return self.assertEqual(None, *args, **kwargs)

    def assert_equal(self, *args, **kwargs):
        'Assert that two values are equal'

        return self.assertEqual(*args, **kwargs)

class MerchantGatewaysTestSuite(MerchantGatewaysUtilitiesTestSuite):

    def setUp(self):
        self.gateway = self.gateway_type()(is_test=True, login='X', password='Y')
        self.gateway.gateway_mode = 'test'
        self.amount = 100
        self.options = dict(order_id=1)  #  TODO  change me to Harry Potter's favorite number & pass all tests
        from merchant_gateways.billing.credit_card import CreditCard

        self.credit_card = CreditCard( number='4242424242424242',
                                       month='12',  year='2090',
                                       card_type='V',
                                       first_name='Hermione', last_name='Granger' )

        self.subscription_id = '100748'  #  TODO  use or lose this

    class CommonTests:

        def gateway_response_type(self):
            return self.gateway_type().Response

        def test_successful_authorization(self):
            self.mock_webservice(self.successful_authorization_response())
            self.options['description'] = 'Chamber of Secrets'
            self.response = self.gateway.authorize(self.amount, self.credit_card, **self.options)

    # TODO        assert self.response.is_test
            self.assert_successful_authorization()
            self.assert_success()
            self.assert_equal(repr(True), repr(self.response.is_test))

        def test_failed_authorization(self):
            self.mock_webservice(self.failed_authorization_response())
            self.response = self.gateway.authorize(self.amount, self.credit_card, **self.options)
            self.assert_failure()
            self.assert_failed_authorization()
            self.assert_equal(repr(True), repr(self.response.is_test))

        def test_successful_purchase(self):
            print self
            self.mock_get_webservice(self.successful_purchase_response())
            self.response = self.gateway.purchase(self.amount, self.credit_card, **self.options)
            self.assert_successful_purchase()

nil = None # C-;

import re
def grep(string,list):
    expr = re.compile(string)
    for text in list:
        match = expr.search(text)
        if match != None:
            print match.string