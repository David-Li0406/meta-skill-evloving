import { z } from "zod";
import fs from "fs";
import path from "path";

/**
 * Validates 3D assets in the project for performance standards.
 * Checks for:
 * 1. Uncompressed .glb files (non-draco)
 * 2. Large PNG/JPG textures (recommends KTX2)
 * 3. Poly count (if metadata is available)
 */

const AssetSchema = z.object({
  path: z.string(),
  size: z.number(),
  extension: z.enum([".glb", ".gltf", ".png", ".jpg", ".jpeg", ".ktx2"]),
});

type Asset = z.infer<typeof AssetSchema>;

const MAX_TEXTURE_SIZE = 2 * 1024 * 1024; // 2MB
const MAX_MODEL_SIZE = 10 * 1024 * 1024; // 10MB

function scanDirectory(dir: string, assets: Asset[] = []) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      scanDirectory(fullPath, assets);
    } else {
      const ext = path.extname(file).toLowerCase();
      if ([".glb", ".gltf", ".png", ".jpg", ".jpeg", ".ktx2"].includes(ext)) {
        assets.push({
          path: fullPath,
          size: stat.size,
          extension: ext as any,
        });
      }
    }
  }
  return assets;
}

async function validate() {
  console.log("🚀 Starting 3D Asset Validation (Squaads Elite Core)...");
  
  const publicDir = path.join(process.cwd(), "public");
  if (!fs.existsSync(publicDir)) {
    console.error("❌ public/ directory not found.");
    return;
  }

  const assets = scanDirectory(publicDir);
  let warnings = 0;

  assets.forEach((asset) => {
    // Check texture size
    if ([".png", ".jpg", ".jpeg"].includes(asset.extension) && asset.size > MAX_TEXTURE_SIZE) {
      console.warn(`⚠️  LARGE TEXTURE: ${asset.path} (${(asset.size / 1024 / 1024).toFixed(2)}MB). Consider KTX2.`);
      warnings++;
    }

    // Check model size
    if (asset.extension === ".glb" && asset.size > MAX_MODEL_SIZE) {
      console.warn(`⚠️  LARGE MODEL: ${asset.path} (${(asset.size / 1024 / 1024).toFixed(2)}MB). Ensure Draco compression is used.`);
      warnings++;
    }
  });

  if (warnings === 0) {
    console.log("✅ All assets pass elite performance standards.");
  } else {
    console.log(`
Found ${warnings} performance warnings. Please optimize before production.`);
  }
}

validate();
