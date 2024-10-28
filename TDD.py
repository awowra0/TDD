from enum import Enum
import logging

class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def processPayment(userId: str, amount: float) -> TransactionResult:
        try:
            if amount < 0:
                raise PaymentException("Podano ujemną kwotę.")
            elif userId is None:
            	raise PaymentException("Nie podano użytkownika.")
            elif amount is None:
            	raise PaymentException("Nie podano kwoty.")
            res = self.gateway.charge(user_id, amount)
            if res.success:
                logging.info(f"Payment successful: {res.transaction_id}")
            else:
                logging.error(f"Payment failed: {res.message}")
            return res
        except (NetworkException, PaymentException) as e:
            logging.error(f"Payment processing error: {str(e)}")
            return TransactionResult(False, "")
    
    def refundPayment(transactionId: str) -> TransactionResult:
    	if transactionId is None:
    	    raise NetworkException("Nie podano numeru transakcji")
    	try:
            res = self.gateway.refund(transaction_id)
            if result.success:
                logging.info(f"Refund successful: {res.transaction_id}")
            else:
                logging.error(f"Refund failed: {res.message}")
            return res
        except (NetworkException, RefundException) as e:
            logging.error(f"Refund processing error: {str(e)}")
            return TransactionResult(False, "")
    	
    def getPaymentStatus(transactionId: str) -> TransactionStatus:
        if not transactionId:
            raise NetworkException("Nie podano numeru transakcji")
        try:
            return self.gateway.get_status(transaction_id)
        except NetworkException as e:
            logging.error(f"Error getting payment status: {str(e)}")
            return TransactionStatus.FAILED
        
        
#Klasa interfejs
class PaymentGateway:
    def charge(userId: str, amount: float) -> TransactionResult:
        pass
        
    def refund(transactionId: str) -> TransactionResult:
    	pass
    	
    def getStatus(transactionId: str) -> TransactionStatus:
    	pass
 
    	
class TransactionResult:
    def __init__(self, success: bool, transactionId: str, message: str = ""):
    	self.success = success
    	self.transactionId = transactionId
    	self.message = message
 
   
class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    
class NetworkException(Exception):
    pass
    
class PaymentException(Exception):
    pass
    
class RefundException(Exception):
    pass 
