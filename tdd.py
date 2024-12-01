from enum import Enum


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionResult:
    def __init__(
        self,
        success: bool,
        transactionId: str,
        message: str = "",
        status: TransactionStatus = TransactionStatus.PENDING,
    ):
        self.success = success
        self.transactionId = transactionId
        self.message = message
        self.status = status


class NetworkException(Exception):
    pass


class PaymentException(Exception):
    pass


class RefundException(Exception):
    pass


class Logger:
    def __init__(self):
        self.infos = []
        self.errors = []

    def loginfo(self, log):
        self.infos.append(log)

    def logerror(self, log):
        self.errors.append(log)


# Klasa interfejs
class PaymentGateway:
    def charge(self, userId: str, amount: float) -> TransactionResult:
        return TransactionResult(False, "", TransactionStatus.FAILED)

    def refund(self, transactionId: str) -> TransactionResult:
        return TransactionResult(False, "", TransactionStatus.FAILED)

    def getStatus(self, transactionId: str) -> TransactionStatus:
        return TransactionResult(False, "", TransactionStatus.FAILED)


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
            return TransactionResult(False, "", status=TransactionStatus.FAILED)

    def refundPayment(self, transactionId: str) -> TransactionResult:
        try:
            result = self.gateway.refund(transactionId)
            if result.success:
                self.logger.loginfo(f"Refund successful: {result.transactionId}")
            else:
                self.logger.logerror(f"Refund failed: {result.message}")
            return result
        except (NetworkException, RefundException) as e:
            self.logger.logerror(f"Refund processing error: {str(e)}")
            return TransactionResult(False, "", status=TransactionStatus.FAILED)

    def getPaymentStatus(self, transactionId: str) -> TransactionStatus:
        try:
            return self.gateway.getStatus(transactionId)
        except NetworkException as e:
            self.logger.logerror(f"Error getting payment status: {str(e)}")
            return TransactionStatus.FAILED
