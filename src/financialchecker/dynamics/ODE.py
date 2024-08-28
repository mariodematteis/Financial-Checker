from datetime import date

from financialchecker.data.estimates import Estimator, Period


class PartialDifferentialEquationsMethods:
    def __init__(self,
                 start_date: date | None = None,
                 end_date: date | None = None,
                 period: Period | str = Period.DAILY) -> None:
        self._estimator: Estimator = Estimator(start_date=start_date,
                                               end_date=end_date)

        self._start_date: date = self._estimator.get_start_date()
        self._end_date: date = self._estimator.get_end_date()

        self._income_coefficient: float = self._estimator.income_rate_of_change(period=period) # noqa E507
        self._expense_coefficient: float = self._estimator.expense_rate_of_change(period=period) # noqa E507
