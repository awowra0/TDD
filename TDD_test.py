import unittest
from unittest.mock import MagicMock, patch
from enum import Enum
import logging


class TransactionResult:
    def __init__(self, success: bool, transactionId: str, message: str = ""):
        self.success = success
        self.transactionId = transactionId
        self.message = message
 
   
class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


#Klasa interfejs
class PaymentGateway:
    def charge(self, userId: str, amount: float) -> TransactionResult:
        pass
        
    def refund(self, transactionId: str) -> TransactionResult:
        pass
    	
    def getStatus(self, transactionId: str) -> TransactionStatus:
        pass


class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def processPayment(self, userId: str, amount: float) -> TransactionResult:
        try:
            if amount < 0:
                raise PaymentException("Podano ujemną kwotę.")
            elif userId is None:
            	raise PaymentException("Nie podano użytkownika.")
            elif amount is None:
            	raise PaymentException("Nie podano kwoty.")
            result = self.gateway.charge(userId, amount)
            if result.success:
                logging.info(f"Payment successful: {result.transactionId}")
            else:
                logging.error(f"Payment failed: {result.message}")
            return result
        except (NetworkException, PaymentException) as e:
            logging.error(f"Payment processing error: {str(e)}")
            return TransactionResult(False, "")
    
    def refundPayment(self, transactionId: str) -> TransactionResult:
        if transactionId is None:
            raise NetworkException("Nie podano numeru transakcji")
        try:
            result = self.gateway.refund(transactionId)
            if result.success:
                logging.info(f"Refund successful: {result.transactionId}")
            else:
                logging.error(f"Refund failed: {result.message}")
            return result
        except (NetworkException, RefundException) as e:
            logging.error(f"Refund processing error: {str(e)}")
            return TransactionResult(False, "")
    	
    def getPaymentStatus(self, transactionId: str) -> TransactionStatus:
        if not transactionId:
            raise NetworkException("Nie podano numeru transakcji")
        try:
            return self.gateway.get_status(transactionId)
        except NetworkException as e:
            logging.error(f"Error getting payment status: {str(e)}")
            return TransactionStatus.FAILED
        

class NetworkException(Exception):
    pass
    
class PaymentException(Exception):
    pass
    
class RefundException(Exception):
    pass 
    
    
class TestPaymentProcessor(unittest.TestCase):

    def setUp(self):
        self.gateway_mock = MagicMock()
        self.processor = PaymentProcessor(self.gateway_mock)

    def test_process_payment_success(self):
        self.gateway_mock.charge.return_value = TransactionResult(True, "123", "Charged successfully.")
        result = self.processor.processPayment("user1", 100.0)
        self.assertTrue(result.success)
        self.assertEqual(result.transactionId, "123")
        self.gateway_mock.charge.assert_called_once_with("user1", 100.0)
        
    def test_process_payment_failure_no_funds(self):
        self.gateway_mock.charge.return_value = TransactionResult(False, "124", "Insufficient funds.")
        result = self.processor.processPayment("user1024", 191.0)
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Insufficient funds.")
        
        
    def test_refund_payment_success(self):
        self.gateway_mock.refund.return_value = TransactionResult(True, "555", "Refunded successfully.")
        result = self.processor.refundPayment("555")
        self.assertTrue(result.success)
        self.gateway_mock.refund.assert_called_once_with("555")
        

if __name__ == "__main__":
    unittest.main()
