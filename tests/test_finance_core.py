
from decimal import Decimal

import pytest

from src.finance.core import (
    compound_interest,
    future_value,
    present_value,
    equivalent_rate,
    accumulated_return,
)


def test_compound_interest():
    result = compound_interest(1000, 0.10, 2)
    assert result == Decimal("1210.00")


def test_future_value():
    result = future_value(1000, 0.10, 2)
    assert result == Decimal("1210.00")


def test_present_value():
    result = present_value(1210, 0.10, 2)
    assert result == Decimal("1E+3")


def test_equivalent_annual_to_monthly_rate():
    monthly_rate = equivalent_rate(0.12, 1, 12)

    reconstructed_annual_rate = (
        (Decimal("1") + monthly_rate) ** 12
    ) - Decimal("1")

    assert reconstructed_annual_rate == pytest.approx(
        Decimal("0.12"),
        abs=Decimal("1e-25")
    )


def test_accumulated_return():
    result = accumulated_return(1000, 1250)
    assert result == Decimal("0.25")


def test_zero_periods():
    result = compound_interest(1000, 0.10, 0)
    assert result == Decimal("1000.0")


@pytest.mark.parametrize(
    "principal, rate, periods",
    [
        (-100, 0.10, 2),
        (100, -1, 2),
        (100, 0.10, -1),
        (100, 0.10, 1.5),
    ],
)
def test_invalid_compound_interest_inputs(principal, rate, periods):
    with pytest.raises(ValueError):
        compound_interest(principal, rate, periods)


def test_present_value_rejects_negative_amount():
    with pytest.raises(ValueError):
        present_value(-100, 0.10, 2)


def test_accumulated_return_rejects_zero_initial_value():
    with pytest.raises(ValueError):
        accumulated_return(0, 100)

@pytest.mark.parametrize(
    "invalid_value",
    [
        "NaN",
        "Infinity",
        "-Infinity",
    ],
)
def test_compound_interest_rejects_non_finite_values(invalid_value):
    with pytest.raises(ValueError):
        compound_interest(invalid_value, 0.10, 2)


@pytest.mark.parametrize(
    "invalid_value",
    [
        "NaN",
        "Infinity",
        "-Infinity",
    ],
)
def test_accumulated_return_rejects_non_finite_values(invalid_value):
    with pytest.raises(ValueError):
        accumulated_return(1000, invalid_value)


from src.finance.core import future_value_with_contributions


def test_future_value_with_contributions_at_end():
    result = future_value_with_contributions(
        1000, 500, 0.01, 2, "end"
    )

    assert result == Decimal("2025.100")


def test_future_value_with_contributions_at_beginning():
    result = future_value_with_contributions(
        1000, 500, 0.01, 2, "beginning"
    )

    assert result == Decimal("2035.150")


def test_future_value_with_contributions_zero_rate():
    result = future_value_with_contributions(
        1000, 500, 0, 2
    )

    assert result == Decimal("2000")


def test_future_value_with_contributions_zero_periods():
    result = future_value_with_contributions(
        1000, 500, 0.01, 0
    )

    assert result == Decimal("1000.00")


def test_future_value_with_contributions_rejects_negative_contribution():
    with pytest.raises(ValueError):
        future_value_with_contributions(
            1000, -500, 0.01, 2
        )


def test_future_value_with_contributions_rejects_invalid_timing():
    with pytest.raises(ValueError):
        future_value_with_contributions(
            1000, 500, 0.01, 2, "invalid"
        )


from src.finance.core import real_return, annualized_return


def test_real_return():
    result = real_return(0.10, 0.05)

    assert result == pytest.approx(
        Decimal("0.0476190476190476190476190476"),
        abs=Decimal("1e-25"),
    )


def test_real_return_with_negative_inflation():
    result = real_return(0.10, -0.02)

    assert result == pytest.approx(
        Decimal("0.1224489795918367346938775510"),
        abs=Decimal("1e-25"),
    )


def test_annualized_return():
    result = annualized_return(0.10, 6)

    expected = (
        (Decimal("1.10") ** 2) - Decimal("1")
    )

    assert result == expected


def test_annualized_return_zero_rate():
    result = annualized_return(0, 6)

    assert result == Decimal("0")


def test_annualized_return_rejects_zero_months():
    with pytest.raises(ValueError):
        annualized_return(0.10, 0)


def test_annualized_return_rejects_negative_months():
    with pytest.raises(ValueError):
        annualized_return(0.10, -6)
