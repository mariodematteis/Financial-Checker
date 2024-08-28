from datetime import date

import pandas as pd

from financialchecker.data.aggregate import DataAggregate
from financialchecker.utils.utils import EnhancedStrEnum


class Period(EnhancedStrEnum):
    DAILY: str = "daily"
    WEEKLY: str = "weekly"
    MONTHLY: str = "monthly"
    YEARLY: str = "yearly"


class Estimator:
    def __init__(self,
                 start_date: date | None = None,
                 end_date: date | None = None) -> None:
        assert isinstance(start_date, date | None)
        assert isinstance(end_date, date | None)
        self.aggregator: DataAggregate = DataAggregate()

        self._income_df: pd.DataFrame = self.aggregator.get_income_dataframe()
        self._expense_df: pd.DataFrame = self.aggregator.get_expense_dataframe()

        if start_date is not None:
            if len(self._income_df):
                self._income_df = self._income_df[self._income_df["date"] >= start_date.strftime("%Y-%m-%d")] # noqa E507
            if len(self._expense_df):
                self._expense_df = self._expense_df[self._expense_df["date"] >= start_date.strftime("%Y-%m-%d")] # noqa E507
        elif end_date is not None:
            if len(self._income_df):
                self._income_df = self._income_df[self._income_df["date"] <= end_date.strftime("%Y-%m-%d")] # noqa E507
            if len(self._expense_df):
                self._expense_df = self._expense_df[self._expense_df["date"] <= end_date.strftime("%Y-%m-%d")] # noqa E507

        if isinstance(start_date, date):
            self._start_date_expense: date = start_date
        else:
            self._start_date_expense: date = self._expense_df["date"].min()

        if isinstance(end_date, date):
            self._end_date_expense: date = end_date
        else:
            self._end_date_expense: date = self._expense_df["date"].max()

    def get_start_date_expense(self) -> date:
        return self._start_date_expense

    def get_end_date_expense(self) -> date:
        return self._end_date_expense

    def _days_difference_expense(self,):
        return (self._end_date_expense - self._start_date_expense).days

    def income_rate_of_change(self,
                              stochastic: bool = False,
                              period: str = "daily") -> float:
        daily_change: float = self._income_df["amount"].diff().sum() / self._days_difference_expense() # noqa E507
        match period:
            case Period.DAILY:
                return daily_change
            case Period.WEEKLY:
                return daily_change * 7
            case Period.MONTHLY:
                return daily_change * 30
            case Period.YEARLY:
                return daily_change * 360
            case _:
                return 0.0

    def expense_rate_of_change(self,
                               stochastic: bool = False,
                               period: str = "daily") -> float:

        daily_change: float = self._expense_df[["date", "amount"]].groupby(by=["date"]).sum().mean() # noqa E507
        match period:
            case Period.DAILY:
                return daily_change
            case Period.WEEKLY:
                return daily_change * 7
            case Period.MONTHLY:
                return daily_change * 30
            case Period.YEARLY:
                return daily_change * 360
            case _:
                return 0.0
