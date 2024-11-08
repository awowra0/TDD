from enum import Enum


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionResult:
    def __init__(self, success: bool, transactionId: str, message: str = "", status: TransactionStatus = "PENDING"):
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


# Klasa interfejs
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
            return TransactionResult(False, "", status="FAILED")

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
            return TransactionResult(False, "", status="FAILED")

    def getPaymentStatus(self, transactionId: str) -> TransactionStatus:
        try:
            return self.gateway.getStatus(transactionId)
        except NetworkException as e:
            self.logger.logerror(f"Error getting payment status: {str(e)}")
            return TransactionStatus.FAILED


# Interfejs do testów
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
        if transactionId is None:
            raise RefundException("Transaction not found.")
        if transactionId == "987":
            raise NetworkException("Network refund failed.")
        return TransactionResult(True, 200, "Refunded successfully.", TransactionStatus.COMPLETED)

    def getStatus(self, transactionId: str) -> TransactionStatus:
        if transactionId is None:
            raise NetworkException("No transaction found.")
        if transactionId == "123":
            raise NetworkException("Network status failed.")
        if transactionId == "1":
            return TransactionStatus.PENDING
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
        # Given
        want = TransactionResult(True, "", "", TransactionStatus.COMPLETED)
        # When
        got = self.sut.processPayment("123", 40)
        # Then
        assert (want.success == got.success)

    def failProcessNeg(self):
        # Given
        want = "Payment processing error: Negative payment."
        # When
        self.sut.processPayment("123", -40)
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)

    def failProcessNet(self):
        # Given
        want = "Payment processing error: Network payment failed."
        # When
        self.sut.processPayment(None, 10)
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)

    def failProcessCash(self):
        # Given
        want = "Payment processing error: No cash."
        # When
        self.sut.processPayment("123", 99999)
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)

    def winRefund(self):
        # Given
        want = TransactionResult(True, "", "", TransactionStatus.COMPLETED)
        # When
        got = self.sut.refundPayment("33")
        # Then
        assert (want.success == got.success)

    def failRefundNone(self):
        # Given
        want = "Refund processing error: Transaction not found."
        # When
        self.sut.refundPayment(None)
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)

    def failRefundNet(self):
        # Given
        want = "Refund processing error: Network refund failed."
        # When
        self.sut.refundPayment("987")
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)

    def winStatusCOM(self):
        # Given
        want = TransactionStatus.COMPLETED
        # When
        got = self.sut.getPaymentStatus("25")
        # Then
        assert (want == got)

    def winStatusPEN(self):
        # Given
        want = TransactionStatus.PENDING
        # When
        got = self.sut.getPaymentStatus("1")
        # Then
        assert (want == got)

    def failStatusNone(self):
        # Given
        want = "Error getting payment status: No transaction found."
        # When
        self.sut.getPaymentStatus(None)
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)

    def failStatusNet(self):
        # Given
        want = "Error getting payment status: Network status failed."
        # When
        self.sut.getPaymentStatus("123")
        got = self.sut.logger.errors[-1]
        # Then
        assert (want == got)


a = TDDTests()
a.winProcess()
a.failProcessNeg()
a.failProcessNet()
a.failProcessCash()
a.winRefund()
a.failRefundNone()
a.failRefundNet()
a.winStatusCOM()
a.winStatusPEN()
a.failStatusNone()
a.failStatusNet()
