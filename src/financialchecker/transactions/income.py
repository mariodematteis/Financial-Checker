from datetime import date

from financialchecker.transactions._transactions import Transaction, TransactionType


class Income(Transaction):
    def __init__(self,
                 transaction_category: str,
                 transaction_amount: float | int,
                 transaction_method: str,
                 transaction_date: date = date.today(),
                 transaction_description: str = "",) -> None:
        super().__init__(transaction_type=TransactionType.INCOME,
                         transaction_amount=transaction_amount,
                         transaction_method=transaction_method,
                         transaction_date=transaction_date,
                         transaction_description=transaction_description)
        self._category: str = transaction_category

    def __dict__(self,) -> dict[str, str | float | bool]:
        _tmp = super().__dict__()
        _tmp["category"] = self._category

        return _tmp
