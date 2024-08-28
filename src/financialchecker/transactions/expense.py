from datetime import date

from financialchecker.transactions._transactions import Transaction, TransactionType


class Expense(Transaction):
    def __init__(self,
                 transaction_category: str,
                 transaction_amount: float | int,
                 transaction_method: str,
                 transaction_date: date = date.today(),
                 transaction_advance_payment: bool = False,
                 transaction_description: str = "",
                 transaction_firm: str = "",
                 transaction_location: str = "") -> None: # noqa E507
        super().__init__(transaction_type=TransactionType.EXPENSE,
                         transaction_amount=transaction_amount,
                         transaction_method=transaction_method,
                         transaction_date=transaction_date,
                         transaction_description=transaction_description,)
        self._category: str = transaction_category
        self._advance_payment: bool = transaction_advance_payment
        self._firm: str = transaction_firm
        self._location: str = transaction_location

    def __dict__(self,) -> dict[str, str | float | bool]:
        _tmp = super().__dict__()
        _tmp["category"] = self._category
        _tmp["advance_payment"] = self._advance_payment
        _tmp["firm"] = self._firm
        _tmp["location"] = self._location

        return _tmp
