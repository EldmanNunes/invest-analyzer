
from dataclasses import dataclass
from enum import Enum


class IncomeTaxPolicy(Enum):
    REGRESSIVE_FIXED_INCOME = "regressive_fixed_income"
    EXEMPT_IF_ELIGIBLE = "exempt_if_eligible"
    MANUAL_REVIEW = "manual_review"
    UNSUPPORTED = "unsupported"


class IofPolicy(Enum):
    REGRESSIVE_WHEN_APPLICABLE = "regressive_when_applicable"
    ZERO_FOR_QUALIFYING_OPERATION = "zero_for_qualifying_operation"
    OPERATION_REVIEW_REQUIRED = "operation_review_required"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class TaxProfile:
    product_code: str
    income_tax_policy: IncomeTaxPolicy
    iof_policy: IofPolicy
    requires_eligibility_check: bool
    requires_operation_review: bool
    description: str


TAX_PROFILES = {
    "CDB": TaxProfile(
        product_code="CDB",
        income_tax_policy=IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME,
        iof_policy=IofPolicy.REGRESSIVE_WHEN_APPLICABLE,
        requires_eligibility_check=False,
        requires_operation_review=False,
        description="CDB no regime tributario regressivo de renda fixa.",
    ),

    "RDB": TaxProfile(
        product_code="RDB",
        income_tax_policy=IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME,
        iof_policy=IofPolicy.REGRESSIVE_WHEN_APPLICABLE,
        requires_eligibility_check=False,
        requires_operation_review=False,
        description="RDB no regime tributario regressivo de renda fixa.",
    ),

    "TESOURO_DIRETO": TaxProfile(
        product_code="TESOURO_DIRETO",
        income_tax_policy=IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME,
        iof_policy=IofPolicy.REGRESSIVE_WHEN_APPLICABLE,
        requires_eligibility_check=False,
        requires_operation_review=True,
        description=(
            "Titulos do Tesouro Direto. O tratamento depende "
            "do evento, lote e prazo da aplicacao."
        ),
    ),

    "LCI": TaxProfile(
        product_code="LCI",
        income_tax_policy=IncomeTaxPolicy.EXEMPT_IF_ELIGIBLE,
        iof_policy=IofPolicy.OPERATION_REVIEW_REQUIRED,
        requires_eligibility_check=True,
        requires_operation_review=True,
        description=(
            "LCI: isencao de IR condicionada ao enquadramento. "
            "IOF exige classificacao da operacao."
        ),
    ),

    "LCA": TaxProfile(
        product_code="LCA",
        income_tax_policy=IncomeTaxPolicy.EXEMPT_IF_ELIGIBLE,
        iof_policy=IofPolicy.ZERO_FOR_QUALIFYING_OPERATION,
        requires_eligibility_check=True,
        requires_operation_review=True,
        description=(
            "LCA: isencao de IR condicionada ao enquadramento. "
            "IOF zero somente nas operacoes legalmente abrangidas."
        ),
    ),
}


def get_tax_profile(product_code):
    """Retorna o perfil tributario cadastrado para um produto."""
    if not isinstance(product_code, str):
        raise ValueError("O codigo do produto deve ser um texto.")

    normalized_code = product_code.strip().upper()

    if not normalized_code:
        raise ValueError("O codigo do produto nao pode ser vazio.")

    try:
        return TAX_PROFILES[normalized_code]
    except KeyError:
        raise ValueError(
            f"Produto sem perfil tributario cadastrado: {normalized_code}"
        )
