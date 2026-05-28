// Extract BacDive strain-medium edges to TSV with literature references
// Run with: mongosh bacdive scripts/extract_bacdive_strain_medium_edges.js

// Header
print([
  "bacdive_id",
  "dsm_number",
  "ncbi_taxid_species",
  "ncbi_taxid_strain",
  "species",
  "strain_designation",
  "type_strain",
  "medium_ref",
  "medium_id",
  "medium_name",
  "medium_link",
  "growth",
  "composition",
  "ref_authors",
  "ref_title",
  "ref_doi_or_url"
].join("\t"));

// Helper to extract medium ID from link
function extractMediumId(link) {
  if (!link) return "";
  const match = link.match(/\/medium\/(\d+[a-z]?)$/);
  return match ? match[1] : "";
}

// Helper to get NCBI tax id at a level
function getNcbiTaxId(taxIds, level) {
  if (!taxIds || !Array.isArray(taxIds)) return "";
  const match = taxIds.find(t => t["Matching level"] === level);
  return match ? match["NCBI tax id"] : "";
}

// Helper to escape TSV field
function escapeField(val) {
  if (val === null || val === undefined) return "";
  let s = String(val);
  // Replace tabs and newlines
  s = s.replace(/\t/g, " ").replace(/\n/g, "\\n").replace(/\r/g, "");
  return s;
}

// Helper to find reference by @id
function findReference(references, refId) {
  if (!references || !Array.isArray(references) || !refId) return null;
  return references.find(r => r["@id"] === refId);
}

// Helper to check if reference is a generic placeholder (not a real literature citation)
function isPlaceholderReference(ref) {
  if (!ref) return true;
  const authors = ref.authors || "";
  // Filter out generic curator/catalog entries
  if (authors.startsWith("Curators of the ")) return true;
  if (authors.includes("Automatically annotated")) return true;
  // Catalogue field without title suggests it's just a catalog entry
  if (ref.catalogue && !ref.title) return true;
  return false;
}

// Process all strains with culture medium
db.strains.find({ "Culture and growth conditions.culture medium": { $exists: true } }).forEach(doc => {
  const gen = doc.General || {};
  const tax = doc["Name and taxonomic classification"] || {};
  const references = doc.Reference || [];

  const bacdiveId = gen["BacDive-ID"] || "";
  const dsmNumber = gen["DSM-Number"] || "";
  const ncbiTaxIds = gen["NCBI tax id"];
  const ncbiSpecies = getNcbiTaxId(ncbiTaxIds, "species");
  const ncbiStrain = getNcbiTaxId(ncbiTaxIds, "strain");
  const species = tax.species || "";
  const strainDesign = tax["strain designation"] || "";
  const typeStrain = tax["type strain"] || "";

  let media = doc["Culture and growth conditions"]["culture medium"];
  if (!Array.isArray(media)) {
    media = [media];
  }

  media.forEach(m => {
    if (!m) return;

    // Look up reference by @ref
    const refId = m["@ref"];
    const ref = findReference(references, refId);

    // Only include real literature references, not placeholders
    let refAuthors = "";
    let refTitle = "";
    let refDoiUrl = "";

    if (ref && !isPlaceholderReference(ref)) {
      refAuthors = ref.authors || "";
      refTitle = ref.title || "";
      refDoiUrl = ref["doi/url"] || "";
    }

    const row = [
      bacdiveId,
      dsmNumber,
      ncbiSpecies,
      ncbiStrain,
      escapeField(species),
      escapeField(strainDesign),
      typeStrain,
      refId || "",
      extractMediumId(m.link),
      escapeField(m.name || ""),
      m.link || "",
      m.growth || "",
      escapeField(m.composition || ""),
      escapeField(refAuthors),
      escapeField(refTitle),
      escapeField(refDoiUrl)
    ];
    print(row.join("\t"));
  });
});
