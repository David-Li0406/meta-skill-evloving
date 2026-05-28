<?php
/**
 * TheHUB Roadmap - Interactive Project Overview
 * Clickable projects with progress tracking
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
requireLogin();

// Read ROADMAP.md
$roadmapPath = __DIR__ . '/../ROADMAP.md';
$roadmapContent = file_exists($roadmapPath) ? file_get_contents($roadmapPath) : '';

// Parse project areas from table (with progress column)
$projectAreas = [];
if (preg_match('/\| Omrade \| Status \| Beskrivning \| Progress \|[\s\S]*?\n((?:\|[^\n]+\n)+)/', $roadmapContent, $matches)) {
    $rows = explode("\n", trim($matches[1]));
    foreach ($rows as $row) {
        if (preg_match('/\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|/', $row, $cols)) {
            $progress = trim($cols[4]);
            $progressNum = (int) preg_replace('/[^0-9]/', '', $progress);
            $projectAreas[] = [
                'id' => strtolower(preg_replace('/[^a-z0-9]+/i', '-', trim($cols[1]))),
                'name' => trim($cols[1]),
                'status' => trim($cols[2]),
                'description' => trim($cols[3]),
                'progress' => $progressNum
            ];
        }
    }
}

// Parse project details (sections starting with ## ProjectName)
$projectDetails = [];

// Parse ongoing projects (PAGAENDE PROJEKT)
if (preg_match('/# PAGAENDE PROJEKT([\s\S]*?)(?=\n# AVSLUTADE|\Z)/', $roadmapContent, $ongoingMatch)) {
    $ongoingContent = $ongoingMatch[1];
    if (preg_match_all('/## ([^\n]+)\n([\s\S]*?)(?=\n## |\n---|\Z)/', $ongoingContent, $projectMatches, PREG_SET_ORDER)) {
        foreach ($projectMatches as $match) {
            $projectId = strtolower(preg_replace('/[^a-z0-9]+/i', '-', trim($match[1])));
            $projectDetails[$projectId] = [
                'name' => trim($match[1]),
                'content' => trim($match[2]),
                'type' => 'ongoing'
            ];
        }
    }
}

// Parse completed projects (AVSLUTADE PROJEKT)
if (preg_match('/# AVSLUTADE PROJEKT([\s\S]*?)(?=\n# TEKNISKA|\Z)/', $roadmapContent, $completedMatch)) {
    $completedContent = $completedMatch[1];
    if (preg_match_all('/## DEL \d+: ([^\n]+)\n([\s\S]*?)(?=\n## DEL |\n---|\Z)/', $completedContent, $projectMatches, PREG_SET_ORDER)) {
        foreach ($projectMatches as $match) {
            $projectId = strtolower(preg_replace('/[^a-z0-9]+/i', '-', trim($match[1])));
            $projectDetails[$projectId] = [
                'name' => trim($match[1]),
                'content' => trim($match[2]),
                'type' => 'completed'
            ];
        }
    }
}

// Parse changelog entries (last 5)
$changelog = [];
if (preg_match_all('/### (\d{4}-\d{2}-\d{2}) \(([^)]+)\)\n([\s\S]*?)(?=\n### \d{4}|\n---|\Z)/', $roadmapContent, $matches, PREG_SET_ORDER)) {
    foreach (array_slice($matches, 0, 5) as $match) {
        $changelog[] = [
            'date' => $match[1],
            'title' => $match[2],
            'content' => trim($match[3])
        ];
    }
}

// Count completed and pending items
$completedCount = substr_count($roadmapContent, '[x]');
$pendingCount = substr_count($roadmapContent, '[ ]');

$page_title = 'Roadmap';
$breadcrumbs = [
    ['label' => 'System', 'url' => '/admin/tools.php'],
    ['label' => 'Roadmap']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.roadmap-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}
.roadmap-stat {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}
.roadmap-stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent);
}
.roadmap-stat-label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}
.roadmap-stat.completed .roadmap-stat-value { color: var(--color-success); }
.roadmap-stat.pending .roadmap-stat-value { color: var(--color-warning); }
.roadmap-stat.ongoing .roadmap-stat-value { color: var(--color-info); }

.project-grid {
    display: grid;
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}

.project-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s ease;
}
.project-card:hover {
    border-color: var(--color-accent);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.project-card.expanded {
    border-color: var(--color-accent);
}

.project-header {
    padding: var(--space-lg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-md);
}
.project-info {
    flex: 1;
}
.project-info h3 {
    margin: 0 0 var(--space-xs);
    font-size: 1.125rem;
    color: var(--color-text-primary);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.project-info p {
    margin: 0;
    color: var(--color-text-secondary);
    font-size: 0.875rem;
}

.project-meta {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.progress-ring {
    width: 56px;
    height: 56px;
    position: relative;
}
.progress-ring svg {
    transform: rotate(-90deg);
}
.progress-ring-bg {
    fill: none;
    stroke: var(--color-bg-page);
    stroke-width: 6;
}
.progress-ring-fill {
    fill: none;
    stroke: var(--color-accent);
    stroke-width: 6;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.3s ease;
}
.progress-ring.completed .progress-ring-fill { stroke: var(--color-success); }
.progress-ring.ongoing .progress-ring-fill { stroke: var(--color-info); }
.progress-ring-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--color-text-primary);
}

.status-badge {
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-full);
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    white-space: nowrap;
}
.status-badge.klar { background: var(--color-success); color: white; }
.status-badge.progress { background: var(--color-warning); color: #000; }
.status-badge.pagaende { background: var(--color-info); color: white; }

.expand-icon {
    color: var(--color-text-muted);
    transition: transform 0.2s ease;
}
.project-card.expanded .expand-icon {
    transform: rotate(180deg);
}

.project-details {
    display: none;
    padding: 0 var(--space-lg) var(--space-lg);
    border-top: 1px solid var(--color-border);
    background: var(--color-bg-page);
}
.project-card.expanded .project-details {
    display: block;
}
.project-details-content {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    line-height: 1.7;
}
.project-details-content h3,
.project-details-content h4 {
    color: var(--color-text-primary);
    margin: var(--space-md) 0 var(--space-sm);
    font-size: 0.95rem;
}
.project-details-content ul {
    margin: var(--space-sm) 0;
    padding-left: var(--space-lg);
}
.project-details-content li {
    margin-bottom: var(--space-xs);
}
.project-details-content code {
    background: var(--color-bg-surface);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
}
.project-details-content pre {
    background: var(--color-bg-surface);
    padding: var(--space-md);
    border-radius: var(--radius-sm);
    overflow-x: auto;
    font-size: 0.8rem;
}

.changelog-section {
    margin-top: var(--space-xl);
}
.changelog-entry {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
}
.changelog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-md);
}
.changelog-date {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}
.changelog-title {
    font-weight: 600;
    color: var(--color-accent);
}
.changelog-content {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    line-height: 1.6;
}

.quick-links {
    display: flex;
    gap: var(--space-sm);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}

/* Mobile */
@media (max-width: 767px) {
    .roadmap-stats {
        grid-template-columns: repeat(2, 1fr);
    }
    .roadmap-stat {
        padding: var(--space-md);
    }
    .roadmap-stat-value {
        font-size: 1.5rem;
    }
    .project-card,
    .changelog-entry {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .project-header {
        flex-wrap: wrap;
    }
    .project-meta {
        width: 100%;
        justify-content: space-between;
        margin-top: var(--space-sm);
    }
}
</style>

<!-- Quick Links -->
<div class="quick-links">
    <a href="/admin/tools.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="wrench"></i> Verktyg
    </a>
    <a href="/admin/migrations.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="database"></i> Migrationer
    </a>
</div>

<!-- Stats -->
<div class="roadmap-stats">
    <div class="roadmap-stat">
        <div class="roadmap-stat-value"><?= count($projectAreas) ?></div>
        <div class="roadmap-stat-label">Projekt</div>
    </div>
    <div class="roadmap-stat completed">
        <div class="roadmap-stat-value"><?= $completedCount ?></div>
        <div class="roadmap-stat-label">Avklarade</div>
    </div>
    <div class="roadmap-stat pending">
        <div class="roadmap-stat-value"><?= $pendingCount ?></div>
        <div class="roadmap-stat-label">Aterstar</div>
    </div>
    <div class="roadmap-stat ongoing">
        <div class="roadmap-stat-value"><?= count(array_filter($projectAreas, function($p) { return strpos(strtolower($p['status']), 'pagaende') !== false; })) ?></div>
        <div class="roadmap-stat-label">Pagaende</div>
    </div>
</div>

<!-- Project Areas -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="layers"></i> Projektomraden</h2>
    </div>
    <div class="admin-card-body" style="padding:var(--space-md);">
        <div class="project-grid">
            <?php foreach ($projectAreas as $area): ?>
            <?php
                $statusLower = strtolower($area['status']);
                $statusClass = 'planned';
                if (strpos($statusLower, 'klar') !== false) {
                    $statusClass = 'klar';
                } elseif (strpos($statusLower, 'pagaende') !== false) {
                    $statusClass = 'pagaende';
                } elseif (strpos($statusLower, '%') !== false) {
                    $statusClass = 'progress';
                }

                $progressClass = $area['progress'] >= 100 ? 'completed' : ($area['progress'] > 0 ? 'ongoing' : '');
                $circumference = 2 * 3.14159 * 22;
                $offset = $circumference - ($area['progress'] / 100) * $circumference;

                // Get project details if available
                $details = $projectDetails[$area['id']] ?? null;
            ?>
            <div class="project-card" data-project="<?= $area['id'] ?>">
                <div class="project-header" onclick="toggleProject('<?= $area['id'] ?>')">
                    <div class="project-info">
                        <h3>
                            <?= htmlspecialchars($area['name']) ?>
                            <span class="status-badge <?= $statusClass ?>"><?= htmlspecialchars($area['status']) ?></span>
                        </h3>
                        <p><?= htmlspecialchars($area['description']) ?></p>
                    </div>
                    <div class="project-meta">
                        <div class="progress-ring <?= $progressClass ?>">
                            <svg width="56" height="56">
                                <circle class="progress-ring-bg" cx="28" cy="28" r="22"></circle>
                                <circle class="progress-ring-fill" cx="28" cy="28" r="22"
                                    stroke-dasharray="<?= $circumference ?>"
                                    stroke-dashoffset="<?= $offset ?>"></circle>
                            </svg>
                            <span class="progress-ring-text"><?= $area['progress'] ?>%</span>
                        </div>
                        <i data-lucide="chevron-down" class="expand-icon"></i>
                    </div>
                </div>
                <div class="project-details">
                    <div class="project-details-content">
                        <?php if ($details): ?>
                            <?php
                            // Convert markdown to basic HTML
                            $content = htmlspecialchars($details['content']);
                            $content = preg_replace('/\*\*([^*]+)\*\*/', '<strong>$1</strong>', $content);
                            $content = preg_replace('/`([^`]+)`/', '<code>$1</code>', $content);
                            $content = preg_replace('/^### (.+)$/m', '<h4>$1</h4>', $content);
                            $content = preg_replace('/^- \[x\] (.+)$/m', '<li style="color:var(--color-success);">✓ $1</li>', $content);
                            $content = preg_replace('/^- \[ \] (.+)$/m', '<li style="color:var(--color-text-muted);">○ $1</li>', $content);
                            $content = preg_replace('/^- (.+)$/m', '<li>$1</li>', $content);
                            $content = preg_replace('/```[\w]*\n([\s\S]*?)```/', '<pre>$1</pre>', $content);
                            echo nl2br($content);
                            ?>
                        <?php else: ?>
                            <p style="color:var(--color-text-muted);">Detaljerad information finns i ROADMAP.md</p>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</div>

<!-- Changelog -->
<div class="changelog-section">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="history"></i> Senaste uppdateringar</h2>
        </div>
        <div class="admin-card-body" style="padding:0;">
            <?php if (empty($changelog)): ?>
            <p style="padding:var(--space-xl);text-align:center;color:var(--color-text-muted);">
                Ingen changelog hittad
            </p>
            <?php else: ?>
            <?php foreach ($changelog as $entry): ?>
            <div class="changelog-entry" style="margin:var(--space-md);margin-bottom:0;">
                <div class="changelog-header">
                    <span class="changelog-title"><?= htmlspecialchars($entry['title']) ?></span>
                    <span class="changelog-date"><?= htmlspecialchars($entry['date']) ?></span>
                </div>
                <div class="changelog-content">
                    <?php
                    $content = htmlspecialchars($entry['content']);
                    $content = preg_replace('/^\s*-\s+\*\*([^*]+)\*\*/m', '<li><strong>$1</strong>', $content);
                    $content = preg_replace('/^\s*-\s+/m', '<li>', $content);
                    $content = preg_replace('/\*\*([^*]+)\*\*/', '<strong>$1</strong>', $content);
                    $content = preg_replace('/`([^`]+)`/', '<code>$1</code>', $content);
                    echo nl2br($content);
                    ?>
                </div>
            </div>
            <?php endforeach; ?>
            <div style="padding:var(--space-md);"></div>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Raw Markdown Link -->
<div style="margin-top:var(--space-lg);text-align:center;">
    <p style="color:var(--color-text-muted);font-size:0.875rem;">
        Full dokumentation: <code>/ROADMAP.md</code>
    </p>
</div>

<script>
function toggleProject(projectId) {
    const card = document.querySelector(`[data-project="${projectId}"]`);
    if (card) {
        card.classList.toggle('expanded');
    }
}

// Initialize Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
