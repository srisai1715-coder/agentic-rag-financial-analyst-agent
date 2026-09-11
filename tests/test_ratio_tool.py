import pytest

from app.tools.ratio_tool import FinancialRatioTool


def test_operating_margin():
    tool = FinancialRatioTool()
    assert round(tool.margin(128.528, 281.724), 2) == 45.62


def test_return_on_revenue():
    tool = FinancialRatioTool()
    assert round(tool.margin(25, 100), 2) == 25.00


def test_margin_zero_revenue():
    tool = FinancialRatioTool()

    with pytest.raises(ValueError):
        tool.margin(25, 0)


def test_ratio_tool_name():
    tool = FinancialRatioTool()
    assert tool.name == "financial_ratio"