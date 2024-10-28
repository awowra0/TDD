class PaymentProcessor:
    def processPayment(userId, amount):
        try:
            if amount < 0:
                raise PaymentException("Podano ujemną kwotę")
        except NetworkException:
            pass
        except PaymentException:
            pass
        #return TransactionResult
    
    def refundPayment(transactionId):
    	pass
    	#return TransactionResult
    	
    def getPaymentStatus(transactionId):
        pass
        #return TransactionStatus
        
        
class PaymentGateway:
    def charge(userId, amount):
        pass
        #return TransactionResult
        
    def refund(transactionId):
    	pass
    	#return TransactionResult
    	
    def getStatus(transactionId):
    	pass
    	#TransactionStatus
    	
class TransactionResult:
    def __init__(self, success, transactionId, message, TransactionStatus):
    	self.success = success
    	self.transactionId = transactionId
    	self.message = message
    	self.TransactionStatus = TransactionStatus
