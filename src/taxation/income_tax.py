
from decimal import Decimal


def get_income_tax_rate(days):
    """
    Retorna a aliquota de IR aplicavel a renda fixa tributada
    pela tabela regressiva.

    O prazo e informado em dias corridos.
    """
    if isinstance(days, bool) or not isinstance(days, int):
        raise ValueError("O prazo deve ser informado em dias inteiros.")

    if days <= 0:
        raise ValueError("O prazo deve ser maior que zero.")

    if days <= 180:
        return Decimal("0.225")

    if days <= 360:
        return Decimal("0.20")

    if days <= 720:
        return Decimal("0.175")

    return Decimal("0.15")


def calculate_income_tax(profit, days):
    """
    Calcula o IR sobre o rendimento positivo da aplicacao.

    O imposto incide sobre o rendimento, nao sobre o capital.
    """
    try:
        profit = Decimal(str(profit))
    except (ValueError, TypeError, ArithmeticError):
        raise ValueError("O rendimento informado deve ser numerico.")

    if not profit.is_finite():
        raise ValueError("O rendimento deve ser finito.")

    if profit < 0:
        raise ValueError("O rendimento nao pode ser negativo.")

    tax_rate = get_income_tax_rate(days)

    return profit * tax_rate


def get_iof_rate(days):
    """
    Retorna a aliquota regressiva de IOF sobre o rendimento.

    A tabela considera dias corridos.
    A partir do 30o dia, a aliquota e zero.
    """
    if isinstance(days, bool) or not isinstance(days, int):
        raise ValueError("O prazo deve ser informado em dias inteiros.")

    if days <= 0:
        raise ValueError("O prazo deve ser maior que zero.")

    iof_rates = (
        96, 93, 90, 86, 83, 80, 76, 73, 70, 66,
        63, 60, 56, 53, 50, 46, 43, 40, 36, 33,
        30, 26, 23, 20, 16, 13, 10, 6, 3, 0,
    )

    if days >= 30:
        return Decimal("0")

    return Decimal(iof_rates[days - 1]) / Decimal("100")


def calculate_iof(profit, days):
    """
    Calcula o IOF sobre o rendimento da aplicacao.

    A aplicabilidade do IOF depende do tipo de investimento.
    Esta funcao calcula o imposto para aplicacoes sujeitas a tabela.
    """
    try:
        profit = Decimal(str(profit))
    except (ValueError, TypeError, ArithmeticError):
        raise ValueError("O rendimento informado deve ser numerico.")

    if not profit.is_finite():
        raise ValueError("O rendimento deve ser finito.")

    if profit < 0:
        raise ValueError("O rendimento nao pode ser negativo.")

    iof_rate = get_iof_rate(days)

    return profit * iof_rate


def calculate_tax_breakdown(profit, days):
    """
    Calcula IOF, IR e rendimento liquido.

    O IR incide sobre o rendimento apos a deducao do IOF.
    Os valores retornados ainda nao sao arredondados para centavos.
    """
    iof = calculate_iof(profit, days)

    gross_profit = Decimal(str(profit))
    taxable_profit = gross_profit - iof

    income_tax = calculate_income_tax(taxable_profit, days)

    total_taxes = iof + income_tax
    net_profit = gross_profit - total_taxes

    return {
        "gross_profit": gross_profit,
        "iof": iof,
        "taxable_profit": taxable_profit,
        "income_tax": income_tax,
        "total_taxes": total_taxes,
        "net_profit": net_profit,
    }
