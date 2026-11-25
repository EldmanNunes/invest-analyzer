
from decimal import Decimal

import pytest

from src.taxation.income_tax import (
    get_income_tax_rate,
    calculate_income_tax,
)


@pytest.mark.parametrize(
    "days, expected_rate",
    [
        (1, Decimal("0.225")),
        (180, Decimal("0.225")),
        (181, Decimal("0.20")),
        (360, Decimal("0.20")),
        (361, Decimal("0.175")),
        (720, Decimal("0.175")),
        (721, Decimal("0.15")),
        (1000, Decimal("0.15")),
    ],
)
def test_income_tax_rates(days, expected_rate):
    assert get_income_tax_rate(days) == expected_rate


def test_calculate_income_tax():
    tax = calculate_income_tax(1000, 365)

    assert tax == Decimal("175.000")


def test_calculate_income_tax_short_term():
    tax = calculate_income_tax(1000, 90)

    assert tax == Decimal("225.000")


def test_zero_profit():
    tax = calculate_income_tax(0, 365)

    assert tax == Decimal("0.00")


@pytest.mark.parametrize(
    "invalid_days",
    [0, -1, 1.5, True, "180"],
)
def test_invalid_days(invalid_days):
    with pytest.raises(ValueError):
        get_income_tax_rate(invalid_days)


@pytest.mark.parametrize(
    "invalid_profit",
    [-100, "NaN", "Infinity", "-Infinity"],
)
def test_invalid_profit(invalid_profit):
    with pytest.raises(ValueError):
        calculate_income_tax(invalid_profit, 365)


from src.taxation.income_tax import (
    get_iof_rate,
    calculate_iof,
)


@pytest.mark.parametrize(
    "days, expected_rate",
    [
        (1, Decimal("0.96")),
        (2, Decimal("0.93")),
        (10, Decimal("0.66")),
        (15, Decimal("0.50")),
        (20, Decimal("0.33")),
        (29, Decimal("0.03")),
        (30, Decimal("0")),
        (31, Decimal("0")),
        (365, Decimal("0")),
    ],
)
def test_iof_rates(days, expected_rate):
    assert get_iof_rate(days) == expected_rate


def test_calculate_iof():
    tax = calculate_iof(1000, 15)

    assert tax == Decimal("500.00")


def test_calculate_iof_after_30_days():
    tax = calculate_iof(1000, 30)

    assert tax == Decimal("0")


def test_calculate_iof_zero_profit():
    tax = calculate_iof(0, 10)

    assert tax == Decimal("0.00")


@pytest.mark.parametrize(
    "invalid_days",
    [0, -1, 1.5, True, "15"],
)
def test_invalid_iof_days(invalid_days):
    with pytest.raises(ValueError):
        get_iof_rate(invalid_days)


@pytest.mark.parametrize(
    "invalid_profit",
    [-100, "NaN", "Infinity", "-Infinity"],
)
def test_invalid_iof_profit(invalid_profit):
    with pytest.raises(ValueError):
        calculate_iof(invalid_profit, 15)


from src.taxation.income_tax import calculate_tax_breakdown


def test_tax_breakdown_before_30_days():
    result = calculate_tax_breakdown(1000, 15)

    assert result["gross_profit"] == Decimal("1000")
    assert result["iof"] == Decimal("500.00")
    assert result["taxable_profit"] == Decimal("500.00")
    assert result["income_tax"] == Decimal("112.500000")
    assert result["total_taxes"] == Decimal("612.500000")
    assert result["net_profit"] == Decimal("387.500000")


def test_tax_breakdown_after_30_days():
    result = calculate_tax_breakdown(1000, 365)

    assert result["gross_profit"] == Decimal("1000")
    assert result["iof"] == Decimal("0")
    assert result["taxable_profit"] == Decimal("1000")
    assert result["income_tax"] == Decimal("175.000")
    assert result["total_taxes"] == Decimal("175.000")
    assert result["net_profit"] == Decimal("825.000")


def test_tax_breakdown_zero_profit():
    result = calculate_tax_breakdown(0, 15)

    assert result["iof"] == Decimal("0")
    assert result["income_tax"] == Decimal("0")
    assert result["total_taxes"] == Decimal("0")
    assert result["net_profit"] == Decimal("0")


def test_tax_breakdown_rejects_negative_profit():
    with pytest.raises(ValueError):
        calculate_tax_breakdown(-100, 15)


def test_tax_breakdown_rejects_invalid_days():
    with pytest.raises(ValueError):
        calculate_tax_breakdown(1000, 0)


