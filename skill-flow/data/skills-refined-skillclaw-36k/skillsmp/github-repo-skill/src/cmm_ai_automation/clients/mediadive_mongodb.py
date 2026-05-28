"""MediaDive MongoDB client.

A client for querying MediaDive data from a local MongoDB database.
The data is loaded by the load_mediadive_mongodb.py script.

This provides faster lookups than the REST API and enables searching
by various fields (name, CAS-RN, ChEBI, etc.) that aren't available
via the REST API.

MediaDive is authoritative for MediaDive ingredient/solution IDs.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

logger = logging.getLogger(__name__)

# Default MongoDB connection settings
DEFAULT_MONGODB_URI = "mongodb://localhost:27017"
DEFAULT_DATABASE_NAME = "mediadive"


@dataclass
class MediaDiveMongoIngredient:
    """Ingredient from MediaDive MongoDB.

    MediaDive is authoritative for these IDs.

    Attributes:
        id: MediaDive ingredient ID
        name: Ingredient name
        cas_rn: CAS Registry Number
        chebi: ChEBI ID
        pubchem: PubChem CID
        kegg: KEGG Compound ID
        metacyc: MetaCyc ID
        formula: Molecular formula
        mass: Molecular mass
        is_complex: True if complex/undefined mixture
        synonyms: List of synonym names
    """

    id: int
    name: str
    cas_rn: str | None = None
    chebi: int | None = None
    pubchem: int | None = None
    kegg: str | None = None
    metacyc: str | None = None
    formula: str | None = None
    mass: float | None = None
    is_complex: bool = False
    synonyms: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "mediadive_id": self.id,
            "mediadive_name": self.name,
            "mediadive_cas_rn": self.cas_rn,
            "mediadive_chebi": self.chebi,
            "mediadive_pubchem": self.pubchem,
            "mediadive_kegg": self.kegg,
            "mediadive_metacyc": self.metacyc,
            "mediadive_formula": self.formula,
            "mediadive_mass": self.mass,
            "mediadive_is_complex": self.is_complex,
        }


@dataclass
class MediaDiveMongoSolution:
    """Solution from MediaDive MongoDB.

    Aligns with LinkML Solution class slots.
    MediaDive is authoritative for solution IDs.

    Attributes:
        id: MediaDive solution ID (authoritative)
        name: Solution name (maps to LinkML: name)
        volume: Total volume in ml
        recipe: Recipe items - ingredient components (maps to LinkML: has_ingredient_component)
        steps: Preparation steps
    """

    id: int
    name: str
    volume: float | None = None
    recipe: list[dict[str, Any]] = field(default_factory=list)
    steps: list[dict[str, Any]] = field(default_factory=list)

    def to_curie(self) -> str:
        """Return authoritative CURIE for this solution."""
        return f"mediadive.solution:{self.id}"


@dataclass
class MediaDiveMongoMedium:
    """Growth medium from MediaDive MongoDB.

    Aligns with LinkML GrowthMedium class slots.
    MediaDive is authoritative for medium IDs.

    Attributes:
        id: MediaDive medium ID (authoritative)
        name: Medium name (maps to LinkML: name)
        complex_medium: Whether this is a complex medium (maps to LinkML: medium_type)
        source: Data source (e.g., "DSMZ")
        link: URL to source documentation (maps to LinkML: source_reference)
        min_ph: Minimum pH (maps to LinkML: ph)
        max_ph: Maximum pH
        reference: Literature reference
        description: Medium description (maps to LinkML: description)
    """

    id: int
    name: str
    complex_medium: bool = False
    source: str | None = None
    link: str | None = None
    min_ph: float | None = None
    max_ph: float | None = None
    reference: str | None = None
    description: str | None = None

    def to_curie(self) -> str:
        """Return authoritative CURIE for this medium."""
        return f"mediadive.medium:{self.id}"


@dataclass
class MediaDiveMongoStrainGrowth:
    """Strain-medium growth relationship from MediaDive MongoDB.

    Aligns with LinkML GrowthPreference class slots.

    Attributes:
        strain_id: MediaDive internal strain ID
        species: Species name (maps to LinkML Strain: scientific_name)
        ccno: Culture collection number (e.g., "DSM 1")
        growth: Growth result (maps to LinkML GrowthPreference: grows)
        bacdive_id: BacDive strain ID for cross-reference (maps to LinkML Strain: bacdive_id)
        domain: Domain (B = Bacteria, A = Archaea)
    """

    strain_id: int
    species: str
    ccno: str
    growth: bool
    bacdive_id: int | None = None
    domain: str | None = None

    def strain_curie(self) -> str | None:
        """Return strain CURIE using BacDive ID if available."""
        if self.bacdive_id:
            return f"bacdive.strain:{self.bacdive_id}"
        return None


@dataclass
class MediaDiveMongoRecipeItem:
    """Recipe item from MediaDive solution/medium composition.

    Aligns with LinkML IngredientComponent class slots.

    Attributes:
        compound: Ingredient name
        compound_id: MediaDive ingredient ID
        amount: Numeric amount
        unit: Unit of measurement
        g_l: Grams per liter (calculated)
        mmol_l: Millimoles per liter (calculated)
        optional: Whether ingredient is optional
        condition: Conditional usage note
        solution: Solution name if this is a solution reference
        solution_id: MediaDive solution ID if this is a solution reference
    """

    compound: str
    compound_id: int | None = None
    amount: float | None = None
    unit: str | None = None
    g_l: float | None = None
    mmol_l: float | None = None
    optional: bool = False
    condition: str | None = None
    solution: str | None = None
    solution_id: int | None = None

    def ingredient_curie(self) -> str | None:
        """Return ingredient CURIE if compound_id is set."""
        if self.compound_id:
            return f"mediadive.ingredient:{self.compound_id}"
        return None

    def solution_curie(self) -> str | None:
        """Return solution CURIE if solution_id is set."""
        if self.solution_id:
            return f"mediadive.solution:{self.solution_id}"
        return None


@dataclass
class MediaDiveMongoLookupError:
    """Error from a failed MongoDB lookup.

    Attributes:
        query: The query that was made
        error_code: Error code
        error_message: Human-readable error message
    """

    query: str
    error_code: str
    error_message: str


class MediaDiveMongoClient:
    """Client for MediaDive data in MongoDB.

    Provides fast lookups and searching capabilities not available
    via the REST API.

    MediaDive is the authoritative source for MediaDive ingredient/solution IDs.

    Example:
        >>> client = MediaDiveMongoClient()
        >>> result = client.get_ingredient_by_id(1)
        >>> if isinstance(result, MediaDiveMongoIngredient):
        ...     print(f"Name: {result.name}, CAS: {result.cas_rn}")

        >>> # Search by name
        >>> results = client.search_ingredients_by_name("peptone")
        >>> for r in results:
        ...     print(f"{r.id}: {r.name}")

        >>> # Find by ChEBI
        >>> result = client.find_ingredient_by_chebi(30729)
    """

    def __init__(
        self,
        mongodb_uri: str = DEFAULT_MONGODB_URI,
        database_name: str = DEFAULT_DATABASE_NAME,
    ):
        """Initialize MediaDive MongoDB client.

        Args:
            mongodb_uri: MongoDB connection URI
            database_name: Name of the MediaDive database
        """
        self.mongodb_uri = mongodb_uri
        self.database_name = database_name
        self._client: MongoClient[dict[str, Any]] | None = None
        self._db: Database[dict[str, Any]] | None = None

    def _get_db(self) -> Database[dict[str, Any]]:
        """Get or create MongoDB database connection."""
        if self._db is None:
            self._client = MongoClient(self.mongodb_uri)
            self._db = self._client[self.database_name]
        return self._db

    def _get_ingredients_collection(self) -> Collection[dict[str, Any]]:
        """Get the ingredients collection."""
        return self._get_db().ingredients

    def _get_solutions_collection(self) -> Collection[dict[str, Any]]:
        """Get the solutions collection."""
        return self._get_db().solutions

    def _get_media_collection(self) -> Collection[dict[str, Any]]:
        """Get the media collection."""
        return self._get_db().media

    def _get_medium_strains_collection(self) -> Collection[dict[str, Any]]:
        """Get the medium_strains collection (strain-medium growth relationships)."""
        return self._get_db().medium_strains

    def _get_solution_details_collection(self) -> Collection[dict[str, Any]]:
        """Get the solution_details collection (full recipes)."""
        return self._get_db().solution_details

    def _get_media_details_collection(self) -> Collection[dict[str, Any]]:
        """Get the media_details collection (full compositions)."""
        return self._get_db().media_details

    def close(self) -> None:
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    # =========================================================================
    # Ingredient Lookups (MediaDive is authoritative for these)
    # =========================================================================

    def get_ingredient_by_id(self, ingredient_id: int) -> MediaDiveMongoIngredient | MediaDiveMongoLookupError:
        """Get an ingredient by MediaDive ID.

        Args:
            ingredient_id: MediaDive ingredient ID

        Returns:
            MediaDiveMongoIngredient on success, MediaDiveMongoLookupError on failure
        """
        try:
            collection = self._get_ingredients_collection()
            doc = collection.find_one({"_id": ingredient_id})

            if not doc:
                return MediaDiveMongoLookupError(
                    query=f"ingredient_id:{ingredient_id}",
                    error_code="NOT_FOUND",
                    error_message=f"Ingredient ID {ingredient_id} not found",
                )

            return self._parse_ingredient(doc)

        except Exception as e:
            return MediaDiveMongoLookupError(
                query=f"ingredient_id:{ingredient_id}",
                error_code="MONGODB_ERROR",
                error_message=str(e),
            )

    def search_ingredients_by_name(self, name: str, exact: bool = False) -> list[MediaDiveMongoIngredient]:
        """Search ingredients by name.

        Args:
            name: Name to search for
            exact: If True, require exact match (case-insensitive)

        Returns:
            List of matching ingredients
        """
        try:
            collection = self._get_ingredients_collection()

            if exact:
                # Case-insensitive exact match
                query = {"name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}}
            else:
                # Case-insensitive substring match
                query = {"name": {"$regex": re.escape(name), "$options": "i"}}

            results = []
            for doc in collection.find(query):
                results.append(self._parse_ingredient(doc))

            return results

        except Exception as e:
            logger.warning(f"Error searching ingredients by name '{name}': {e}")
            return []

    def find_ingredient_by_cas(self, cas_rn: str) -> MediaDiveMongoIngredient | None:
        """Find an ingredient by CAS Registry Number.

        Args:
            cas_rn: CAS Registry Number (e.g., "50-99-7")

        Returns:
            MediaDiveMongoIngredient if found, None otherwise
        """
        try:
            collection = self._get_ingredients_collection()
            doc = collection.find_one({"CAS-RN": cas_rn})

            if doc:
                return self._parse_ingredient(doc)
            return None

        except Exception as e:
            logger.warning(f"Error finding ingredient by CAS '{cas_rn}': {e}")
            return None

    def find_ingredient_by_chebi(self, chebi_id: int | str) -> MediaDiveMongoIngredient | None:
        """Find an ingredient by ChEBI ID.

        Args:
            chebi_id: ChEBI ID (numeric, without CHEBI: prefix)

        Returns:
            MediaDiveMongoIngredient if found, None otherwise
        """
        try:
            # Normalize to int
            chebi_int = int(str(chebi_id).replace("CHEBI:", ""))

            collection = self._get_ingredients_collection()
            doc = collection.find_one({"ChEBI": chebi_int})

            if doc:
                return self._parse_ingredient(doc)
            return None

        except Exception as e:
            logger.warning(f"Error finding ingredient by ChEBI '{chebi_id}': {e}")
            return None

    def find_ingredient_by_pubchem(self, pubchem_cid: int) -> MediaDiveMongoIngredient | None:
        """Find an ingredient by PubChem CID.

        Args:
            pubchem_cid: PubChem Compound ID

        Returns:
            MediaDiveMongoIngredient if found, None otherwise
        """
        try:
            collection = self._get_ingredients_collection()
            doc = collection.find_one({"PubChem": pubchem_cid})

            if doc:
                return self._parse_ingredient(doc)
            return None

        except Exception as e:
            logger.warning(f"Error finding ingredient by PubChem '{pubchem_cid}': {e}")
            return None

    def find_ingredient_by_kegg(self, kegg_id: str) -> MediaDiveMongoIngredient | None:
        """Find an ingredient by KEGG Compound ID.

        Args:
            kegg_id: KEGG Compound ID (e.g., "C00031")

        Returns:
            MediaDiveMongoIngredient if found, None otherwise
        """
        try:
            collection = self._get_ingredients_collection()
            doc = collection.find_one({"KEGG-Compound": kegg_id})

            if doc:
                return self._parse_ingredient(doc)
            return None

        except Exception as e:
            logger.warning(f"Error finding ingredient by KEGG '{kegg_id}': {e}")
            return None

    def get_all_ingredients_with_chebi(self) -> list[MediaDiveMongoIngredient]:
        """Get all ingredients that have a ChEBI ID.

        Returns:
            List of ingredients with ChEBI IDs
        """
        try:
            collection = self._get_ingredients_collection()
            results = []

            for doc in collection.find({"ChEBI": {"$ne": None}}):
                results.append(self._parse_ingredient(doc))

            return results

        except Exception as e:
            logger.warning(f"Error getting ingredients with ChEBI: {e}")
            return []

    def get_all_ingredients_with_cas(self) -> list[MediaDiveMongoIngredient]:
        """Get all ingredients that have a CAS Registry Number.

        Returns:
            List of ingredients with CAS-RN
        """
        try:
            collection = self._get_ingredients_collection()
            results = []

            for doc in collection.find({"CAS-RN": {"$ne": None}}):
                results.append(self._parse_ingredient(doc))

            return results

        except Exception as e:
            logger.warning(f"Error getting ingredients with CAS: {e}")
            return []

    # =========================================================================
    # Solution Lookups
    # =========================================================================

    def get_solution_by_id(self, solution_id: int) -> MediaDiveMongoSolution | MediaDiveMongoLookupError:
        """Get a solution by MediaDive ID.

        Args:
            solution_id: MediaDive solution ID

        Returns:
            MediaDiveMongoSolution on success, MediaDiveMongoLookupError on failure
        """
        try:
            collection = self._get_solutions_collection()
            doc = collection.find_one({"_id": solution_id})

            if not doc:
                return MediaDiveMongoLookupError(
                    query=f"solution_id:{solution_id}",
                    error_code="NOT_FOUND",
                    error_message=f"Solution ID {solution_id} not found",
                )

            return self._parse_solution(doc)

        except Exception as e:
            return MediaDiveMongoLookupError(
                query=f"solution_id:{solution_id}",
                error_code="MONGODB_ERROR",
                error_message=str(e),
            )

    def search_solutions_by_name(self, name: str, exact: bool = False) -> list[MediaDiveMongoSolution]:
        """Search solutions by name.

        Args:
            name: Name to search for
            exact: If True, require exact match (case-insensitive)

        Returns:
            List of matching solutions
        """
        try:
            collection = self._get_solutions_collection()

            if exact:
                query = {"name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}}
            else:
                query = {"name": {"$regex": re.escape(name), "$options": "i"}}

            results = []
            for doc in collection.find(query):
                results.append(self._parse_solution(doc))

            return results

        except Exception as e:
            logger.warning(f"Error searching solutions by name '{name}': {e}")
            return []

    # =========================================================================
    # Media Lookups
    # =========================================================================

    def get_medium_by_id(self, medium_id: int) -> MediaDiveMongoMedium | MediaDiveMongoLookupError:
        """Get a medium by MediaDive ID.

        Args:
            medium_id: MediaDive medium ID

        Returns:
            MediaDiveMongoMedium on success, MediaDiveMongoLookupError on failure
        """
        try:
            collection = self._get_media_collection()
            doc = collection.find_one({"_id": medium_id})

            if not doc:
                return MediaDiveMongoLookupError(
                    query=f"medium_id:{medium_id}",
                    error_code="NOT_FOUND",
                    error_message=f"Medium ID {medium_id} not found",
                )

            return self._parse_medium(doc)

        except Exception as e:
            return MediaDiveMongoLookupError(
                query=f"medium_id:{medium_id}",
                error_code="MONGODB_ERROR",
                error_message=str(e),
            )

    def get_all_media(self) -> list[MediaDiveMongoMedium]:
        """Get all media from the database.

        Returns:
            List of all media records
        """
        try:
            collection = self._get_media_collection()
            results = []

            for doc in collection.find():
                results.append(self._parse_medium(doc))

            return results

        except Exception as e:
            logger.warning(f"Error getting all media: {e}")
            return []

    def search_media_by_name(self, name: str, exact: bool = False) -> list[MediaDiveMongoMedium]:
        """Search media by name.

        Args:
            name: Name to search for
            exact: If True, require exact match (case-insensitive)

        Returns:
            List of matching media
        """
        try:
            collection = self._get_media_collection()

            if exact:
                query = {"name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}}
            else:
                query = {"name": {"$regex": re.escape(name), "$options": "i"}}

            results = []
            for doc in collection.find(query):
                results.append(self._parse_medium(doc))

            return results

        except Exception as e:
            logger.warning(f"Error searching media by name '{name}': {e}")
            return []

    # =========================================================================
    # Medium-Strain Relationships (Growth Data)
    # =========================================================================

    def get_strains_for_medium(self, medium_id: int) -> list[MediaDiveMongoStrainGrowth]:
        """Get all strain growth records for a specific medium.

        Args:
            medium_id: MediaDive medium ID

        Returns:
            List of strain growth records for this medium
        """
        try:
            collection = self._get_medium_strains_collection()
            doc = collection.find_one({"_id": medium_id})

            if not doc or "strains" not in doc:
                return []

            results = []
            for strain_data in doc["strains"]:
                results.append(self._parse_strain_growth(strain_data))

            return results

        except Exception as e:
            logger.warning(f"Error getting strains for medium {medium_id}: {e}")
            return []

    def get_all_medium_strain_relationships(self) -> list[tuple[int, list[MediaDiveMongoStrainGrowth]]]:
        """Get all medium-strain relationships from the database.

        Returns:
            List of (medium_id, strain_growth_list) tuples
        """
        try:
            collection = self._get_medium_strains_collection()
            results = []

            for doc in collection.find():
                medium_id = doc.get("_id")
                strains = []
                for strain_data in doc.get("strains", []):
                    strains.append(self._parse_strain_growth(strain_data))
                if medium_id and strains:
                    results.append((medium_id, strains))

            return results

        except Exception as e:
            logger.warning(f"Error getting medium-strain relationships: {e}")
            return []

    # =========================================================================
    # Solution Details (Full Recipes)
    # =========================================================================

    def get_solution_details(self, solution_id: int) -> MediaDiveMongoSolution | MediaDiveMongoLookupError:
        """Get full solution details including recipe items.

        Args:
            solution_id: MediaDive solution ID

        Returns:
            MediaDiveMongoSolution with full recipe, or error
        """
        try:
            collection = self._get_solution_details_collection()
            doc = collection.find_one({"_id": solution_id})

            if not doc:
                return MediaDiveMongoLookupError(
                    query=f"solution_details:{solution_id}",
                    error_code="NOT_FOUND",
                    error_message=f"Solution details for ID {solution_id} not found",
                )

            return self._parse_solution_details(doc)

        except Exception as e:
            return MediaDiveMongoLookupError(
                query=f"solution_details:{solution_id}",
                error_code="MONGODB_ERROR",
                error_message=str(e),
            )

    def get_all_solution_details(self) -> list[MediaDiveMongoSolution]:
        """Get all solutions with their full recipes.

        Returns:
            List of solutions with recipe details
        """
        try:
            collection = self._get_solution_details_collection()
            results = []

            for doc in collection.find():
                results.append(self._parse_solution_details(doc))

            return results

        except Exception as e:
            logger.warning(f"Error getting all solution details: {e}")
            return []

    # =========================================================================
    # All Ingredients (for bulk export)
    # =========================================================================

    def get_all_ingredients(self) -> list[MediaDiveMongoIngredient]:
        """Get all ingredients from the database.

        Returns:
            List of all ingredient records
        """
        try:
            collection = self._get_ingredients_collection()
            results = []

            for doc in collection.find():
                results.append(self._parse_ingredient(doc))

            return results

        except Exception as e:
            logger.warning(f"Error getting all ingredients: {e}")
            return []

    def get_all_solutions(self) -> list[MediaDiveMongoSolution]:
        """Get all solutions from the database (basic info, not full recipes).

        Returns:
            List of all solution records
        """
        try:
            collection = self._get_solutions_collection()
            results = []

            for doc in collection.find():
                results.append(self._parse_solution(doc))

            return results

        except Exception as e:
            logger.warning(f"Error getting all solutions: {e}")
            return []

    # =========================================================================
    # Stats and Info
    # =========================================================================

    def get_medium_count(self) -> int:
        """Get total number of media in the database."""
        try:
            count: int = int(self._get_media_collection().count_documents({}))
            return count
        except Exception:
            return 0

    def get_ingredient_count(self) -> int:
        """Get total number of ingredients in the database."""
        try:
            count: int = int(self._get_ingredients_collection().count_documents({}))
            return count
        except Exception:
            return 0

    def get_solution_count(self) -> int:
        """Get total number of solutions in the database."""
        try:
            count: int = int(self._get_solutions_collection().count_documents({}))
            return count
        except Exception:
            return 0

    def get_xref_counts(self) -> dict[str, int]:
        """Get counts of ingredients with each type of cross-reference.

        Returns:
            Dict with counts for each xref type
        """
        try:
            collection = self._get_ingredients_collection()
            return {
                "total": collection.count_documents({}),
                "cas_rn": collection.count_documents({"CAS-RN": {"$ne": None}}),
                "chebi": collection.count_documents({"ChEBI": {"$ne": None}}),
                "pubchem": collection.count_documents({"PubChem": {"$ne": None}}),
                "kegg": collection.count_documents({"KEGG-Compound": {"$ne": None}}),
                "metacyc": collection.count_documents({"MetaCyc": {"$ne": None}}),
            }
        except Exception as e:
            logger.warning(f"Error getting xref counts: {e}")
            return {}

    # =========================================================================
    # Parsing
    # =========================================================================

    def _parse_ingredient(self, doc: dict[str, Any]) -> MediaDiveMongoIngredient:
        """Parse a MongoDB document into a MediaDiveMongoIngredient."""
        return MediaDiveMongoIngredient(
            id=doc.get("id", doc.get("_id", 0)),
            name=doc.get("name", ""),
            cas_rn=doc.get("CAS-RN"),
            chebi=doc.get("ChEBI"),
            pubchem=doc.get("PubChem"),
            kegg=doc.get("KEGG-Compound"),
            metacyc=doc.get("MetaCyc"),
            formula=doc.get("formula"),
            mass=doc.get("mass"),
            is_complex=bool(doc.get("complex_compound")),
            synonyms=doc.get("synonyms", []),
        )

    def _parse_solution(self, doc: dict[str, Any]) -> MediaDiveMongoSolution:
        """Parse a MongoDB document into a MediaDiveMongoSolution."""
        return MediaDiveMongoSolution(
            id=doc.get("id", doc.get("_id", 0)),
            name=doc.get("name", ""),
            volume=doc.get("volume"),
            recipe=doc.get("recipe", []),
            steps=doc.get("steps", []),
        )

    def _parse_solution_details(self, doc: dict[str, Any]) -> MediaDiveMongoSolution:
        """Parse a solution_details document into a MediaDiveMongoSolution."""
        return MediaDiveMongoSolution(
            id=doc.get("id", doc.get("_id", 0)),
            name=doc.get("name", ""),
            volume=doc.get("volume"),
            recipe=doc.get("recipe", []),
            steps=doc.get("steps", []),
        )

    def _parse_medium(self, doc: dict[str, Any]) -> MediaDiveMongoMedium:
        """Parse a MongoDB document into a MediaDiveMongoMedium."""
        # Handle complex_medium which may be int (1/0) or string ("yes"/"no")
        complex_val = doc.get("complex_medium")
        if isinstance(complex_val, str):
            complex_medium = complex_val.lower() in ("yes", "true", "1")
        else:
            complex_medium = bool(complex_val)

        return MediaDiveMongoMedium(
            id=doc.get("id", doc.get("_id", 0)),
            name=doc.get("name", ""),
            complex_medium=complex_medium,
            source=doc.get("source"),
            link=doc.get("link"),
            min_ph=doc.get("min_pH"),
            max_ph=doc.get("max_pH"),
            reference=doc.get("reference"),
            description=doc.get("description"),
        )

    def _parse_strain_growth(self, strain_data: dict[str, Any]) -> MediaDiveMongoStrainGrowth:
        """Parse a strain growth record from medium_strains document."""
        # Growth may be int (1/0) or bool
        growth_val = strain_data.get("growth", 1)
        growth = bool(growth_val) if isinstance(growth_val, int) else growth_val

        return MediaDiveMongoStrainGrowth(
            strain_id=strain_data.get("id", 0),
            species=strain_data.get("species", ""),
            ccno=strain_data.get("ccno", ""),
            growth=growth,
            bacdive_id=strain_data.get("bacdive_id"),
            domain=strain_data.get("domain"),
        )

    def _parse_recipe_item(self, item: dict[str, Any]) -> MediaDiveMongoRecipeItem:
        """Parse a recipe item from a solution or medium composition."""
        return MediaDiveMongoRecipeItem(
            compound=item.get("compound", ""),
            compound_id=item.get("compound_id"),
            amount=item.get("amount"),
            unit=item.get("unit"),
            g_l=item.get("g_l"),
            mmol_l=item.get("mmol_l"),
            optional=bool(item.get("optional", 0)),
            condition=item.get("condition"),
            solution=item.get("solution"),
            solution_id=item.get("solution_id"),
        )
