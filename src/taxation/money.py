
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


CENT = Decimal("0.01")


def round_money(value):
    """
    Arredonda um valor monetario para duas casas decimais.

    Utiliza ROUND_HALF_UP:
    10.125 -> 10.13
    10.124 -> 10.12
    """
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("O valor monetario deve ser numerico.")

    if not amount.is_finite():
        raise ValueError("O valor monetario deve ser finito.")

    return amount.quantize(CENT, rounding=ROUND_HALF_UP)



def round_tax_breakdown(breakdown):
    """
    Retorna uma copia do detalhamento tributario
    com valores monetarios consistentes e arredondados.
    """
    if not isinstance(breakdown, dict):
        raise ValueError("O detalhamento tributario deve ser um dicionario.")

    monetary_fields = (
        "gross_profit",
        "iof",
        "taxable_profit",
        "income_tax",
        "total_taxes",
        "net_profit",
    )

    if not all(field in breakdown for field in monetary_fields):
        raise ValueError("O detalhamento tributario esta incompleto.")

    result = breakdown.copy()

    # Arredonda os valores principais individualmente.
    result["gross_profit"] = round_money(breakdown["gross_profit"])
    result["iof"] = round_money(breakdown["iof"])
    result["income_tax"] = round_money(breakdown["income_tax"])

    # Recalcula os valores derivados para manter consistencia.
    result["taxable_profit"] = (
        result["gross_profit"] - result["iof"]
    )

    result["total_taxes"] = (
        result["iof"] + result["income_tax"]
    )

    result["net_profit"] = (
        result["gross_profit"] - result["total_taxes"]
    )

    return result


