from datetime import date, datetime

from financialchecker.utils.utils import EnhancedStrEnum


class TransactionType(EnhancedStrEnum):
    INCOME: str = "INCOME"
    EXPENSE: str = "EXPENSE"


class Transaction:
    def __init__(self,
                 transaction_type: TransactionType | str,
                 transaction_amount: float | int,
                 transaction_method: str,
                 transaction_date: date = date.today(),
                 transaction_description: str = "",) -> None:
        assert isinstance(transaction_type, TransactionType) or (isinstance(transaction_type, str) and TransactionType.has(transaction_type)) # noqa E507
        assert isinstance(transaction_amount, float | int) and \
            transaction_amount >= 0.01
        assert isinstance(transaction_method, str)
        assert isinstance(transaction_date, date)
        assert isinstance(transaction_description, str)

        self._type: str = transaction_type.value if isinstance(transaction_type, TransactionType) else transaction_type # noqa E507
        self._amount: float = transaction_amount if isinstance(transaction_amount, float) else float(transaction_amount) # noqa E507
        self._transaction_method: str = transaction_method
        self._date: date = transaction_date
        self._description: str = transaction_description

    def get_type(self) -> str:
        return self._type

    def get_amount(self) -> float:
        return self._amount

    def get_transaction_method(self) -> str:
        return self._transaction_method

    def get_date(self) -> date:
        return self._date

    def get_description(self) -> str:
        return self._description

    def set_type(self, transaction_type: TransactionType | str) -> None:
        self._type = transaction_type

    def set_amount(self, transaction_amount: float | int) -> None:
        self._amount = transaction_amount

    def set_transaction_method(self, transaction_method: str) -> None:
        self._transaction_method = transaction_method

    def set_date(self, transaction_date: date) -> None:
        self._date = transaction_date

    def set_description(self, description) -> None:
        self._description = description

    def __dict__(self) -> dict[str, str | float | bool]:
        return {
            "type": self._type,
            "amount": self._amount,
            "transaction_method": self._transaction_method,
            "date": datetime.strftime(self._date, "%Y-%m-%d"),
            "description": self._description
        }

    def __iter__(self):
        return ((k, v) for k, v in self.__dict__().items())
