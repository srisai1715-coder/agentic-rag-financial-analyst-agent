from typing import Any


class FinancialCalculationTool:
    """Deterministic financial calculations using Python."""

    name = "financial_calculation"

    @staticmethod
    def revenue_growth(previous_revenue: float, current_revenue: float) -> float:
        if previous_revenue == 0:
            raise ValueError("Previous revenue cannot be zero.")
        return ((current_revenue - previous_revenue) / previous_revenue) * 100

    @staticmethod
    def percentage_change(old_value: float, new_value: float) -> float:
        if old_value == 0:
            raise ValueError("Old value cannot be zero.")
        return ((new_value - old_value) / old_value) * 100

    @staticmethod
    def difference(first_value: float, second_value: float) -> float:
        return second_value - first_value

    @staticmethod
    def profit_margin(profit: float, revenue: float) -> float:
        if revenue == 0:
            raise ValueError("Revenue cannot be zero.")
        return (profit / revenue) * 100

    def run(self, operation: str, values: dict[str, Any]) -> dict[str, Any]:
        if operation == "revenue_growth":
            result = self.revenue_growth(
                float(values["previous_revenue"]),
                float(values["current_revenue"]),
            )
        elif operation == "percentage_change":
            result = self.percentage_change(
                float(values["old_value"]),
                float(values["new_value"]),
            )
        elif operation == "difference":
            result = self.difference(
                float(values["first_value"]),
                float(values["second_value"]),
            )
        elif operation == "profit_margin":
            result = self.profit_margin(
                float(values["profit"]),
                float(values["revenue"]),
            )
        else:
            raise ValueError(f"Unsupported calculation operation: {operation}")

        return {
            "tool": self.name,
            "operation": operation,
            "inputs": values,
            "result": result,
        }
