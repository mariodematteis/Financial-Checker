from datetime import date

import pandas as pd
from numpy.typing import NDArray

from financialchecker.database.mongodb.database import MongoDBCrud
from financialchecker.transactions._transactions import TransactionType


class DataAggregate:
    def __init__(self) -> None:
        self._mongo_instance: MongoDBCrud = MongoDBCrud()
        self.update_transactions()

    def update_transactions(self) -> None:
        self._all_transaction: list[dict] = self._mongo_instance.get_all_transactions()
        self._expense_dataframe: pd.DataFrame = pd.DataFrame(_dict for _dict in self._all_transaction if _dict.get("type", "") == TransactionType.EXPENSE) # noqa E507
        self._expense_dataframe["date"] = pd.to_datetime(
            self._expense_dataframe["date"]
        )

        self._income_dataframe: pd.DataFrame = pd.DataFrame(_dict for _dict in self._all_transaction if _dict.get("type", "") == TransactionType.INCOME) # noqa E507

    def get_expense_dataframe(self) -> pd.DataFrame:
        self.update_transactions()

        if len(self._expense_dataframe):
            self._expense_dataframe["date"] = pd.to_datetime(
                self._expense_dataframe["date"],
                format="%Y-%m-%d"
            )
        return self._expense_dataframe

    def get_income_dataframe(self) -> pd.DataFrame:
        self.update_transactions()
        if len(self._income_dataframe):
            self._income_dataframe["date"] = pd.to_datetime(self._income_dataframe["date"], # noqa E507
                                                            format="%Y-%m-%d")
        return self._income_dataframe

    def get_income_amount_distribution(self,
                                       start_date: date | None = None,
                                       end_date: date | None = None) -> NDArray:
        self.update_transactions()
        if start_date is None and end_date is None:
            return self._income_dataframe["amount"]
        elif start_date is not None:
            return self._income_dataframe[self._income_dataframe["date"] >= start_date]["amount"] # noqa E507
        elif end_date is not None:
            return self._income_dataframe[self._income_dataframe["date"] <= end_date]["amount"] # noqa E507
        else:
            return self._income_dataframe[(self._income_dataframe["date"] >= start_date) & (self._income_dataframe["date"] <= end_date)]["amount"] # noqa E507

    def get_expense_amount_distribution(self,
                                        start_date: date | None = None,
                                        end_date: date | None = None) -> NDArray:
        self.update_transactions()
        if start_date is None and end_date is None:
            return self._expense_dataframe["amount"]
        elif start_date is not None:
            return self._expense_dataframe[self._expense_dataframe["date"] >= start_date]["amount"] # noqa E507
        elif end_date is not None:
            return self._expense_dataframe[self._expense_dataframe["date"] <= end_date]["amount"] # noqa E507
        else:
            return self._expense_dataframe[(self._expense_dataframe["date"] >= start_date) & (self._expense_dataframe["date"] <= end_date)]["amount"] # noqa E507

    def distribution(self) -> None:
        ...
