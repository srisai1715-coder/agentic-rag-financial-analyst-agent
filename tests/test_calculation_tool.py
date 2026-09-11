import pytest

from app.tools.calculation_tool import FinancialCalculationTool


def test_revenue_growth():
    tool = FinancialCalculationTool()
    result = tool.revenue_growth(245.122, 281.724)
    assert round(result, 2) == 14.93


def test_percentage_change():
    tool = FinancialCalculationTool()
    assert tool.percentage_change(100, 120) == 20


def test_difference():
    tool = FinancialCalculationTool()
    assert tool.difference(100, 150) == 50


def test_profit_margin():
    tool = FinancialCalculationTool()
    assert tool.profit_margin(25, 100) == 25


def test_revenue_growth_zero_previous_value():
    tool = FinancialCalculationTool()
    with pytest.raises(ValueError):
        tool.revenue_growth(0, 100)


def test_profit_margin_zero_revenue():
    tool = FinancialCalculationTool()
    with pytest.raises(ValueError):
        tool.profit_margin(25, 0)
