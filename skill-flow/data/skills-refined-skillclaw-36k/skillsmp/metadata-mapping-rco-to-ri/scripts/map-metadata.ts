/** biome-ignore-all lint/suspicious/noConsole: Fine for scripts */
import fs from "node:fs";
import path from "node:path";
import { parseLheoXml } from "../../../packages/rco/src/lheo";
import type { LheoDocument } from "../../../packages/rco/src/lheo-types";

/**
 * Script de mapping des métadonnées RCO vers Réfugiés.info
 * Usage: pnpm tsx .skills/metadata/scripts/map-metadata.ts <path_to_xml>
 */

// --- CONSTANTES DE MAPPING (Issues de base-connaissance.md) ---

const PUBLIC_STATUS_MAP: Record<string, string> = {
  "81021": "Tous les publics",
  "82060": "Tous les publics",
  "81043": "Tous les publics",
  "81019": "Tous les publics",
  "81023": "Personnes en situation d’exil",
  "81042": "Demandeurs d’asile",
  "81022": "Public immigré",
};

const FINANCEURS_PUBLICS = ["2", "3", "8", "9", "11", "12", "13", "15", "19"];

const FRENCH_LEVELS = ["alpha", "A1", "A2", "B1", "B2", "C1", "C2"];

// --- UTILS ---

/**
 * Extrait le texte d'un nœud Lhéo (gère le cas où c'est un objet avec _text ou une string directe)
 */
// biome-ignore lint/suspicious/noExplicitAny: Lhéo XML nodes can be varied strings or objects
function getText(node: any): string {
  if (!node) return "";
  if (typeof node === "string") return node;
  if (typeof node === "number") return String(node);
  if (node._text) return node._text;
  return "";
}

// --- LOGIQUE DE MAPPING ---

async function main() {
  const xmlPath = process.argv[2];
  if (!xmlPath) {
    console.error(
      "Usage: pnpm tsx .skills/metadata/scripts/map-metadata.ts <path_to_xml>",
    );
    process.exit(1);
  }

  try {
    const xmlContent = fs.readFileSync(path.resolve(xmlPath), "utf-8");
    const lheoDoc = await parseLheoXml(xmlContent);

    const mappingResult = mapLheoToRi(lheoDoc);

    console.log("---");
    console.log("metadata_ri:");
    console.log(JSON.stringify(mappingResult.metadata, null, 2));
    console.log("---");
    console.log("\n## Métadonnées mappées\n");
    console.log(mappingResult.table);
  } catch (error) {
    console.error("Erreur lors du mapping :", error);
    process.exit(1);
  }
}

function mapLheoToRi(doc: LheoDocument) {
  const formation = doc.lheo.offres.formation?.[0];
  if (!formation) {
    throw new Error("No formation found in LHEO document.");
  }
  const action = formation.action?.[0];
  if (!action) {
    throw new Error("No action found for the formation.");
  }
  const organisme = formation["organisme-formation-responsable"];
  const session = action.session?.[0];

  // 1. Titres et Sponsor
  const mainSponsor = getText(organisme["nom-organisme"]);
  const titreInformatif = getText(formation["intitule-formation"]);
  const titreMarque = getText(organisme["nom-organisme"]);

  // 2. Abstract (max 50 chars)
  const rawAbstract = getText(formation["contenu-formation"]) || "";
  const abstract =
    rawAbstract.length > 50
      ? `${rawAbstract.substring(0, 47)}...`
      : rawAbstract;

  // 3. Location
  const location =
    getText(
      action["lieu-de-formation"]?.[0]?.coordonnees?.adresse?.departement,
    ) || "";

  // 4. Price Logic
  const conventionnement = getText(action.conventionnement);
  const codeFinanceur = getText(
    action["organisme-financeur"]?.[0]?.["code-financeur"],
  );
  const isGratuit =
    conventionnement === "1" &&
    FINANCEURS_PUBLICS.includes(codeFinanceur || "");
  const price = {
    values: [isGratuit ? "gratuit" : "payant"],
    details: "",
  };

  // 5. Public Status
  const publicStatus = (action["code-public-vise"] || [])
    .map((cpv) => PUBLIC_STATUS_MAP[getText(cpv)])
    .filter(Boolean);

  // 6. French Level
  const frenchLevel = FRENCH_LEVELS.filter((level) =>
    rawAbstract.toLowerCase().includes(level.toLowerCase()),
  );

  // 7. Periode
  const periode = session
    ? {
        debut: { $date: formatDate(getText(session.periode.debut), "start") },
        fin: { $date: formatDate(getText(session.periode.fin), "end") },
      }
    : null;

  // 8. Map (Lieu de formation)
  const lieu = action["lieu-de-formation"]?.[0];
  const map = lieu?.coordonnees?.adresse
    ? {
        title: getText(lieu.coordonnees.adresse.denomination) || "",
        address: `${getText(lieu.coordonnees.adresse.ligne?.[0])}, ${getText(lieu.coordonnees.adresse.codepostal)} ${getText(lieu.coordonnees.adresse.ville)}`,
        city: getText(lieu.coordonnees.adresse.ville) || "",
        lat: parseFloat(
          getText(lieu.coordonnees.adresse.geolocalisation?.latitude) || "0",
        ),
        lng: parseFloat(
          getText(lieu.coordonnees.adresse.geolocalisation?.longitude) || "0",
        ),
      }
    : null;

  const metadata = {
    mainSponsor,
    titreInformatif,
    titreMarque,
    abstract,
    location,
    price,
    publicStatus,
    frenchLevel,
    periode,
    map,
  };

  // Génération du tableau de traçabilité
  let table = "| Métadonnée | Valeur(s) renseignée(s) | Source RCO |\n";
  table += "|---|---|---|\n";
  table += `| Titre marque | ${titreMarque} | nom-organisme : ${titreMarque} |\n`;
  table += `| Structure | ${mainSponsor} | organisme-formation-responsable/nom-organisme |\n`;
  table += `| Abstract | ${abstract} | contenu-formation (tronqué) |\n`;
  table += `| Prix | ${isGratuit ? "gratuit" : "payant"} | conventionnement : ${conventionnement} ; code-financeur : ${codeFinanceur} |\n`;
  table += `| Départements | ${location} | lieu-de-formation/departement |\n`;

  return { metadata, table };
}

function formatDate(rcoDate: string, type: "start" | "end") {
  if (!rcoDate || rcoDate.length !== 8) return "";
  const y = rcoDate.substring(0, 4);
  const m = rcoDate.substring(4, 6);
  const d = rcoDate.substring(6, 8);
  const time = type === "start" ? "00:00:00.000Z" : "23:59:59.999Z";
  return `${y}-${m}-${d}T${time}`;
}

main();
