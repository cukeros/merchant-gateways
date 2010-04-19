
from merchant_gateways.billing.gateways.authorize_net import AuthorizeNet  #  test target is _always_ first line!
from merchant_gateways.billing.avs_result import AVSResult
from merchant_gateways.billing.cvv_result import CVVResult
from merchant_gateways.billing.credit_card import CreditCard
from tests.test_helper import *

#  TODO  rename the outer folder

#  TODO  all them options gotta be... OPTIONAL!!

#  TODO  require all required parameters

#  TODO  rename MerchantGatewaysTestSuite

class AuthorizeNetTests(MerchantGatewaysTestSuite, MerchantGatewaysTestSuite.CommonTests):

    def gateway_type(self):
        return AuthorizeNet

    def mock_webservice(self, response):
        self.mock_get_webservice(response)  #  TODO  is this REALLY a "get"??

    def assert_successful_authorization(self):

        # TODO  assert the response is None if we epic-fail (oh, and trap exceptions)

        self.gateway.get_webservice.assert_called_with(
                ('https://test.authorize.net/gateway/transact.dll?x_login=X&x_invoice_num=%i&' % self.options['order_id']) +
                'x_last_name=Granger&x_card_code=None&x_card_num=4242424242424242&x_amount=1.00&x_delim_char=%2C&x_tran_key=Y&' +
                'x_encap_char=%24&x_version=3.1&x_first_name=Hermione&x_exp_date=1290&x_delim_data=TRUE&x_relay_response=FALSE&' +
                'x_type=AUTH_ONLY&x_description=Chamber+of+Secrets&x_test_request=TRUE', {}
                )  #  TODO  beautify the response, via assert_params

        #~ assert response = self.gateway.authorize(self.amount, self.credit_card)

        # TODO  test these        print self.response.params
        #        self.assertEqual('508141794', self.response.params['authorization'])  #  TODO  also self.response.authorization
        self.assertEqual('508141794', self.response.authorization)

    def assert_failed_authorization(self):
        self.assertEqual('508141794', self.response.authorization)  # uh, we authorize failure around here?

    def assert_successful_purchase(self):  #  TODO  abstract me

        self.assert_success()  #  TODO  what's in the response? and why a PayflowRequest inherits Request but a AuthorizeNet Response IS a Response?

          #  TODO  who set the amount? Why ain't it 42.95?

        self.gateway.get_webservice.assert_called_with(
                ('https://test.authorize.net/gateway/transact.dll?x_login=X&x_invoice_num=%i&x_trans_id=Y&' % self.options['order_id']) + \
                  'x_last_name=Granger&x_card_code=None&x_card_num=4242424242424242&x_amount=1.00' + \
                  '&x_delim_char=%2C&x_tran_key=Y&x_encap_char=%24&x_version=3.1&x_first_name=Hermione&' + \
                  'x_exp_date=1290&x_delim_data=TRUE&x_relay_response=FALSE&x_type=AUTH_CAPTURE&' + \
                  'x_description=&x_test_request=TRUE', {}
                )  #  TODO  beautify the response, and constrain the order of the params

    def test_add_description(self):
        result = {}
        self.gateway.order_id = 42
        self.gateway.add_invoice(result, { 'description': 'Cornish Pixies' })
        self.assertEqual('Cornish Pixies', result['description'])

    def successful_authorization_response(self):
        return '$1$,$1$,$1$,$This transaction has been approved.$,$advE7f$,$Y$,$508141794$,$5b3fe66005f3da0ebe51$,$$,$1.00$,' + \
                      '$CC$,$auth_only$,$$,$Longbob$,$Longsen$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,' + \
                        '$2860A297E0FE804BCB9EF8738599645C$,$P$,$2$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$'

    def successful_purchase_response(self):
        return '$1$,$1$,$1$,$This transaction has been approved.$,$d1GENk$,$Y$,$508141795$,$32968c18334f16525227$,' + \
                      '$Store purchase$,$1.00$,$CC$,$auth_capture$,$$,$Longbob$,$Longsen$,' + \
                      '$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,' + \
                      '$269862C030129C1173727CC10B1935ED$,$P$,$2$,' + \
                      '$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$'

    '''  def test_add_address_outsite_north_america
        result = {}

        self.gateway.send(:add_address, result, :billing_address => {:address1 => '164 Waverley Street', :country => 'DE', :state => ''} )

        assert_equal ["address", "city", "company", "country", "phone", "state", "zip"], result.stringify_keys.keys.sort
        assert_equal 'n/a', result[:state]
        assert_equal '164 Waverley Street', result[:address]
        assert_equal 'DE', result[:country]
      end

      def test_add_address
        result = {}

        self.gateway.send(:add_address, result, :billing_address => {:address1 => '164 Waverley Street', :country => 'US', :state => 'CO'} )

        assert_equal ["address", "city", "company", "country", "phone", "state", "zip"], result.stringify_keys.keys.sort
        assert_equal 'CO', result[:state]
        assert_equal '164 Waverley Street', result[:address]
        assert_equal 'US', result[:country]

      end

      def test_add_invoice
        result = {}
        self.gateway.send(:add_invoice, result, :order_id => '#1001')
        assert_equal '#1001', result[:invoice_num]
      end

      def test_add_duplicate_window_without_duplicate_window
        result = {}
        ActiveMerchant::Billing::AuthorizeNetGateway.duplicate_window = nil
        self.gateway.send(:add_duplicate_window, result)
        assert_nil result[:duplicate_window]
      end

      def test_add_duplicate_window_with_duplicate_window
        result = {}
        ActiveMerchant::Billing::AuthorizeNetGateway.duplicate_window = 0
        self.gateway.send(:add_duplicate_window, result)
        assert_equal 0, result[:duplicate_window]
      end

      def test_purchase_is_valid_csv
       params = { :amount => '1.01' }

       self.gateway.send(:add_creditcard, params, self.credit_card)

       assert data = self.gateway.send(:post_data, 'AUTH_ONLY', params)
       assert_equal post_data_fixture.size, data.size
      end

      def test_purchase_meets_minimum_requirements
        params = {
          :amount => "1.01",
        }

        self.gateway.send(:add_creditcard, params, self.credit_card)

        assert data = self.gateway.send(:post_data, 'AUTH_ONLY', params)
        minimum_requirements.each do |key|
          assert_not_nil(data =~ /x_#{key}=/)
        end
      end

      def test_successful_credit
        self.gateway.expects(:ssl_post).returns(successful_purchase_response)
        assert response = self.gateway.credit(self.amount, '123456789', :card_number => self.credit_card.number)
        assert_success response
        assert_equal 'This transaction has been approved', response.message
      end

      def test_failed_credit
        self.gateway.expects(:ssl_post).returns(failed_credit_response)

        assert response = self.gateway.credit(self.amount, '123456789', :card_number => self.credit_card.number)
        assert_failure response
        assert_equal 'The referenced transaction does not meet the criteria for issuing a credit', response.message
      end

      def test_supported_countries
        assert_equal ['US'], AuthorizeNetGateway.supported_countries
      end

      def test_supported_card_types
        assert_equal [:visa, :master, :american_express, :discover], AuthorizeNetGateway.supported_cardtypes
      end

      def test_failure_without_response_reason_text
        assert_nothing_raised do
          assert_equal '', self.gateway.send(:message_from, {})
        end
      end

      def test_response_under_review_by_fraud_service
        self.gateway.expects(:ssl_post).returns(fraud_review_response)

        response = self.gateway.purchase(self.amount, self.credit_card)
        assert_failure response
        assert response.fraud_review?
        assert_equal "Thank you! For security reasons your order is currently being reviewed", response.message
      end

      def test_avs_result
        self.gateway.expects(:ssl_post).returns(fraud_review_response)

        response = self.gateway.purchase(self.amount, self.credit_card)
        assert_equal 'X', response.avs_result['code']
      end

      def test_cvv_result
        self.gateway.expects(:ssl_post).returns(fraud_review_response)

        response = self.gateway.purchase(self.amount, self.credit_card)
        assert_equal 'M', response.cvv_result['code']
      end

      # ARB Unit Tests

      def test_successful_recurring
        self.gateway.expects(:ssl_post).returns(successful_recurring_response)

        response = self.gateway.recurring(self.amount, self.credit_card,
          :billing_address => address.merge(:first_name => 'Jim', :last_name => 'Smith'),
          :interval => {
            :length => 10,
            :unit => :days
          },
          :duration => {
            :start_date => Time.now.strftime("%Y-%m-%d"),
            :occurrences => 30
          }
       )

        assert_instance_of Response, response
        assert response.success?
        assert response.test?
        assert_equal self.subscription_id, response.authorization
      end

      def test_successful_update_recurring
        self.gateway.expects(:ssl_post).returns(successful_update_recurring_response)

        response = self.gateway.update_recurring(:subscription_id => self.subscription_id, :amount => self.amount * 2)

        assert_instance_of Response, response
        assert response.success?
        assert response.test?
        assert_equal self.subscription_id, response.authorization
      end

      def test_successful_cancel_recurring
        self.gateway.expects(:ssl_post).returns(successful_cancel_recurring_response)

        response = self.gateway.cancel_recurring(self.subscription_id)

        assert_instance_of Response, response
        assert response.success?
        assert response.test?
        assert_equal self.subscription_id, response.authorization
      end

      def test_expdate_formatting
        assert_equal '2009-09', self.gateway.send(:arb_expdate, credit_card('4111111111111111', :month => "9", :year => "2009"))
        assert_equal '2013-11', self.gateway.send(:arb_expdate, credit_card('4111111111111111', :month => "11", :year => "2013"))
      end

      private
      def post_data_fixture
        'x_encap_char=%24&x_card_num=4242424242424242&x_exp_date=0806&x_card_code=123&x_type=AUTH_ONLY&x_first_name=Longbob&x_version=3.1&x_login=X&x_last_name=Longsen&x_tran_key=Y&x_relay_response=FALSE&x_delim_data=TRUE&x_delim_char=%2C&x_amount=1.01'
      end

      def minimum_requirements
        %w(version delim_data relay_response login tran_key amount card_num exp_date type)
      end

      def failed_credit_response
        '$3$,$2$,$54$,$The referenced transaction does not meet the criteria for issuing a credit.$,$$,$P$,$0$,$$,$$,$1.00$,$CC$,$credit$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$39265D8BA0CDD4F045B5F4129B2AAA01$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$'
      end

      def fraud_review_response
        "$4$,$$,$253$,$Thank you! For security reasons your order is currently being reviewed.$,$$,$X$,$0$,$$,$$,$1.00$,$$,$auth_capture$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$207BCBBF78E85CF174C87AE286B472D2$,$M$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$"
      end

      def successful_recurring_response
        <<-XML
    <ARBCreateSubscriptionResponse xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
      <refId>Sample</refId>
      <messages>
        <resultCode>Ok</resultCode>
        <message>
          <code>I00001</code>
          <text>Successful.</text>
        </message>
      </messages>
      <subscriptionId>#{self.subscription_id}</subscriptionId>
    </ARBCreateSubscriptionResponse>
        XML
      end

      def successful_update_recurring_response
        <<-XML
    <ARBUpdateSubscriptionResponse xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
      <refId>Sample</refId>
      <messages>
        <resultCode>Ok</resultCode>
        <message>
          <code>I00001</code>
          <text>Successful.</text>
        </message>
      </messages>
      <subscriptionId>#{self.subscription_id}</subscriptionId>
    </ARBUpdateSubscriptionResponse>
        XML
      end

      def successful_cancel_recurring_response
        <<-XML
    <ARBCancelSubscriptionResponse xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
      <refId>Sample</refId>
      <messages>
        <resultCode>Ok</resultCode>
        <message>
          <code>I00001</code>
          <text>Successful.</text>
        </message>
      </messages>
      <subscriptionId>#{self.subscription_id}</subscriptionId>
    </ARBCancelSubscriptionResponse>
        XML
      end
    end
    '''

    def failed_authorization_response(self):
        return '$2$,$1$,$1$,$This transaction was declined.$,$advE7f$,$Y$,$508141794$,$5b3fe66005f3da0ebe51$,' + \
                      '$$,$1.00$,$CC$,$auth_only$,$$,$Longbob$,$Longsen$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,' + \
                      '$$,$$,$$,$$,$$,$$,$$,$$,$$,$2860A297E0FE804BCB9EF8738599645C$,$P$,$2$,$$,$$,$$,$$,$$,$$,' + \
                      '$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$,$$'