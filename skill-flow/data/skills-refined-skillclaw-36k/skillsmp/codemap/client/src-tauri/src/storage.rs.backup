use crate::codemap::{CodeMap, CodeMapIndex, CodeMapMeta};
use anyhow::{Context, Result};
use std::fs;
use std::path::PathBuf;
use chrono::Utc;

pub struct Storage {
    codemap_dir: PathBuf,
}

impl Storage {
    pub fn new(project_root: &str) -> Result<Self> {
        let codemap_dir = PathBuf::from(project_root)
            .join("docs")
            .join(".codemap");
        
        // Create directory structure
        fs::create_dir_all(&codemap_dir)?;
        fs::create_dir_all(codemap_dir.join("codemaps"))?;
        fs::create_dir_all(codemap_dir.join("exports"))?;
        fs::create_dir_all(codemap_dir.join("cache"))?;
        
        // Initialize index if it doesn't exist
        let index_path = codemap_dir.join("index.json");
        if !index_path.exists() {
            let index = CodeMapIndex {
                version: 1,
                project_root: project_root.to_string(),
                codemaps: Vec::new(),
            };
            let json = serde_json::to_string_pretty(&index)?;
            fs::write(&index_path, json)?;
        }
        
        Ok(Storage { codemap_dir })
    }
    
    pub fn save_codemap(&self, codemap: &CodeMap) -> Result<String> {
        let filename = codemap.filename();
        let filepath = self.codemap_dir.join("codemaps").join(&filename);
        
        // Save CodeMap file
        let json = serde_json::to_string_pretty(codemap)?;
        fs::write(&filepath, json)?;
        
        // Update index
        let mut index = self.load_index()?;
        
        // Update or add to index
        if let Some(existing) = index.codemaps.iter_mut().find(|c| c.id == codemap.metadata.id) {
            existing.filename = filename.clone();
            existing.title = codemap.metadata.title.clone();
            existing.description = codemap.metadata.description.clone();
            existing.query = codemap.metadata.query.clone();
            existing.updated_at = Utc::now();
            existing.tags = codemap.metadata.tags.clone();
            existing.note = codemap.metadata.note.clone();
        } else {
            index.codemaps.push(CodeMapMeta {
                id: codemap.metadata.id.clone(),
                filename: filename.clone(),
                title: codemap.metadata.title.clone(),
                description: codemap.metadata.description.clone(),
                query: codemap.metadata.query.clone(),
                created_at: codemap.metadata.created_at,
                updated_at: Utc::now(),
                tags: codemap.metadata.tags.clone(),
                note: codemap.metadata.note.clone(),
            });
        }
        
        self.save_index(&index)?;
        
        Ok(codemap.metadata.id.clone())
    }
    
    pub fn load_codemap(&self, id: &str) -> Result<CodeMap> {
        let index = self.load_index()?;
        let meta = index.codemaps.iter()
            .find(|c| c.id == id)
            .context("CodeMap not found")?;
        
        let filepath = self.codemap_dir.join("codemaps").join(&meta.filename);
        let json = fs::read_to_string(&filepath)?;
        let codemap: CodeMap = serde_json::from_str(&json)?;
        
        Ok(codemap)
    }
    
    pub fn list_codemaps(&self) -> Result<Vec<CodeMapMeta>> {
        let index = self.load_index()?;
        Ok(index.codemaps)
    }
    
    pub fn delete_codemap(&self, id: &str) -> Result<()> {
        let mut index = self.load_index()?;
        let codemap_meta = index.codemaps.iter()
            .find(|c| c.id == id)
            .context("CodeMap not found")?;

        // Delete file
        let filepath = self.codemap_dir.join("codemaps").join(&codemap_meta.filename);
        if filepath.exists() {
            fs::remove_file(filepath)?;
        }

        // Remove from index
        index.codemaps.retain(|c| c.id != id);
        self.save_index(&index)?;

        Ok(())
    }

    pub fn update_codemap_meta(
        &self,
        id: &str,
        title: Option<String>,
        note: Option<String>,
        tags: Option<Vec<String>>,
    ) -> Result<CodeMapMeta> {
        let mut index = self.load_index()?;

        let meta = index.codemaps.iter_mut()
            .find(|c| c.id == id)
            .context("CodeMap not found")?;

        // Update fields if provided
        if let Some(new_title) = title {
            meta.title = new_title;
        }
        if let Some(new_note) = note {
            meta.note = Some(new_note);
        }
        if let Some(new_tags) = tags {
            meta.tags = new_tags;
        }
        meta.updated_at = Utc::now();

        let updated_meta = meta.clone();
        self.save_index(&index)?;

        Ok(updated_meta)
    }
    
    pub fn export_codemap(&self, id: &str, format: &str) -> Result<String> {
        let codemap = self.load_codemap(id)?;
        let exports_dir = self.codemap_dir.join("exports");
        fs::create_dir_all(&exports_dir)?;
        
        let filename_base = codemap.metadata.id.clone();
        let export_path = match format {
            "json" => {
                let filepath = exports_dir.join(format!("{}.json", filename_base));
                let json = serde_json::to_string_pretty(&codemap)?;
                fs::write(&filepath, json)?;
                filepath.to_string_lossy().to_string()
            }
            "markdown" => {
                let filepath = exports_dir.join(format!("{}.md", filename_base));
                let markdown = self.codemap_to_markdown(&codemap);
                fs::write(&filepath, markdown)?;
                filepath.to_string_lossy().to_string()
            }
            "html" => {
                let filepath = exports_dir.join(format!("{}.html", filename_base));
                let html = self.codemap_to_html(&codemap);
                fs::write(&filepath, html)?;
                filepath.to_string_lossy().to_string()
            }
            _ => anyhow::bail!("Unsupported export format: {}", format),
        };
        
        Ok(export_path)
    }
    
    pub fn import_codemap(&self, file_path: &str) -> Result<CodeMap> {
        let json = fs::read_to_string(file_path)?;
        let mut codemap: CodeMap = serde_json::from_str(&json)?;
        
        // Generate new ID to avoid conflicts
        let now = Utc::now();
        let new_id = format!("{}-import", now.format("%Y%m%d"));
        codemap.metadata.id = new_id.clone();
        codemap.metadata.updated_at = now;
        
        self.save_codemap(&codemap)?;
        
        Ok(codemap)
    }
    
    fn load_index(&self) -> Result<CodeMapIndex> {
        let index_path = self.codemap_dir.join("index.json");
        
        // If file doesn't exist, return empty index
        if !index_path.exists() {
            return Ok(CodeMapIndex {
                version: 1,
                project_root: self.codemap_dir.parent()
                    .and_then(|p| p.parent())
                    .and_then(|p| p.to_str())
                    .unwrap_or("")
                    .to_string(),
                codemaps: Vec::new(),
            });
        }
        
        let json = fs::read_to_string(&index_path)?;
        
        // If file is empty, return empty index
        if json.trim().is_empty() {
            return Ok(CodeMapIndex {
                version: 1,
                project_root: self.codemap_dir.parent()
                    .and_then(|p| p.parent())
                    .and_then(|p| p.to_str())
                    .unwrap_or("")
                    .to_string(),
                codemaps: Vec::new(),
            });
        }
        
        let index: CodeMapIndex = serde_json::from_str(&json)
            .map_err(|e| anyhow::anyhow!("Failed to parse index.json: {}", e))?;
        Ok(index)
    }
    
    fn save_index(&self, index: &CodeMapIndex) -> Result<()> {
        let index_path = self.codemap_dir.join("index.json");
        let json = serde_json::to_string_pretty(index)?;
        fs::write(&index_path, json)?;
        Ok(())
    }
    
    fn codemap_to_markdown(&self, codemap: &CodeMap) -> String {
        let mut md = String::new();
        
        md.push_str(&format!("# {}\n\n", codemap.title));
        md.push_str(&format!("**描述**: {}\n\n", codemap.description));
        md.push_str(&format!("**查询**: {}\n\n", codemap.metadata.query));
        md.push_str(&format!("**创建时间**: {}\n\n", codemap.metadata.created_at.format("%Y-%m-%d %H:%M:%S")));
        
        if !codemap.metadata.tags.is_empty() {
            md.push_str("**标签**: ");
            md.push_str(&codemap.metadata.tags.join(", "));
            md.push_str("\n\n");
        }
        
        if let Some(note) = &codemap.metadata.note {
            md.push_str(&format!("**备注**: {}\n\n", note));
        }
        
        md.push_str("## Mermaid 流程图\n\n");
        md.push_str("```mermaid\n");
        md.push_str(&codemap.mermaid_diagram);
        md.push_str("\n```\n\n");
        
        for trace in &codemap.traces {
            md.push_str(&format!("## {} - {}\n\n", trace.id, trace.title));
            md.push_str(&format!("{}\n\n", trace.description));
            
            md.push_str("### 关键代码节点\n\n");
            for loc in &trace.locations {
                md.push_str(&format!("- **{}**: `{}:{}\n", loc.title, loc.path, loc.line_number));
                md.push_str(&format!("  ```\n  {}\n  ```\n", loc.line_content));
                md.push_str(&format!("  {}\n\n", loc.description));
            }
            
            md.push_str("### 调用链路\n\n");
            md.push_str("```\n");
            md.push_str(&trace.trace_text_diagram);
            md.push_str("\n```\n\n");
            
            md.push_str("### 详细说明\n\n");
            md.push_str(&trace.trace_guide);
            md.push_str("\n\n");
        }
        
        md
    }
    
    fn codemap_to_html(&self, codemap: &CodeMap) -> String {
        let mut html = String::new();
        
        html.push_str("<!DOCTYPE html>\n");
        html.push_str("<html lang=\"zh-CN\">\n");
        html.push_str("<head>\n");
        html.push_str("  <meta charset=\"UTF-8\">\n");
        html.push_str("  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n");
        html.push_str(&format!("  <title>{}</title>\n", codemap.title));
        html.push_str("  <script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>\n");
        html.push_str("  <style>\n");
        html.push_str("    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }\n");
        html.push_str("    .header { border-bottom: 2px solid #e0e0e0; padding-bottom: 20px; margin-bottom: 30px; }\n");
        html.push_str("    .metadata { background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px; }\n");
        html.push_str("    .trace { margin-top: 40px; }\n");
        html.push_str("    .location { background: #fff9c4; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }\n");
        html.push_str("    .diagram { background: #f0f0f0; padding: 20px; border-radius: 8px; overflow-x: auto; }\n");
        html.push_str("    .tree { font-family: 'Courier New', monospace; background: #f5f5f5; padding: 15px; border-radius: 8px; }\n");
        html.push_str("  </style>\n");
        html.push_str("</head>\n");
        html.push_str("<body>\n");
        
        html.push_str(&format!("  <div class=\"header\"><h1>{}</h1></div>\n", codemap.title));
        
        html.push_str("  <div class=\"metadata\">\n");
        html.push_str(&format!("    <p><strong>描述:</strong> {}</p>\n", codemap.description));
        html.push_str(&format!("    <p><strong>查询:</strong> {}</p>\n", codemap.metadata.query));
        html.push_str(&format!("    <p><strong>创建时间:</strong> {}</p>\n", codemap.metadata.created_at.format("%Y-%m-%d %H:%M:%S")));
        
        if !codemap.metadata.tags.is_empty() {
            html.push_str("    <p><strong>标签:</strong> ");
            html.push_str(&codemap.metadata.tags.join(", "));
            html.push_str("</p>\n");
        }
        
        if let Some(note) = &codemap.metadata.note {
            html.push_str(&format!("    <p><strong>备注:</strong> {}</p>\n", note));
        }
        
        html.push_str("  </div>\n");
        
        html.push_str("  <h2>Mermaid 流程图</h2>\n");
        html.push_str("  <div class=\"diagram\">\n");
        html.push_str("    <pre class=\"mermaid\">\n");
        html.push_str(&codemap.mermaid_diagram);
        html.push_str("    </pre>\n");
        html.push_str("  </div>\n");
        
        for trace in &codemap.traces {
            html.push_str(&format!("  <div class=\"trace\">\n"));
            html.push_str(&format!("    <h2>{} - {}</h2>\n", trace.id, trace.title));
            html.push_str(&format!("    <p>{}</p>\n", trace.description));
            
            html.push_str("    <h3>关键代码节点</h3>\n");
            for loc in &trace.locations {
                html.push_str("    <div class=\"location\">\n");
                html.push_str(&format!("      <strong>{}</strong>: {}:{}\n", loc.title, loc.path, loc.line_number));
                html.push_str(&format!("      <pre><code>{}</code></pre>\n", loc.line_content));
                html.push_str(&format!("      <p>{}</p>\n", loc.description));
                html.push_str("    </div>\n");
            }
            
            html.push_str("    <h3>调用链路</h3>\n");
            html.push_str("    <div class=\"tree\">\n");
            html.push_str("    <pre>\n");
            html.push_str(&trace.trace_text_diagram);
            html.push_str("    </pre>\n");
            html.push_str("    </div>\n");
            
            html.push_str("    <h3>详细说明</h3>\n");
            html.push_str(&format!("    <div>{}</div>\n", trace.trace_guide));
            
            html.push_str("  </div>\n");
        }
        
        html.push_str("  <script>\n");
        html.push_str("    mermaid.initialize({ startOnLoad: true });\n");
        html.push_str("  </script>\n");
        html.push_str("</body>\n");
        html.push_str("</html>\n");
        
        html
    }
}