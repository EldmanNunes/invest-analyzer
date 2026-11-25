
import pytest
from decimal import Decimal

from src.taxation.money import round_money
from src.taxation.money import round_tax_breakdown


@pytest.mark.parametrize(
    "value, expected",
    [
        ("10.125", Decimal("10.13")),
        ("10.124", Decimal("10.12")),
        ("10.126", Decimal("10.13")),
        ("100", Decimal("100.00")),
        ("0", Decimal("0.00")),
        ("-10.125", Decimal("-10.13")),
        ("-10.124", Decimal("-10.12")),
        ("0.005", Decimal("0.01")),
        ("0.004", Decimal("0.00")),
    ],
)
def test_round_money(value, expected):
    assert round_money(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "NaN",
        "Infinity",
        "-Infinity",
    ],
)
def test_round_money_rejects_non_finite_values(value):
    with pytest.raises(ValueError):
        round_money(value)


@pytest.mark.parametrize(
    "value",
    [
        "texto",
        None,
        object(),
    ],
)
def test_round_money_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        round_money(value)


def test_round_money_returns_decimal():
    result = round_money("123.456")
    assert isinstance(result, Decimal)


def test_round_tax_breakdown():
    breakdown = {
        "gross_profit": Decimal("1000.125"),
        "iof": Decimal("100.125"),
        "taxable_profit": Decimal("900.000"),
        "income_tax": Decimal("135.005"),
        "total_taxes": Decimal("235.130"),
        "net_profit": Decimal("764.995"),
    }

    result = round_tax_breakdown(breakdown)

    assert result["gross_profit"] == Decimal("1000.13")
    assert result["iof"] == Decimal("100.13")
    assert result["taxable_profit"] == Decimal("900.00")
    assert result["income_tax"] == Decimal("135.01")
    assert result["total_taxes"] == Decimal("235.14")
    assert result["net_profit"] == Decimal("764.99")


def test_round_tax_breakdown_preserves_original():
    breakdown = {
        "gross_profit": Decimal("100.125"),
        "iof": Decimal("10.125"),
        "taxable_profit": Decimal("90.000"),
        "income_tax": Decimal("13.500"),
        "total_taxes": Decimal("23.625"),
        "net_profit": Decimal("76.500"),
    }

    original = breakdown.copy()

    round_tax_breakdown(breakdown)

    assert breakdown == original


def test_round_tax_breakdown_rejects_non_dictionary():
    with pytest.raises(ValueError):
        round_tax_breakdown("invalid")


def test_round_tax_breakdown_rejects_incomplete_dictionary():
    with pytest.raises(ValueError):
        round_tax_breakdown({
            "gross_profit": Decimal("100.00"),
        })


def test_round_tax_breakdown_reconciles_displayed_values():
    breakdown = {
        "gross_profit": Decimal("10.00"),
        "iof": Decimal("0.005"),
        "taxable_profit": Decimal("9.995"),
        "income_tax": Decimal("0.005"),
        "total_taxes": Decimal("0.010"),
        "net_profit": Decimal("9.990"),
    }

    result = round_tax_breakdown(breakdown)

    assert result["iof"] == Decimal("0.01")
    assert result["income_tax"] == Decimal("0.01")

    assert result["total_taxes"] == (
        result["iof"] + result["income_tax"]
    )

    assert result["total_taxes"] == Decimal("0.02")

    assert result["net_profit"] == (
        result["gross_profit"] - result["total_taxes"]
    )

    assert result["net_profit"] == Decimal("9.98")


def test_round_tax_breakdown_preserves_calculation_precision():
    breakdown = {
        "gross_profit": Decimal("10.005"),
        "iof": Decimal("0.005"),
        "taxable_profit": Decimal("10.000"),
        "income_tax": Decimal("1.500"),
        "total_taxes": Decimal("1.505"),
        "net_profit": Decimal("8.500"),
    }

    result = round_tax_breakdown(breakdown)

    # O calculo original deve manter sua precisao.
    assert breakdown["gross_profit"] == Decimal("10.005")
    assert breakdown["iof"] == Decimal("0.005")
    assert breakdown["total_taxes"] == Decimal("1.505")

    # A copia apresentada deve ter valores arredondados.
    assert result["gross_profit"] == Decimal("10.01")
    assert result["iof"] == Decimal("0.01")
    assert result["taxable_profit"] == Decimal("10.00")
    assert result["income_tax"] == Decimal("1.50")
    assert result["total_taxes"] == Decimal("1.51")
    assert result["net_profit"] == Decimal("8.50")