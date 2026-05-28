import fs from 'fs';
import path from 'path';

// I'll stick to string template for MVP to avoid extra deps if possible,
// but js-yaml is standard. I'll add it to package.json later or just write text.
// Text is fine for MVP.

export class RalphyIntegration {
  static init(rootPath: string) {
    const ralphyDir = path.join(rootPath, '.ralphy');
    if (!fs.existsSync(ralphyDir)) {
      fs.mkdirSync(ralphyDir, { recursive: true });
    }

    const configPath = path.join(ralphyDir, 'config.yaml');

    const config = `project:
  name: "My Project"
  language: "typescript"
  framework: "node"

commands:
  test: "npm test"
  lint: "npm run lint"
  build: "npm run build"

rules:
  - "Always run 'atlas pack' before starting a task"
  - "Check for duplicates using 'atlas find-duplicates' before creating new files"

boundaries:
  never_touch:
    - "node_modules"
    - "dist"
    - "coverage"
    - ".atlas"
`;

    if (!fs.existsSync(configPath)) {
      fs.writeFileSync(configPath, config);
      console.log('Created .ralphy/config.yaml');
    } else {
      console.log('.ralphy/config.yaml already exists. Skipping.');
    }
  }
}
