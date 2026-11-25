
from dataclasses import dataclass

from src.taxation.profiles import (
    IncomeTaxPolicy,
    IofPolicy,
    get_tax_profile,
)


@dataclass(frozen=True)
class TaxDecision:
    product_code: str
    income_tax_status: str
    iof_status: str
    can_calculate_income_tax: bool
    can_calculate_iof: bool


def evaluate_tax_treatment(
    product_code,
    eligibility_confirmed=False,
    iof_applicable=None,
    iof_zero_confirmed=False,
    operation_review_confirmed=False,
):
    """
    Avalia se o tratamento tributario pode ser calculado.

    A funcao nao calcula valores de impostos.
    Ela verifica se existem condicoes suficientes
    para permitir os calculos.
    """
    profile = get_tax_profile(product_code)

    # Decisao sobre IR
    if (
        profile.income_tax_policy
        == IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME
    ):
        if (
            profile.requires_operation_review
            and not operation_review_confirmed
        ):
            income_status = "REVIEW_REQUIRED"
            can_calculate_income_tax = False
        else:
            income_status = "READY"
            can_calculate_income_tax = True

    elif (
        profile.income_tax_policy
        == IncomeTaxPolicy.EXEMPT_IF_ELIGIBLE
    ):
        if eligibility_confirmed:
            income_status = "EXEMPT"
            can_calculate_income_tax = False
        else:
            income_status = "REVIEW_REQUIRED"
            can_calculate_income_tax = False

    else:
        income_status = "UNSUPPORTED"
        can_calculate_income_tax = False

    # Decisao sobre IOF
    if profile.iof_policy == IofPolicy.REGRESSIVE_WHEN_APPLICABLE:
        if iof_applicable is True:
            iof_status = "READY"
            can_calculate_iof = True
        elif iof_applicable is False:
            iof_status = "NOT_APPLICABLE"
            can_calculate_iof = False
        else:
            iof_status = "REVIEW_REQUIRED"
            can_calculate_iof = False

    elif (
        profile.iof_policy
        == IofPolicy.ZERO_FOR_QUALIFYING_OPERATION
    ):
        if iof_applicable is False:
            iof_status = "NOT_APPLICABLE"
            can_calculate_iof = False
        elif iof_applicable is True and iof_zero_confirmed:
            iof_status = "EXEMPT"
            can_calculate_iof = False
        else:
            iof_status = "REVIEW_REQUIRED"
            can_calculate_iof = False

    elif profile.iof_policy == IofPolicy.OPERATION_REVIEW_REQUIRED:
        if iof_applicable is False:
            iof_status = "NOT_APPLICABLE"
            can_calculate_iof = False
        else:
            iof_status = "REVIEW_REQUIRED"
            can_calculate_iof = False

    else:
        iof_status = "UNSUPPORTED"
        can_calculate_iof = False

    return TaxDecision(
        product_code=profile.product_code,
        income_tax_status=income_status,
        iof_status=iof_status,
        can_calculate_income_tax=can_calculate_income_tax,
        can_calculate_iof=can_calculate_iof,
    )
