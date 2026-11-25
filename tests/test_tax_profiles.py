
import pytest

from src.taxation.profiles import (
    TAX_PROFILES,
    IncomeTaxPolicy,
    IofPolicy,
    get_tax_profile,
)


def test_all_expected_products_are_registered():
    expected = {
        "CDB",
        "RDB",
        "TESOURO_DIRETO",
        "LCI",
        "LCA",
    }

    assert set(TAX_PROFILES.keys()) == expected


def test_cdb_tax_profile():
    profile = get_tax_profile("CDB")

    assert profile.income_tax_policy == (
        IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME
    )
    assert profile.iof_policy == (
        IofPolicy.REGRESSIVE_WHEN_APPLICABLE
    )


def test_rdb_tax_profile():
    profile = get_tax_profile("RDB")

    assert profile.income_tax_policy == (
        IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME
    )
    assert profile.iof_policy == (
        IofPolicy.REGRESSIVE_WHEN_APPLICABLE
    )


def test_tesouro_direto_requires_operation_review():
    profile = get_tax_profile("TESOURO_DIRETO")

    assert profile.income_tax_policy == (
        IncomeTaxPolicy.REGRESSIVE_FIXED_INCOME
    )
    assert profile.requires_operation_review is True


def test_lci_requires_eligibility_and_operation_review():
    profile = get_tax_profile("LCI")

    assert profile.income_tax_policy == (
        IncomeTaxPolicy.EXEMPT_IF_ELIGIBLE
    )
    assert profile.iof_policy == (
        IofPolicy.OPERATION_REVIEW_REQUIRED
    )
    assert profile.requires_eligibility_check is True
    assert profile.requires_operation_review is True


def test_lca_requires_eligibility_check():
    profile = get_tax_profile("LCA")

    assert profile.income_tax_policy == (
        IncomeTaxPolicy.EXEMPT_IF_ELIGIBLE
    )
    assert profile.iof_policy == (
        IofPolicy.ZERO_FOR_QUALIFYING_OPERATION
    )
    assert profile.requires_eligibility_check is True


def test_product_code_is_case_insensitive():
    assert get_tax_profile("cdb") == get_tax_profile("CDB")


def test_product_code_accepts_surrounding_spaces():
    assert get_tax_profile(" CDB ") == get_tax_profile("CDB")


@pytest.mark.parametrize(
    "invalid_code",
    [
        "",
        " ",
        None,
        123,
        "FUND",
        "POUPANCA",
    ],
)
def test_invalid_product_code_is_rejected(invalid_code):
    with pytest.raises(ValueError):
        get_tax_profile(invalid_code)


def test_tax_profile_is_immutable():
    profile = get_tax_profile("CDB")

    with pytest.raises(AttributeError):
        profile.product_code = "RDB"
