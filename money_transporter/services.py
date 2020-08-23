from django.db.transaction import atomic

from money_transporter.models import User


class MoneyTransfer:

    def __init__(self, sender: User, recipient: User, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = float(amount)

    @atomic
    def make(self):
        self.sender.balance -= self.amount
        recipient_increase_amount = round(self.amount * self._calc_coefficient(), 2)
        self.recipient.balance += recipient_increase_amount
        self.sender.save()
        self.recipient.save()

        return recipient_increase_amount

    def _calc_coefficient(self):
        if self.sender.currency == self.recipient.currency:
            return 1

        send_currency = self.sender.currency
        recipient_currency = self.recipient.currency

        return (send_currency.multiplicity * recipient_currency.actual_course.course) /\
               (recipient_currency.multiplicity * send_currency.actual_course.course)
