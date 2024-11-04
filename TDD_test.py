import unittest
from unittest.mock import MagicMock, patch
from enum import Enum
import logging


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionResult:
    def __init__(self, success: bool, transactionId: str, message: str = "", status: TransactionStatus = "FAILED"):
        self.success = success
        self.transactionId = transactionId
        self.message = message
 
   
#class PaymentGatewayError(Enum):
#    NetworkException = "NetworkException"

#Klasa interfejs
class PaymentGateway:
    def charge(self, userId: str, amount: float) -> TransactionResult:
        pass
        
    def refund(self, transactionId: str) -> TransactionResult:
        pass
    	
    def getStatus(self, transactionId: str) -> TransactionStatus:
        pass


class TestPaymentGateway(PaymentGateway):
    def charge(self, userId: str, amount: float) -> TransactionResult:
        if amount < 0:
            raise PaymentException
        if userId is None:
            raise NetworkException
        return TransactionResult(True, 100, "Charged successfully.", TransactionStatus.COMPLETED)
        
    def refund(self, transactionId: str) -> TransactionResult:
        return TransactionResult(True, 200, "Refunded successfully.", TransactionStatus.COMPLETED)
    	
    def getStatus(self, transactionId: str) -> TransactionStatus:
        return TransactionStatus.COMPLETED

class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def processPayment(self, userId: str, amount: float) -> TransactionResult:
        try:
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
        
    def test_refund_payment_failure_due_to_nonexistent_transaction(self):
        self.gateway_mock.refund.return_value = TransactionResult(False, "153", "Transaction not found.")
        result = self.processor.refundPayment("153")
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Transaction not found.")

    def test_get_payment_status_success(self):
        self.gateway_mock.get_status.return_value = TransactionStatus.COMPLETED
        status = self.processor.getPaymentStatus("120")
        self.assertEqual(status, TransactionStatus.COMPLETED)
        self.gateway_mock.get_status.assert_called_once_with("120")

    def test_get_payment_status_network_exception(self):
        self.gateway_mock.get_status.side_effect = NetworkException("Network error.")
        status = self.processor.getPaymentStatus("1")
        self.assertEqual(status, TransactionStatus.FAILED)


if __name__ == "__main__":
    unittest.main()
