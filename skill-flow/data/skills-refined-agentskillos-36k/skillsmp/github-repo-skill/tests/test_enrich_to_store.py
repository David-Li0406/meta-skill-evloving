"""Tests for the enrich_to_store module."""

from cmm_ai_automation.scripts.enrich_to_store import normalize_inchikey


class TestNormalizeInchikey:
    """Tests for InChIKey normalization."""

    def test_normalize_bare_inchikey(self) -> None:
        """Bare InChIKey should be returned unchanged."""
        inchikey = "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        assert normalize_inchikey(inchikey) == "WQZGKKKJIJFFOK-GASJEMHNSA-N"

    def test_normalize_inchikey_equals_prefix(self) -> None:
        """InChIKey= prefix should be stripped."""
        inchikey = "InChIKey=GFHNAMRJFCEERV-UHFFFAOYSA-L"
        assert normalize_inchikey(inchikey) == "GFHNAMRJFCEERV-UHFFFAOYSA-L"

    def test_normalize_inchikey_colon_prefix(self) -> None:
        """INCHIKEY: prefix should be stripped."""
        inchikey = "INCHIKEY:XLYOFNOQVPJJNP-UHFFFAOYSA-N"
        assert normalize_inchikey(inchikey) == "XLYOFNOQVPJJNP-UHFFFAOYSA-N"

    def test_normalize_lowercase_prefix(self) -> None:
        """inchikey: lowercase prefix should be stripped."""
        inchikey = "inchikey:XLYOFNOQVPJJNP-UHFFFAOYSA-N"
        assert normalize_inchikey(inchikey) == "XLYOFNOQVPJJNP-UHFFFAOYSA-N"

    def test_normalize_none(self) -> None:
        """None should return None."""
        assert normalize_inchikey(None) is None

    def test_normalize_empty_string(self) -> None:
        """Empty string should return None."""
        assert normalize_inchikey("") is None
