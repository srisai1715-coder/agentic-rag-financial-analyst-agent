from typing import Any


class FinancialRatioTool:
    """Deterministic financial ratio calculations using Python."""

    name = "financial_ratio"

    @staticmethod
    def margin(profit: float, revenue: float) -> float:
        if revenue == 0:
            raise ValueError("Revenue cannot be zero.")
        return (profit / revenue) * 100

    @staticmethod
    def return_on_equity(net_income: float, equity: float) -> float:
        if equity == 0:
            raise ValueError("Equity cannot be zero.")
        return (net_income / equity) * 100

    @staticmethod
    def return_on_assets(net_income: float, assets: float) -> float:
        if assets == 0:
            raise ValueError("Assets cannot be zero.")
        return (net_income / assets) * 100

    @staticmethod
    def debt_to_equity(debt: float, equity: float) -> float:
        if equity == 0:
            raise ValueError("Equity cannot be zero.")
        return debt / equity

    def run(self, operation: str, values: dict[str, Any]) -> dict[str, Any]:
        if operation == "operating_margin" or operation == "net_margin":
            result = self.margin(float(values["profit"]), float(values["revenue"]))
        elif operation == "roe":
            result = self.return_on_equity(
                float(values["net_income"]), float(values["equity"])
            )
        elif operation == "roa":
            result = self.return_on_assets(
                float(values["net_income"]), float(values["assets"])
            )
        elif operation == "debt_to_equity":
            result = self.debt_to_equity(
                float(values["debt"]), float(values["equity"])
            )
        else:
            raise ValueError(f"Unsupported ratio operation: {operation}")

        return {
            "tool": self.name,
            "operation": operation,
            "inputs": values,
            "result": result,
        }
