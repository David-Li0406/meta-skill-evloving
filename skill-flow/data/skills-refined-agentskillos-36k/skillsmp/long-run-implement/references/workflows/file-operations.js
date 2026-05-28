/**
 * Cross-platform file operations for long-run execution
 *
 * Usage from workflows:
 *   node -e "require('./file-operations').writeAtomic('path', 'content')"
 *   node -e "require('./file-operations').updateJson('path', d => d.agents.push({...}))"
 */

const fs = require('fs');
const path = require('path');

module.exports = {
  /**
   * Write content to file atomically (temp file + rename)
   * @param {string} target - Target file path
   * @param {string} content - Content to write
   */
  writeAtomic(target, content) {
    const temp = `${target}.tmp.${process.pid}`;
    try {
      fs.writeFileSync(temp, content, 'utf8');
      fs.renameSync(temp, target);
    } catch (err) {
      // Clean up temp file if rename failed
      if (fs.existsSync(temp)) {
        fs.unlinkSync(temp);
      }
      throw err;
    }
  },

  /**
   * Read and update JSON file atomically
   * @param {string} file - JSON file path
   * @param {Function} updater - Function that receives data object and modifies it
   */
  updateJson(file, updater) {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    updater(data);
    this.writeAtomic(file, JSON.stringify(data, null, 2));
  },

  /**
   * Read JSON file safely with corruption recovery
   * @param {string} file - JSON file path
   * @returns {Object} Parsed JSON data
   */
  readJsonSafe(file) {
    try {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (parseError) {
      // Check for incomplete temp file
      const tempPattern = `${file}.tmp.*`;
      const dir = path.dirname(file);
      const basename = path.basename(file);

      const tempFiles = fs.readdirSync(dir)
        .filter(f => f.startsWith(`${basename}.tmp.`))
        .map(f => path.join(dir, f));

      for (const tempFile of tempFiles) {
        try {
          const data = JSON.parse(fs.readFileSync(tempFile, 'utf8'));
          // Valid temp file found, recover
          fs.renameSync(tempFile, file);
          console.log(`Recovered ${file} from ${tempFile}`);
          return data;
        } catch {
          // Invalid temp file, clean up
          fs.unlinkSync(tempFile);
        }
      }

      throw new Error(`Cannot recover ${file}: ${parseError.message}`);
    }
  },

  /**
   * Remove directory recursively (cross-platform)
   * @param {string} dir - Directory path
   */
  removeDir(dir) {
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  },

  /**
   * Ensure directory exists (cross-platform)
   * @param {string} dir - Directory path
   */
  ensureDir(dir) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  },

  /**
   * Copy file (cross-platform)
   * @param {string} src - Source file path
   * @param {string} dest - Destination file path
   */
  copyFile(src, dest) {
    this.ensureDir(path.dirname(dest));
    fs.copyFileSync(src, dest);
  },

  /**
   * Read file as string
   * @param {string} file - File path
   * @returns {string} File content
   */
  readFile(file) {
    return fs.readFileSync(file, 'utf8');
  },

  /**
   * Check if file exists
   * @param {string} file - File path
   * @returns {boolean}
   */
  exists(file) {
    return fs.existsSync(file);
  },

  /**
   * List files in directory matching pattern
   * @param {string} dir - Directory path
   * @param {string} pattern - Glob pattern (simple: *.md, *-SUMMARY.md)
   * @returns {string[]} Array of matching file paths
   */
  listFiles(dir, pattern = '*') {
    if (!fs.existsSync(dir)) return [];

    const files = fs.readdirSync(dir);
    const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');

    return files
      .filter(f => regex.test(f))
      .map(f => path.join(dir, f));
  },

  /**
   * Parse markdown frontmatter
   * @param {string} content - Markdown content
   * @returns {Object} Parsed frontmatter
   */
  parseFrontmatter(content) {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return {};

    const frontmatter = {};
    match[1].split('\n').forEach(line => {
      const [key, ...valueParts] = line.split(':');
      if (key && valueParts.length) {
        let value = valueParts.join(':').trim();
        // Try to parse as JSON for arrays/objects
        try {
          value = JSON.parse(value);
        } catch {
          // Keep as string
        }
        frontmatter[key.trim()] = value;
      }
    });

    return frontmatter;
  }
};
