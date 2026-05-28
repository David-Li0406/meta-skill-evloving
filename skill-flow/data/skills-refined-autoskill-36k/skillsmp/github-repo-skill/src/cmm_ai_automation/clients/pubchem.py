"""PubChem PUG-REST API client.

A thin, typed wrapper around PubChem's PUG-REST JSON API for compound lookups.

References:
    - PUG-REST docs: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
    - CHEMINF ontology: https://pmc.ncbi.nlm.nih.gov/articles/PMC3184996/
"""

import json
import logging
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import requests

from cmm_ai_automation.clients.base import HTTPClientBase

logger = logging.getLogger(__name__)

# PubChem rate limit: max 5 requests per second
# We use 0.25s delay to stay well under limit
PUBCHEM_RATE_LIMIT_DELAY = 0.25

# Properties to fetch from PubChem
# See: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest#section=Compound-Property-Tables
COMPOUND_PROPERTIES = [
    "MolecularFormula",
    "MolecularWeight",
    "CanonicalSMILES",
    "IsomericSMILES",
    "InChI",
    "InChIKey",
    "IUPACName",
    "Title",  # Common/preferred name
    "XLogP",
    "ExactMass",
    "MonoisotopicMass",
    "Charge",
]


@dataclass
class CompoundResult:
    """Result from a PubChem compound lookup.

    Field names match PubChem PUG-REST API property names.
    See: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest#section=Compound-Property-Tables

    Attributes:
        CID: PubChem Compound ID
        name_queried: The name we searched for (not a PubChem field)
        MolecularFormula: Chemical formula (e.g., "C6H12O6")
        MolecularWeight: Molecular weight in g/mol
        CanonicalSMILES: Canonical SMILES string (no stereochemistry)
        IsomericSMILES: Isomeric SMILES (with stereochemistry)
        InChI: Full InChI string
        InChIKey: InChIKey hash (27 characters)
        IUPACName: IUPAC systematic name
        Title: Common/preferred name from PubChem
        ExactMass: Exact mass
        MonoisotopicMass: Monoisotopic mass
        Charge: Formal charge
        XLogP: Computed XLogP (partition coefficient)
        CAS: CAS Registry Number (from cross-references)
        ChEBI: ChEBI identifier (from cross-references)
        Wikidata: Wikidata entity ID (from cross-references)
    """

    CID: int
    name_queried: str
    MolecularFormula: str | None = None
    MolecularWeight: float | None = None
    CanonicalSMILES: str | None = None
    IsomericSMILES: str | None = None
    InChI: str | None = None
    InChIKey: str | None = None
    IUPACName: str | None = None
    Title: str | None = None
    ExactMass: float | None = None
    MonoisotopicMass: float | None = None
    Charge: int | None = None
    XLogP: float | None = None
    CAS: str | None = None
    ChEBI: str | None = None
    Wikidata: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "CID": self.CID,
            "name_queried": self.name_queried,
            "MolecularFormula": self.MolecularFormula,
            "MolecularWeight": self.MolecularWeight,
            "CanonicalSMILES": self.CanonicalSMILES,
            "IsomericSMILES": self.IsomericSMILES,
            "InChI": self.InChI,
            "InChIKey": self.InChIKey,
            "IUPACName": self.IUPACName,
            "Title": self.Title,
            "ExactMass": self.ExactMass,
            "MonoisotopicMass": self.MonoisotopicMass,
            "Charge": self.Charge,
            "XLogP": self.XLogP,
            "CAS": self.CAS,
            "ChEBI": self.ChEBI,
            "Wikidata": self.Wikidata,
        }


@dataclass
class LookupError:
    """Error from a failed PubChem lookup.

    Attributes:
        name_queried: The name we searched for
        error_code: PubChem error code (e.g., "PUGREST.NotFound")
        error_message: Human-readable error message
    """

    name_queried: str
    error_code: str
    error_message: str


class PubChemClient(HTTPClientBase):
    """Client for PubChem PUG-REST API.

    Example:
        >>> client = PubChemClient()
        >>> result = client.get_compound_by_name("glucose")
        >>> if isinstance(result, CompoundResult):
        ...     print(f"CID: {result.CID}, InChIKey: {result.InChIKey}")
        CID: 5793, InChIKey: WQZGKKKJIJFFOK-GASJEMHNSA-N
    """

    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(
        self,
        rate_limit_delay: float = PUBCHEM_RATE_LIMIT_DELAY,
        timeout: float = 30.0,
    ):
        """Initialize PubChem client.

        Args:
            rate_limit_delay: Seconds to wait between requests (default: 0.25)
            timeout: Request timeout in seconds (default: 30)
        """
        super().__init__(rate_limit_delay=rate_limit_delay, timeout=timeout)

    def get_cids_by_name(self, name: str) -> list[int] | LookupError:
        """Get all CIDs matching a compound name.

        Args:
            name: Chemical name to search

        Returns:
            List of CIDs on success, LookupError on failure
        """
        encoded_name = quote(name)
        url = f"{self.BASE_URL}/compound/name/{encoded_name}/cids/JSON"

        try:
            data = self._get_json(url)
        except requests.HTTPError as e:
            try:
                error_data = e.response.json()
                fault = error_data.get("Fault", {})
                return LookupError(
                    name_queried=name,
                    error_code=fault.get("Code", "UNKNOWN"),
                    error_message=fault.get("Message", str(e)),
                )
            except (json.JSONDecodeError, AttributeError, KeyError):
                return LookupError(
                    name_queried=name,
                    error_code="HTTP_ERROR",
                    error_message=str(e),
                )
        except requests.RequestException as e:
            return LookupError(
                name_queried=name,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        try:
            cids: list[int] = data["IdentifierList"]["CID"]
            return cids
        except (KeyError, IndexError):
            return []

    def get_compounds_by_name(self, name: str) -> list[CompoundResult] | LookupError:
        """Look up all compounds matching a name.

        Args:
            name: Chemical name to search (e.g., "glucose", "magnesium sulfate heptahydrate")

        Returns:
            List of CompoundResult on success, LookupError on failure
        """
        # First get all matching CIDs
        cids_result = self.get_cids_by_name(name)
        if isinstance(cids_result, LookupError):
            return cids_result

        if not cids_result:
            return LookupError(
                name_queried=name,
                error_code="NO_RESULTS",
                error_message="No compounds found for this name",
            )

        # Fetch properties for all CIDs
        results = []
        for cid in cids_result:
            result = self.get_compound_by_cid(cid)
            if isinstance(result, CompoundResult):
                result.name_queried = name
                results.append(result)

        return (
            results
            if results
            else LookupError(
                name_queried=name,
                error_code="NO_VALID_RESULTS",
                error_message=f"Found {len(cids_result)} CIDs but could not fetch properties",
            )
        )

    def get_compound_by_name(self, name: str) -> CompoundResult | LookupError:
        """Look up a compound by name (returns first match only).

        For all matches, use get_compounds_by_name() instead.

        Args:
            name: Chemical name to search (e.g., "glucose", "magnesium sulfate heptahydrate")

        Returns:
            CompoundResult on success, LookupError on failure
        """
        # URL-encode the name
        encoded_name = quote(name)
        properties = ",".join(COMPOUND_PROPERTIES)
        url = f"{self.BASE_URL}/compound/name/{encoded_name}/property/{properties}/JSON"

        try:
            data = self._get_json(url)
        except requests.HTTPError as e:
            # Try to parse PubChem error response
            try:
                error_data = e.response.json()
                fault = error_data.get("Fault", {})
                return LookupError(
                    name_queried=name,
                    error_code=fault.get("Code", "UNKNOWN"),
                    error_message=fault.get("Message", str(e)),
                )
            except (json.JSONDecodeError, AttributeError, KeyError):
                return LookupError(
                    name_queried=name,
                    error_code="HTTP_ERROR",
                    error_message=str(e),
                )
        except requests.RequestException as e:
            return LookupError(
                name_queried=name,
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        # Parse successful response
        # Note: PubChem returns "ConnectivitySMILES" for canonical and "SMILES" for isomeric
        try:
            props = data["PropertyTable"]["Properties"][0]
            return CompoundResult(
                CID=props["CID"],
                name_queried=name,
                MolecularFormula=props.get("MolecularFormula"),
                MolecularWeight=_to_float(props.get("MolecularWeight")),
                CanonicalSMILES=props.get("ConnectivitySMILES"),
                IsomericSMILES=props.get("SMILES"),
                InChI=props.get("InChI"),
                InChIKey=props.get("InChIKey"),
                IUPACName=props.get("IUPACName"),
                Title=props.get("Title"),
                ExactMass=_to_float(props.get("ExactMass")),
                MonoisotopicMass=_to_float(props.get("MonoisotopicMass")),
                Charge=props.get("Charge"),
                XLogP=_to_float(props.get("XLogP")),
            )
        except (KeyError, IndexError) as e:
            return LookupError(
                name_queried=name,
                error_code="PARSE_ERROR",
                error_message=f"Failed to parse response: {e}",
            )

    def get_compound_by_cid(self, cid: int) -> CompoundResult | LookupError:
        """Look up a compound by PubChem CID.

        Args:
            cid: PubChem Compound ID

        Returns:
            CompoundResult on success, LookupError on failure
        """
        properties = ",".join(COMPOUND_PROPERTIES)
        url = f"{self.BASE_URL}/compound/cid/{cid}/property/{properties}/JSON"

        try:
            data = self._get_json(url)
        except requests.HTTPError as e:
            try:
                error_data = e.response.json()
                fault = error_data.get("Fault", {})
                return LookupError(
                    name_queried=f"CID:{cid}",
                    error_code=fault.get("Code", "UNKNOWN"),
                    error_message=fault.get("Message", str(e)),
                )
            except (json.JSONDecodeError, AttributeError, KeyError):
                return LookupError(
                    name_queried=f"CID:{cid}",
                    error_code="HTTP_ERROR",
                    error_message=str(e),
                )
        except requests.RequestException as e:
            return LookupError(
                name_queried=f"CID:{cid}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        try:
            props = data["PropertyTable"]["Properties"][0]
            return CompoundResult(
                CID=props["CID"],
                name_queried=f"CID:{cid}",
                MolecularFormula=props.get("MolecularFormula"),
                MolecularWeight=_to_float(props.get("MolecularWeight")),
                CanonicalSMILES=props.get("ConnectivitySMILES"),
                IsomericSMILES=props.get("SMILES"),
                InChI=props.get("InChI"),
                InChIKey=props.get("InChIKey"),
                IUPACName=props.get("IUPACName"),
                Title=props.get("Title"),
                ExactMass=_to_float(props.get("ExactMass")),
                MonoisotopicMass=_to_float(props.get("MonoisotopicMass")),
                Charge=props.get("Charge"),
                XLogP=_to_float(props.get("XLogP")),
            )
        except (KeyError, IndexError) as e:
            return LookupError(
                name_queried=f"CID:{cid}",
                error_code="PARSE_ERROR",
                error_message=f"Failed to parse response: {e}",
            )

    def get_synonyms(self, cid: int) -> list[str] | LookupError:
        """Get all synonyms for a compound by CID.

        Args:
            cid: PubChem Compound ID

        Returns:
            List of synonym strings on success, LookupError on failure
        """
        url = f"{self.BASE_URL}/compound/cid/{cid}/synonyms/JSON"

        try:
            data = self._get_json(url)
        except requests.HTTPError as e:
            try:
                error_data = e.response.json()
                fault = error_data.get("Fault", {})
                return LookupError(
                    name_queried=f"CID:{cid}",
                    error_code=fault.get("Code", "UNKNOWN"),
                    error_message=fault.get("Message", str(e)),
                )
            except (json.JSONDecodeError, AttributeError, KeyError):
                return LookupError(
                    name_queried=f"CID:{cid}",
                    error_code="HTTP_ERROR",
                    error_message=str(e),
                )
        except requests.RequestException as e:
            return LookupError(
                name_queried=f"CID:{cid}",
                error_code="REQUEST_ERROR",
                error_message=str(e),
            )

        try:
            synonyms: list[str] = data["InformationList"]["Information"][0]["Synonym"]
            return synonyms
        except (KeyError, IndexError):
            return []

    def get_xrefs(self, cid: int) -> dict[str, str | None]:
        """Get cross-references (CAS, ChEBI, Wikidata) for a compound.

        Uses PUG-VIEW API to fetch annotation data.

        Args:
            cid: PubChem Compound ID

        Returns:
            Dictionary with keys 'CAS', 'ChEBI', 'Wikidata' (values may be None)
        """
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"

        result: dict[str, str | None] = {"CAS": None, "ChEBI": None, "Wikidata": None}

        try:
            self._wait_for_rate_limit()
            logger.debug(f"GET {url}")
            response = self._session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.warning(f"Failed to fetch xrefs for CID {cid}: {e}")
            return result

        # Parse the nested PUG-VIEW structure
        try:
            record = data.get("Record", {})
            sections = record.get("Section", [])

            for section in sections:
                if section.get("TOCHeading") == "Names and Identifiers":
                    self._extract_xrefs_from_section(section, result)
                    break
        except (KeyError, TypeError) as e:
            logger.warning(f"Failed to parse xrefs for CID {cid}: {e}")

        return result

    def _extract_xrefs_from_section(self, section: dict[str, Any], result: dict[str, str | None]) -> None:
        """Extract CAS, ChEBI, Wikidata from a Names and Identifiers section."""
        for subsection in section.get("Section", []):
            toc = subsection.get("TOCHeading", "")

            if toc == "Other Identifiers":
                for item in subsection.get("Section", []):
                    item_toc = item.get("TOCHeading", "")
                    if item_toc == "CAS" and result["CAS"] is None:
                        result["CAS"] = self._get_first_string_value(item)
                    elif item_toc == "ChEBI ID" and result["ChEBI"] is None:
                        result["ChEBI"] = self._get_first_string_value(item)
                    elif item_toc == "Wikidata" and result["Wikidata"] is None:
                        result["Wikidata"] = self._get_first_string_value(item)

            # Also check direct subsections
            if toc == "CAS" and result["CAS"] is None:
                result["CAS"] = self._get_first_string_value(subsection)
            elif toc == "ChEBI ID" and result["ChEBI"] is None:
                result["ChEBI"] = self._get_first_string_value(subsection)
            elif toc == "Wikidata" and result["Wikidata"] is None:
                result["Wikidata"] = self._get_first_string_value(subsection)

    def _get_first_string_value(self, section: dict[str, Any]) -> str | None:
        """Extract the first string value from a PUG-VIEW section."""
        try:
            info_list = section.get("Information", [])
            if info_list:
                value = info_list[0].get("Value", {})
                markup_list = value.get("StringWithMarkup", [])
                if markup_list:
                    string_value = markup_list[0].get("String")
                    result: str | None = str(string_value) if string_value is not None else None
                    return result
        except (KeyError, IndexError, TypeError):
            pass
        return None


def _to_float(value: Any) -> float | None:
    """Safely convert a value to float."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
