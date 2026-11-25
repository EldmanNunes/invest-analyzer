
from decimal import Decimal, InvalidOperation

def _to_decimal(value):
    """Converte valores numericos finitos para Decimal."""
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("O valor informado deve ser numerico.")

    if not result.is_finite():
        raise ValueError("O valor deve ser finito.")

    return result


def _validate_rate(rate):
    rate = _to_decimal(rate)
    if rate <= Decimal("-1"):
        raise ValueError("A taxa deve ser maior que -100%.")
    return rate


def _validate_periods(periods):
    if isinstance(periods, bool) or not isinstance(periods, int):
        raise ValueError("O numero de periodos deve ser inteiro.")
    if periods < 0:
        raise ValueError("O numero de periodos nao pode ser negativo.")
    return periods


def compound_interest(principal, rate, periods):
    """Calcula o montante com juros compostos."""
    principal = _to_decimal(principal)
    rate = _validate_rate(rate)
    periods = _validate_periods(periods)

    if principal < 0:
        raise ValueError("O capital inicial nao pode ser negativo.")

    return principal * (Decimal("1") + rate) ** periods


def future_value(principal, rate, periods):
    """Calcula o valor futuro de um capital sem aportes."""
    return compound_interest(principal, rate, periods)


def present_value(future_amount, rate, periods):
    """Calcula o valor presente de um montante futuro."""
    future_amount = _to_decimal(future_amount)
    rate = _validate_rate(rate)
    periods = _validate_periods(periods)

    if future_amount < 0:
        raise ValueError("O valor futuro nao pode ser negativo.")

    return future_amount / (Decimal("1") + rate) ** periods


def equivalent_rate(rate, source_periods, target_periods):
    """
    Converte uma taxa efetiva entre periodos.

    Exemplo: taxa efetiva anual para taxa efetiva mensal:
    source_periods=1 e target_periods=12.
    """
    rate = _validate_rate(rate)
    source_periods = _validate_periods(source_periods)
    target_periods = _validate_periods(target_periods)

    if source_periods == 0 or target_periods == 0:
        raise ValueError("Os periodos de conversao devem ser positivos.")

    return (
        (Decimal("1") + rate)
        ** (Decimal(source_periods) / Decimal(target_periods))
    ) - Decimal("1")


def accumulated_return(initial_value, final_value):
    """Calcula a rentabilidade acumulada em percentual decimal."""
    initial_value = _to_decimal(initial_value)
    final_value = _to_decimal(final_value)

    if initial_value <= 0:
        raise ValueError("O valor inicial deve ser maior que zero.")

    if final_value < 0:
        raise ValueError("O valor final nao pode ser negativo.")

    return (final_value / initial_value) - Decimal("1")


def future_value_with_contributions(
    initial_capital,
    contribution,
    rate,
    periods,
    contribution_timing="end",
):
    """
    Calcula o valor futuro com aportes periódicos.

    contribution_timing:
        "end": aporte realizado no final de cada periodo.
        "beginning": aporte realizado no inicio de cada periodo.
    """
    initial_capital = _to_decimal(initial_capital)
    contribution = _to_decimal(contribution)
    rate = _validate_rate(rate)
    periods = _validate_periods(periods)

    if initial_capital < 0:
        raise ValueError("O capital inicial nao pode ser negativo.")

    if contribution < 0:
        raise ValueError("O aporte nao pode ser negativo.")

    if contribution_timing not in ("beginning", "end"):
        raise ValueError(
            "O momento do aporte deve ser 'beginning' ou 'end'."
        )

    accumulated_capital = compound_interest(
        initial_capital,
        rate,
        periods,
    )

    if periods == 0 or contribution == 0:
        return accumulated_capital

    if rate == 0:
        return accumulated_capital + contribution * periods

    periodic_factor = (
        (Decimal("1") + rate) ** periods - Decimal("1")
    ) / rate

    if contribution_timing == "beginning":
        periodic_factor *= Decimal("1") + rate

    return accumulated_capital + contribution * periodic_factor


def real_return(nominal_rate, inflation_rate):
    """
    Calcula a taxa real descontando a inflacao.

    Ambas as taxas devem ser informadas em formato decimal.
    Exemplo: 10% = 0.10.
    """
    nominal_rate = _validate_rate(nominal_rate)
    inflation_rate = _validate_rate(inflation_rate)

    if inflation_rate <= Decimal("-1"):
        raise ValueError("A inflacao deve ser maior que -100%.")

    return (
        (Decimal("1") + nominal_rate)
        / (Decimal("1") + inflation_rate)
    ) - Decimal("1")


def annualized_return(accumulated_rate, months):
    """
    Converte uma rentabilidade acumulada em taxa anual efetiva.

    Exemplo:
    accumulated_rate=0.10 e months=6 representam
    10% acumulados em seis meses.
    """
    accumulated_rate = _validate_rate(accumulated_rate)
    months = _validate_periods(months)

    if months == 0:
        raise ValueError("O prazo deve ser maior que zero.")

    return (
        (Decimal("1") + accumulated_rate)
        ** (Decimal("12") / Decimal(months))
    ) - Decimal("1")

