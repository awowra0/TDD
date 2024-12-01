from TDD import *


# Interface used for tests
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


mock = MockPaymentGateway()
sut = PaymentProcessor(mock)


# Class running tests
class Tester:
    def test_winProcess(self):
        # Given
        want = TransactionResult(True, "", "", TransactionStatus.COMPLETED)
        # When
        got = sut.processPayment("123", 40)
        # Then
        assert (want.success == got.success)

    def test_failProcessNeg(self):
        # Given
        want = "Payment processing error: Negative payment."
        # When
        sut.processPayment("123", -40)
        got = sut.logger.errors[-1]
        # Then
        assert want == got

    def test_failProcessNet(self):
        # Given
        want = "Payment processing error: Network payment failed."
        # When
        sut.processPayment(None, 10)
        got = sut.logger.errors[-1]
        # Then
        assert want == got

    def test_failProcessCash(self):
        # Given
        want = "Payment processing error: No cash."
        # When
        sut.processPayment("123", 99999)
        got = sut.logger.errors[-1]
        # Then
        assert want == got

    def test_winRefund(self):
        # Given
        want = TransactionResult(True, "", "", TransactionStatus.COMPLETED)
        # When
        got = sut.refundPayment("33")
        # Then
        assert (want.success == got.success)

    def test_failRefundNone(self):
        # Given
        want = "Refund processing error: Transaction not found."
        # When
        sut.refundPayment(None)
        got = sut.logger.errors[-1]
        # Then
        assert want == got

    def test_failRefundNet(self):
        # Given
        want = "Refund processing error: Network refund failed."
        # When
        sut.refundPayment("987")
        got = sut.logger.errors[-1]
        # Then
        assert want == got

    def test_winStatusCOM(self):
        # Given
        want = TransactionStatus.COMPLETED
        # When
        got = sut.getPaymentStatus("25")
        # Then
        assert want == got

    def test_winStatusPEN(self):
        # Given
        want = TransactionStatus.PENDING
        # When
        got = sut.getPaymentStatus("1")
        # Then
        assert want == got

    def test_failStatusNone(self):
        # Given
        want = "Error getting payment status: No transaction found."
        # When
        sut.getPaymentStatus(None)
        got = sut.logger.errors[-1]
        # Then
        assert want == got

    def test_failStatusNet(self):
        # Given
        want = "Error getting payment status: Network status failed."
        # When
        sut.getPaymentStatus("123")
        got = sut.logger.errors[-1]
        # Then
        assert want == got
