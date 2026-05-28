"""Tests for CAS Common Chemistry API client.

Unit tests verify dataclass behavior and initialization.
Integration tests verify actual API calls (require CAS_API_KEY).
"""

import os
from unittest.mock import patch

import pytest

from cmm_ai_automation.clients.cas import (
    CASClient,
    CASLookupError,
    CASResult,
    get_cas_client,
)


class TestCASResult:
    """Tests for CASResult dataclass."""

    def test_result_to_dict(self) -> None:
        """Test CASResult serialization."""
        result = CASResult(
            rn="50-99-7",
            name="D-Glucose",
            name_queried="glucose",
            molecular_formula="C6H12O6",
            molecular_mass=180.16,
            inchi="InChI=1S/C6H12O6/...",
            inchikey="WQZGKKKJIJFFOK-GASJEMHNSA-N",
            smiles="OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
            synonyms=["Dextrose", "Grape sugar"],
            is_mixture=False,
        )

        d = result.to_dict()
        assert d["cas_rn"] == "50-99-7"
        assert d["cas_name"] == "D-Glucose"
        assert d["name_queried"] == "glucose"
        assert d["cas_molecular_formula"] == "C6H12O6"
        assert d["cas_molecular_mass"] == 180.16
        assert d["cas_inchikey"] == "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        assert d["cas_is_mixture"] is False

    def test_result_to_dict_mixture(self) -> None:
        """Test CASResult for a mixture compound."""
        result = CASResult(
            rn="73049-73-7",
            name="Peptone",
            name_queried="peptone",
            molecular_formula=None,
            molecular_mass=None,
            is_mixture=True,
        )

        d = result.to_dict()
        assert d["cas_rn"] == "73049-73-7"
        assert d["cas_molecular_formula"] is None
        assert d["cas_is_mixture"] is True


class TestCASLookupError:
    """Tests for CASLookupError dataclass."""

    def test_error_attributes(self) -> None:
        """Test error dataclass has correct attributes."""
        error = CASLookupError(
            name_queried="invalidcompound",
            error_code="404",
            error_message="Not found",
        )
        assert error.name_queried == "invalidcompound"
        assert error.error_code == "404"
        assert error.error_message == "Not found"


class TestCASClientInit:
    """Tests for CASClient initialization."""

    def test_init_without_api_key_raises(self) -> None:
        """Test that missing API key raises ValueError."""
        # Remove CAS_API_KEY from environment for this test
        env = {k: v for k, v in os.environ.items() if k != "CAS_API_KEY"}
        with patch.dict(os.environ, env, clear=True), pytest.raises(ValueError, match="CAS API key required"):
            CASClient()

    def test_init_with_api_key_arg(self) -> None:
        """Test initialization with api_key argument."""
        client = CASClient(api_key="test-key-123")
        assert client.api_key == "test-key-123"
        assert client.rate_limit_delay == 0.5  # default
        assert client.timeout == 30.0  # default

    def test_init_with_env_var(self) -> None:
        """Test initialization with environment variable."""
        with patch.dict(os.environ, {"CAS_API_KEY": "env-key-456"}):
            client = CASClient()
            assert client.api_key == "env-key-456"

    def test_init_custom_settings(self) -> None:
        """Test initialization with custom settings."""
        client = CASClient(
            api_key="test-key",
            rate_limit_delay=1.0,
            timeout=60.0,
        )
        assert client.rate_limit_delay == 1.0
        assert client.timeout == 60.0


class TestGetCasClient:
    """Tests for get_cas_client helper function."""

    def test_returns_client_when_key_available(self) -> None:
        """Test that client is returned when API key is available."""
        with patch.dict(os.environ, {"CAS_API_KEY": "test-key"}):
            client = get_cas_client()
            assert client is not None
            assert isinstance(client, CASClient)

    def test_returns_none_when_no_key(self) -> None:
        """Test that None is returned when no API key."""
        env = {k: v for k, v in os.environ.items() if k != "CAS_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            client = get_cas_client()
            assert client is None


class TestCASClientIntegration:
    """Integration tests requiring CAS_API_KEY.

    These tests make real API calls to CAS Common Chemistry.
    They're marked as integration tests and skipped by default.
    Run with: pytest -m integration --run-integration
    """

    @pytest.fixture
    def client(self) -> CASClient | None:
        """Get CAS client if API key is available."""
        return get_cas_client()

    @pytest.mark.integration
    def test_search_glucose(self, client: CASClient | None) -> None:
        """Test searching for glucose."""
        if client is None:
            pytest.skip("CAS_API_KEY not set")
        assert client is not None  # Type narrowing for mypy

        results = client.search_by_name("glucose")
        assert isinstance(results, list)
        assert len(results) > 0

        # Should find D-glucose
        rns = [r.rn for r in results]
        assert "50-99-7" in rns or any("glucose" in r.name.lower() for r in results)

    @pytest.mark.integration
    def test_get_glucose_by_rn(self, client: CASClient | None) -> None:
        """Test looking up glucose by CAS RN."""
        if client is None:
            pytest.skip("CAS_API_KEY not set")
        assert client is not None  # Type narrowing for mypy

        result = client.get_by_rn("50-99-7")
        assert isinstance(result, CASResult)
        assert result.rn == "50-99-7"
        assert result.molecular_formula == "C6H12O6"
        assert result.is_mixture is False

    @pytest.mark.integration
    def test_get_peptone_mixture(self, client: CASClient | None) -> None:
        """Test that peptone is correctly identified as mixture."""
        if client is None:
            pytest.skip("CAS_API_KEY not set")
        assert client is not None  # Type narrowing for mypy

        result = client.get_by_rn("73049-73-7")
        if isinstance(result, CASResult):
            # Peptone should be identified as a mixture
            assert result.is_mixture is True
            assert result.molecular_formula is None

    @pytest.mark.integration
    def test_get_magnesium_sulfate(self, client: CASClient | None) -> None:
        """Test looking up magnesium sulfate."""
        if client is None:
            pytest.skip("CAS_API_KEY not set")
        assert client is not None  # Type narrowing for mypy

        result = client.get_by_rn("7487-88-9")
        assert isinstance(result, CASResult)
        assert result.rn == "7487-88-9"
        assert result.name is not None
        assert result.is_mixture is False

    @pytest.mark.integration
    def test_get_invalid_rn(self, client: CASClient | None) -> None:
        """Test that invalid CAS RN returns error."""
        if client is None:
            pytest.skip("CAS_API_KEY not set")
        assert client is not None  # Type narrowing for mypy

        result = client.get_by_rn("999-99-9")
        # Invalid CAS RN should return an error, not a result
        assert isinstance(result, CASLookupError)
