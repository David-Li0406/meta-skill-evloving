use crate::codemap_v2::{CodeMap, Node, Edge, CodeRef, TraceGuide, EdgeType, ModelTier};
use anyhow::{Context, Result};
use std::fs;
use std::path::Path;

pub struct Analyzer {
    project_root: String,
}

impl Analyzer {
    pub fn new(project_root: String) -> Self {
        Analyzer { project_root }
    }

    pub fn analyze(&self, files: Vec<String>, query: String, model_tier: ModelTier) -> Result<CodeMap> {
        let repo_name = Path::new(&self.project_root)
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("unknown");

        let mut codemap = CodeMap::new(
            query.clone(),
            self.project_root.clone(),
            repo_name.to_string(),
            model_tier,
        );

        // Read and parse all files
        let mut nodes: Vec<Node> = Vec::new();
        let mut edges: Vec<Edge> = Vec::new();
        let mut node_counter = 0;

        for (file_idx, file_path) in files.iter().enumerate() {
            let content = fs::read_to_string(file_path)
                .with_context(|| format!("Failed to read file: {}", file_path))?;

            // Analyze file and create nodes
            let (mut file_nodes, file_edges) = self.analyze_file(file_path, &content, file_idx, &mut node_counter)?;
            nodes.append(&mut file_nodes);
            edges.extend(file_edges);
        }

        // Update CodeMap
        codemap.nodes = nodes;
        codemap.edges = edges;

        Ok(codemap)
    }

    fn analyze_file(
        &self,
        file_path: &str,
        content: &str,
        file_idx: usize,
        node_counter: &mut usize,
    ) -> Result<(Vec<Node>, Vec<Edge>)> {
        let mut nodes = Vec::new();
        let mut edges = Vec::new();
        let lines: Vec<&str> = content.lines().collect();

        let file_relative = file_path
            .strip_prefix(&self.project_root)
            .unwrap_or(file_path)
            .trim_start_matches('/');

        let file_name = Path::new(file_path)
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("Unknown");

        let parent_node_id = format!("file_{}", file_idx);
        let mut child_ids: Vec<String> = Vec::new();

        // Create parent file node
        let parent_node = Node {
            node_id: parent_node_id.clone(),
            title: file_name.to_string(),
            summary: format!("文件: {}", file_name),
            children: Vec::new(),
            code_refs: vec![CodeRef {
                path: file_relative.to_string(),
                start_line: 1,
                end_line: lines.len(),
                symbol: None,
            }],
            trace_guide: TraceGuide {
                short: format!("分析文件 {}", file_name),
                long: format!(
                    "## 文件概述\n\n文件 `{}` 包含 {} 行代码。\n\n## 代码节点\n\n以下是在此文件中识别的关键代码块。",
                    file_path, lines.len()
                ),
            },
        };
        nodes.push(parent_node);

        // Analyze lines for code nodes
        let mut code_blocks: Vec<(usize, usize, String, String)> = Vec::new();

        for (line_num, line) in lines.iter().enumerate() {
            let line_number = line_num + 1;
            let trimmed = line.trim();

            if trimmed.is_empty() || trimmed.starts_with("//") || trimmed.starts_with("#") {
                continue;
            }

            let (node_type, description) = if self.is_controller_endpoint(trimmed) {
                ("Controller 入口", "处理 HTTP 请求的入口点")
            } else if self.is_service_method(trimmed) {
                ("Service 业务逻辑", "核心业务处理逻辑")
            } else if self.is_mapper_operation(trimmed) {
                ("数据库操作", "数据持久化操作")
            } else if self.is_branching_logic(trimmed) {
                ("分支判断", "条件分支逻辑")
            } else if self.is_exception_handling(trimmed) {
                ("异常处理", "捕获和处理异常")
            } else {
                continue;
            };

            code_blocks.push((line_number, line_number, node_type.to_string(), description.to_string()));
        }

        // Group consecutive code blocks
        let mut grouped_blocks: Vec<(usize, usize, String, String)> = Vec::new();
        for block in code_blocks {
            if let Some(last) = grouped_blocks.last_mut() {
                if block.0 == last.1 + 1 && block.2 == last.2 {
                    last.1 = block.1;
                } else {
                    grouped_blocks.push(block);
                }
            } else {
                grouped_blocks.push(block);
            }
        }

        // Create nodes for grouped blocks
        for (start, end, node_type, description) in grouped_blocks {
            *node_counter += 1;
            let node_id = format!("node_{}", node_counter);
            child_ids.push(node_id.clone());

            let code_content: String = lines[(start - 1)..end]
                .iter()
                .take(5)
                .map(|s| s.trim())
                .filter(|s| !s.is_empty())
                .collect::<Vec<_>>()
                .join("; ");

            let node = Node {
                node_id: node_id.clone(),
                title: format!("{}:{} - {}", file_name, start, node_type),
                summary: description.to_string(),
                children: Vec::new(),
                code_refs: vec![CodeRef {
                    path: file_relative.to_string(),
                    start_line: start,
                    end_line: end,
                    symbol: None,
                }],
                trace_guide: TraceGuide {
                    short: format!("{} ({})", description, start),
                    long: format!(
                        "## 代码块\n\n**位置**: `{}`:{}\n\n**类型**: {}\n\n**描述**: {}\n\n**代码**: ```\n{}\n```",
                        file_relative, start, node_type, description, code_content
                    ),
                },
            };

            nodes.push(node);

            // Create edge from parent to child
            edges.push(Edge {
                from: parent_node_id.clone(),
                to: node_id,
                edge_type: EdgeType::Calls,
            });
        }

        // Update parent node with children
        if let Some(parent) = nodes.first_mut() {
            parent.children = child_ids;
        }

        Ok((nodes, edges))
    }

    fn is_controller_endpoint(&self, line: &str) -> bool {
        line.contains("@RequestMapping")
            || line.contains("@GetMapping")
            || line.contains("@PostMapping")
            || line.contains("@PutMapping")
            || line.contains("@DeleteMapping")
            || (line.contains("def ") && (line.contains("request") || line.contains("route")))
            || (line.contains("app.") && (line.contains("get") || line.contains("post")))
    }

    fn is_service_method(&self, line: &str) -> bool {
        (line.contains("def ") && !line.contains("__"))
            || (line.contains("public ") && (line.contains("void") || line.contains("return")))
            || line.contains("async def ")
            || (line.contains("fn ") && line.contains("pub"))
    }

    fn is_mapper_operation(&self, line: &str) -> bool {
        line.contains("SELECT")
            || line.contains("INSERT")
            || line.contains("UPDATE")
            || line.contains("DELETE")
            || line.contains(".find(")
            || line.contains(".create(")
            || line.contains(".update(")
            || line.contains(".delete(")
            || line.contains("execute_query")
            || line.contains("db.query")
    }

    fn is_branching_logic(&self, line: &str) -> bool {
        line.starts_with("if ")
            || line.starts_with("elif ")
            || line.starts_with("else:")
            || line.contains("switch ")
            || line.contains("case ")
            || (line.contains("?") && line.contains(":"))
    }

    fn is_exception_handling(&self, line: &str) -> bool {
        line.contains("try") || line.contains("catch") || line.contains("except")
    }
}
