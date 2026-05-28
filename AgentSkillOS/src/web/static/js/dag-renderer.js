/**
 * DAG Renderer - SVG-based DAG visualization for Skill Orchestrator
 */

/**
 * Truncate text with ellipsis if it exceeds maxLength
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} Truncated text with '..' if needed
 */
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength - 2) + '..';
}

/**
 * Compute DAG layout using topological sort
 * @param {Array} nodes - Array of node objects with id, depends_on
 * @param {Object} options - Layout options
 * @returns {Object} Layout data with positions and edges
 */
function computeDagLayout(nodes, options = {}) {
    const {
        nodeWidth = 140,
        nodeHeight = 42,
        hGap = 40,
        vGap = 50,
        startX = 10,
        startY = 10
    } = options;

    if (!nodes || nodes.length === 0) {
        return { layout: [], edges: [], viewBox: '0 0 400 200', uniqueSkills: [] };
    }

    // Build node map
    const nodeMap = {};
    nodes.forEach(n => { nodeMap[n.id] = n; });

    // Compute node levels (topological sort)
    const levels = {};
    const computeLevel = (nodeId, visited = new Set()) => {
        if (visited.has(nodeId)) return 0;
        if (levels[nodeId] !== undefined) return levels[nodeId];
        visited.add(nodeId);
        const node = nodeMap[nodeId];
        const deps = node?.depends_on || [];
        if (deps.length === 0) {
            levels[nodeId] = 0;
        } else {
            levels[nodeId] = Math.max(...deps.map(d => computeLevel(d, visited) + 1));
        }
        return levels[nodeId];
    };
    nodes.forEach(n => computeLevel(n.id));

    // Group by level
    const byLevel = {};
    nodes.forEach(n => {
        const level = levels[n.id] || 0;
        if (!byLevel[level]) byLevel[level] = [];
        byLevel[level].push(n);
    });

    // Compute positions
    const layout = [];
    const positions = {};
    let maxX = 0;

    Object.keys(byLevel).sort((a, b) => Number(a) - Number(b)).forEach(levelStr => {
        const level = Number(levelStr);
        const items = byLevel[levelStr];
        items.forEach((node, i) => {
            const x = startX + i * (nodeWidth + hGap);
            const y = startY + level * (nodeHeight + vGap);
            positions[node.id] = { x: x + nodeWidth / 2, y: y + nodeHeight / 2 };
            layout.push({ ...node, x, y });
            maxX = Math.max(maxX, x + nodeWidth);
        });
    });

    // Compute edges
    const edges = [];
    nodes.forEach(n => {
        (n.depends_on || []).forEach(depId => {
            if (positions[depId] && positions[n.id]) {
                const from = positions[depId];
                const to = positions[n.id];
                edges.push({
                    from: depId,
                    to: n.id,
                    path: `M ${from.x} ${from.y + nodeHeight / 2} L ${to.x} ${to.y - nodeHeight / 2 - 5}`
                });
            }
        });
    });

    // Extract unique skills
    const skillSet = new Map();
    nodes.forEach((n) => {
        if (n.name && !skillSet.has(n.name)) {
            skillSet.set(n.name, window.getSkillColor ? window.getSkillColor(skillSet.size) : SKILL_COLORS[skillSet.size % SKILL_COLORS.length]);
        }
    });
    const uniqueSkills = Array.from(skillSet.entries()).map(([name, color]) => ({ name, color }));

    // Compute viewBox
    const maxLevel = Math.max(...Object.keys(byLevel).map(Number));
    const height = (maxLevel + 1) * (nodeHeight + vGap) + startY + 10;
    const viewBox = `0 0 ${Math.max(maxX + 20, 400)} ${Math.max(height, 180)}`;

    return { layout, edges, viewBox, positions, uniqueSkills };
}

/**
 * Render DAG as SVG string
 * @param {Object} dagData - Data from computeDagLayout
 * @param {Object} options - Render options
 * @returns {string} SVG HTML string
 */
function renderDagSvg(dagData, options = {}) {
    const {
        nodeWidth = 140,
        nodeHeight = 42,
        showStatus = true
    } = options;

    const { layout, edges, viewBox } = dagData;

    if (!layout || layout.length === 0) {
        return '';
    }

    let svg = `<svg viewBox="${viewBox}" class="w-full" style="min-height:180px">
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#4b5563"/>
            </marker>
        </defs>`;

    // Render edges
    edges.forEach(edge => {
        svg += `<path d="${edge.path}" class="dag-edge" marker-end="url(#arrow)"/>`;
    });

    // Render nodes
    layout.forEach(node => {
        const statusClass = 'dag-node-' + (node.status || 'pending');
        const icon = window.getStatusIcon ? window.getStatusIcon(node.status) : '';
        // Calculate max characters based on node width and font size (each char ~7px)
        const maxChars = Math.floor((nodeWidth - 12) / 7);
        const displayName = truncateText(node.name, maxChars);
        const needsTooltip = node.name && node.name.length > maxChars;
        svg += `<g transform="translate(${node.x},${node.y})" class="dag-node">
            <rect width="${nodeWidth}" height="${nodeHeight}" rx="6" stroke-width="2" class="${statusClass}"/>
            <text x="${nodeWidth / 2}" y="18" text-anchor="middle" class="dag-node-text" style="font-size:11px">${displayName}</text>
            <text x="${nodeWidth / 2}" y="32" text-anchor="middle" class="dag-node-text" style="font-size:9px">${showStatus ? icon : ''}</text>
            ${needsTooltip ? `<title>${node.name}</title>` : ''}
        </g>`;
    });

    svg += '</svg>';
    return svg;
}

/**
 * Render mini DAG preview for plan selection
 * @param {Object} plan - Plan object with nodes array
 * @param {Object} options - Render options
 * @returns {string} SVG HTML string
 */
function renderPlanPreview(plan, options = {}) {
    const {
        nodeWidth = 100,
        nodeHeight = 32,
        hGap = 25,
        vGap = 25
    } = options;

    try {
        const nodes = plan?.nodes || [];
        if (nodes.length === 0) {
            return '<div class="text-gray-500 text-xs p-2">No nodes</div>';
        }

        // Compute layout using shared function
        const dagData = computeDagLayout(nodes, { nodeWidth, nodeHeight, hGap, vGap, startX: 5, startY: 5 });
        const { layout, edges, positions } = dagData;

        if (layout.length === 0) {
            return '<div class="text-gray-500 text-xs p-2">Empty plan</div>';
        }

        // Compute viewBox
        const maxX = Math.max(...layout.map(n => n.x + nodeWidth)) + 10;
        const levels = {};
        const nodeMap = {};
        nodes.forEach(n => { nodeMap[n.id] = n; });

        const computeLevel = (nodeId, visited = new Set()) => {
            if (visited.has(nodeId)) return 0;
            if (levels[nodeId] !== undefined) return levels[nodeId];
            visited.add(nodeId);
            const node = nodeMap[nodeId];
            const deps = node?.depends_on || [];
            if (deps.length === 0) {
                levels[nodeId] = 0;
            } else {
                levels[nodeId] = Math.max(...deps.filter(d => nodeMap[d]).map(d => computeLevel(d, visited) + 1));
            }
            return levels[nodeId];
        };
        nodes.forEach(n => computeLevel(n.id));

        const maxLevel = Math.max(...Object.values(levels));
        const maxY = (maxLevel + 1) * (nodeHeight + vGap) + 10;
        const viewBox = `0 0 ${maxX} ${maxY}`;

        let svg = `<svg viewBox="${viewBox}" class="w-full" style="height:100px">
            <defs>
                <marker id="arrow-mini" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#4b5563"/>
                </marker>
            </defs>`;

        // Render edges
        edges.forEach(edge => {
            svg += `<path d="${edge.path}" class="dag-edge" marker-end="url(#arrow-mini)"/>`;
        });

        // Render nodes
        layout.forEach(node => {
            // Calculate max characters based on node width (each char ~6px for smaller font)
            const maxChars = Math.floor((nodeWidth - 10) / 6);
            const displayName = truncateText(node.name, maxChars);
            const needsTooltip = node.name && node.name.length > maxChars;
            svg += `<g transform="translate(${node.x},${node.y})">
                <rect width="${nodeWidth}" height="${nodeHeight}" rx="4" class="dag-node-pending" stroke-width="1"/>
                <text x="${nodeWidth / 2}" y="20" text-anchor="middle" class="dag-node-text" style="font-size:9px">${displayName}</text>
                ${needsTooltip ? `<title>${node.name}</title>` : ''}
            </g>`;
        });

        svg += '</svg>';
        return svg;
    } catch (e) {
        console.error('renderPlanPreview error:', e);
        return '<div class="text-red-500 text-xs p-2">Render error</div>';
    }
}

/**
 * Update node status in existing layout
 * @param {Array} layout - Layout array from computeDagLayout
 * @param {string} nodeId - Node ID to update
 * @param {string} status - New status
 * @param {string} time - Optional time string
 */
function updateNodeInLayout(layout, nodeId, status, time) {
    const node = layout.find(n => n.id === nodeId);
    if (node) {
        node.status = status;
        if (time) node.time = time;
    }
}

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.truncateText = truncateText;
    window.computeDagLayout = computeDagLayout;
    window.renderDagSvg = renderDagSvg;
    window.renderPlanPreview = renderPlanPreview;
    window.updateNodeInLayout = updateNodeInLayout;
}
