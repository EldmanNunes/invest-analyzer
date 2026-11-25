
import pytest

from src.taxation.tax_decision import evaluate_tax_treatment


def test_cdb_with_iof_applicable_is_ready():
    result = evaluate_tax_treatment(
        "CDB",
        iof_applicable=True,
    )

    assert result.income_tax_status == "READY"
    assert result.iof_status == "READY"
    assert result.can_calculate_income_tax is True
    assert result.can_calculate_iof is True


def test_cdb_without_iof_applicability():
    result = evaluate_tax_treatment(
        "CDB",
        iof_applicable=False,
    )

    assert result.income_tax_status == "READY"
    assert result.iof_status == "NOT_APPLICABLE"
    assert result.can_calculate_iof is False


def test_cdb_without_iof_classification_requires_review():
    result = evaluate_tax_treatment("CDB")

    assert result.iof_status == "REVIEW_REQUIRED"
    assert result.can_calculate_iof is False


def test_lci_without_eligibility_requires_review():
    result = evaluate_tax_treatment("LCI")

    assert result.income_tax_status == "REVIEW_REQUIRED"
    assert result.can_calculate_income_tax is False


def test_lci_with_eligibility_is_exempt_from_income_tax():
    result = evaluate_tax_treatment(
        "LCI",
        eligibility_confirmed=True,
        iof_applicable=False,
    )

    assert result.income_tax_status == "EXEMPT"
    assert result.can_calculate_income_tax is False


def test_lci_iof_requires_operation_review():
    result = evaluate_tax_treatment(
        "LCI",
        eligibility_confirmed=True,
        iof_applicable=True,
    )

    assert result.iof_status == "REVIEW_REQUIRED"
    assert result.can_calculate_iof is False


def test_lca_without_eligibility_requires_review():
    result = evaluate_tax_treatment("LCA")

    assert result.income_tax_status == "REVIEW_REQUIRED"


def test_lca_with_eligibility_is_exempt_from_income_tax():
    result = evaluate_tax_treatment(
        "LCA",
        eligibility_confirmed=True,
        iof_applicable=False,
    )

    assert result.income_tax_status == "EXEMPT"
    assert result.iof_status == "NOT_APPLICABLE"


def test_lca_iof_zero_requires_confirmation():
    result = evaluate_tax_treatment(
        "LCA",
        eligibility_confirmed=True,
        iof_applicable=True,
        iof_zero_confirmed=False,
    )

    assert result.iof_status == "REVIEW_REQUIRED"
    assert result.can_calculate_iof is False


def test_lca_confirmed_zero_iof():
    result = evaluate_tax_treatment(
        "LCA",
        eligibility_confirmed=True,
        iof_applicable=True,
        iof_zero_confirmed=True,
    )

    assert result.iof_status == "EXEMPT"
    assert result.can_calculate_iof is False



def test_tesouro_requires_operation_review():
    result = evaluate_tax_treatment("TESOURO_DIRETO")

    assert result.income_tax_status == "REVIEW_REQUIRED"
    assert result.can_calculate_income_tax is False
    assert result.iof_status == "REVIEW_REQUIRED"
    assert result.can_calculate_iof is False


def test_tesouro_allows_income_tax_after_operation_review():
    result = evaluate_tax_treatment(
        "TESOURO_DIRETO",
        operation_review_confirmed=True,
        iof_applicable=False,
    )

    assert result.income_tax_status == "READY"
    assert result.can_calculate_income_tax is True
    assert result.iof_status == "NOT_APPLICABLE"
    assert result.can_calculate_iof is False



@pytest.mark.parametrize("product", ["CDB", "RDB"])
def test_fixed_income_products_allow_income_tax_calculation(product):
    result = evaluate_tax_treatment(
        product,
        iof_applicable=True,
    )

    assert result.can_calculate_income_tax is True


def test_unknown_product_is_rejected():
    with pytest.raises(ValueError):
        evaluate_tax_treatment("FUND")

def test_tesouro_requires_operation_review_for_iof():
    result = evaluate_tax_treatment(
        "TESOURO_DIRETO",
        operation_review_confirmed=False,
        iof_applicable=True,
    )

    assert result.iof_status == "REVIEW_REQUIRED"
    assert result.can_calculate_iof is False

def test_tesouro_allows_iof_after_operation_review():
    result = evaluate_tax_treatment(
        "TESOURO_DIRETO",
        operation_review_confirmed=True,
        iof_applicable=True,
    )

    assert result.iof_status == "READY"
    assert result.can_calculate_iof is True