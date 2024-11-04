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
        if transactionId is None:
            raise NetworkException
        return TransactionResult(True, 200, "Refunded successfully.", TransactionStatus.COMPLETED)

    def getStatus(self, transactionId: str) -> TransactionStatus:
        if transactionId is None:
            raise NetworkException
        return TransactionStatus.COMPLETED


class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
        self.logger = Logger()
    
    def processPayment(self, userId: str, amount: float) -> TransactionResult:
        try:
            result = self.gateway.charge(userId, amount)
            if result.success:
                self.logger.loginfo(f"Payment successful: {result.transactionId}")
            else:
                self.logger.logerror(f"Payment failed: {result.message}")
            return result
        except (NetworkException, PaymentException) as e:
            self.logger.logerror(f"Payment processing error: {str(e)}")
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
    

class MockPaymentGateway(PaymentGateway):
    def charge(self, userId: str, amount: float) -> TransactionResult:
        if amount < 0:
            raise PaymentException("Negative payment.")
        if amount > 20000:
            raise PaymentException("No cash.")
        if userId is None:
            raise NetworkException("Network payment failed.")
        return TransactionResult(True, 100, "Charged successfully.", TransactionStatus.COMPLETED)
        
    def refund(self, transactionId: str) -> TransactionResult:
        return TransactionResult(True, 200, "Refunded successfully.", TransactionStatus.COMPLETED)
    	
    def getStatus(self, transactionId: str) -> TransactionStatus:
        return TransactionStatus.COMPLETED


class Logger:
    def __init__(self):
        self.infos = []
        self.errors = []
        
    def loginfo(self, log):
        self.infos.append(log)
        
    def logerror(self, log):
        self.errors.append(log)


class TDDTests:
    def __init__(self):
        self.mock = MockPaymentGateway()
        self.sut = PaymentProcessor(self.mock)
        
    def winProcess(self):
        self.mock = MockPaymentGateway()
        self.sut = PaymentProcessor(self.mock)
        #Given
        want = TransactionResult(True, "", "", TransactionStatus.COMPLETED)
        #When
        got = self.sut.processPayment("123",40)
        #Then
        assert(want.success==got.success)
    
    def failProcessNeg(self):
        self.mock = MockPaymentGateway()
        self.sut = PaymentProcessor(self.mock)
        #Given
        want = "Payment processing error: Negative payment."
        #When
        self.sut.processPayment("123",-40)
        got = self.sut.logger.errors[-1]
        #Then
        assert(want==got)
        
    def failProcessNet(self):
        self.mock = MockPaymentGateway()
        self.sut = PaymentProcessor(self.mock)
        #Given
        want = "Payment processing error: Network payment failed."
        #When
        self.sut.processPayment(None,10)
        got = self.sut.logger.errors[-1]
        #Then
        assert(want==got)
        
    def failProcessCash(self):
        self.mock = MockPaymentGateway()
        self.sut = PaymentProcessor(self.mock)
        #Given
        want = "Payment processing error: No cash."
        #When
        self.sut.processPayment("123", 99999)
        got = self.sut.logger.errors[-1]
        #Then
        assert(want==got)
        
    def 
 
 
a = TDDTests()
a.winProcess()
a.failProcessNeg()
a.failProcessNet()
a.failProcessCash()
