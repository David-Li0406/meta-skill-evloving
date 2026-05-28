<?php
/**
 * UCI-ID Formatter Tool
 * Converts UCI IDs to standard format: XXX XXX XXX XX
 * Example: "10022464170" → "100 224 641 70"
 */
require_once __DIR__ . '/../config.php';
require_admin();

require_once INCLUDES_PATH . '/helpers.php';

$results = [];
$input = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['uci_ids'])) {
    $input = $_POST['uci_ids'];
    $lines = preg_split('/[\r\n,;]+/', $input);

    foreach ($lines as $line) {
        $line = trim($line);
        if (empty($line)) continue;

        $formatted = normalizeUciId($line);
        $results[] = [
            'original' => $line,
            'formatted' => $formatted,
            'valid' => strlen(preg_replace('/[^0-9]/', '', $formatted)) === 11
        ];
    }
}

// Page config
$page_title = 'Formatera UCI-ID';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Formatera UCI-ID']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.formatter-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-lg);
}

@media (max-width: 768px) {
    .formatter-container {
        grid-template-columns: 1fr;
    }
}

.input-section, .output-section {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
}

.section-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    font-weight: 600;
    font-size: var(--text-lg);
}

.section-header svg {
    width: 24px;
    height: 24px;
    color: var(--color-accent);
}

.uci-textarea {
    width: 100%;
    min-height: 200px;
    padding: var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: var(--font-mono);
    font-size: var(--text-sm);
    resize: vertical;
    background: var(--color-bg-input);
    color: var(--color-text-primary);
}

.uci-textarea:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px rgba(97, 206, 112, 0.1);
}

.format-hint {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-sm);
}

.results-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
    max-height: 400px;
    overflow-y: auto;
}

.result-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-sunken);
    border-radius: var(--radius-md);
    font-family: var(--font-mono);
}

.result-item.invalid {
    background: #FEE2E2;
    border: 1px solid #FECACA;
}

.result-original {
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
}

.result-arrow {
    color: var(--color-text-muted);
    margin: 0 var(--space-sm);
}

.result-formatted {
    font-weight: 600;
    color: var(--color-accent);
    font-size: var(--text-md);
    letter-spacing: 0.5px;
}

.result-item.invalid .result-formatted {
    color: var(--color-error);
}

.copy-btn {
    padding: var(--space-2xs) var(--space-sm);
    font-size: var(--text-xs);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s;
}

.copy-btn:hover {
    background: var(--color-accent);
    color: white;
    border-color: var(--color-accent);
}

.copy-all-section {
    margin-top: var(--space-md);
    padding-top: var(--space-md);
    border-top: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.empty-state {
    text-align: center;
    padding: var(--space-2xl);
    color: var(--color-text-muted);
}

.empty-state svg {
    width: 48px;
    height: 48px;
    margin-bottom: var(--space-md);
    opacity: 0.5;
}

.btn-actions {
    display: flex;
    gap: var(--space-sm);
    margin-top: var(--space-md);
}

.info-box {
    background: var(--color-accent-light);
    border: 1px solid var(--color-accent);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-lg);
    display: flex;
    align-items: flex-start;
    gap: var(--space-sm);
}

.info-box svg {
    width: 20px;
    height: 20px;
    color: var(--color-accent);
    flex-shrink: 0;
    margin-top: 2px;
}

.info-box-content {
    font-size: var(--text-sm);
    color: var(--color-text-primary);
}

.info-box-content strong {
    display: block;
    margin-bottom: var(--space-2xs);
}
</style>

<div class="info-box">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>
    </svg>
    <div class="info-box-content">
        <strong>UCI-ID Standardformat</strong>
        Korrekt format är: <code style="background: var(--color-bg-sunken); padding: 2px 6px; border-radius: 4px;">XXX XXX XXX XX</code> (11 siffror med mellanslag)<br>
        Exempel: <code style="background: var(--color-bg-sunken); padding: 2px 6px; border-radius: 4px;">100 224 641 70</code>
    </div>
</div>

<div class="formatter-container">
    <div class="input-section">
        <div class="section-header">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
                <path d="m15 5 4 4"/>
            </svg>
            Ange UCI-ID
        </div>
        <form method="POST">
            <textarea
                name="uci_ids"
                class="uci-textarea"
                placeholder="Ange ett eller flera UCI-ID, ett per rad eller kommaseparerade.

Exempel:
10022464170
100-224-641-70
100 224 641 70"
            ><?= htmlspecialchars($input) ?></textarea>
            <p class="format-hint">Accepterar siffror med eller utan bindestreck/mellanslag. Kan klistra in flera på en gång.</p>
            <div class="btn-actions">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                        <path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>
                    </svg>
                    Formatera
                </button>
                <button type="button" class="btn-admin btn-admin-secondary" onclick="document.querySelector('.uci-textarea').value=''; document.querySelector('form').submit();">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                        <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                    </svg>
                    Rensa
                </button>
            </div>
        </form>
    </div>

    <div class="output-section">
        <div class="section-header">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 5H2v7l6.29 6.29c.94.94 2.48.94 3.42 0l3.58-3.58c.94-.94.94-2.48 0-3.42L9 5Z"/>
                <path d="M6 9.01V9"/><path d="m15 5 6.3 6.3a2.4 2.4 0 0 1 0 3.4L17 19"/>
            </svg>
            Formaterat resultat
        </div>

        <?php if (empty($results)): ?>
        <div class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 5H2v7l6.29 6.29c.94.94 2.48.94 3.42 0l3.58-3.58c.94-.94.94-2.48 0-3.42L9 5Z"/>
                <path d="M6 9.01V9"/>
            </svg>
            <p>Ange UCI-ID till vänster och klicka "Formatera"</p>
        </div>
        <?php else: ?>
        <div class="results-list">
            <?php foreach ($results as $r): ?>
            <div class="result-item <?= $r['valid'] ? '' : 'invalid' ?>">
                <div>
                    <span class="result-original"><?= htmlspecialchars($r['original']) ?></span>
                    <span class="result-arrow">→</span>
                    <span class="result-formatted"><?= htmlspecialchars($r['formatted']) ?></span>
                </div>
                <button class="copy-btn" onclick="copyToClipboard('<?= htmlspecialchars($r['formatted']) ?>', this)">
                    Kopiera
                </button>
            </div>
            <?php endforeach; ?>
        </div>

        <?php
        $validResults = array_filter($results, fn($r) => $r['valid']);
        if (count($validResults) > 1):
            $allFormatted = implode("\n", array_map(fn($r) => $r['formatted'], $validResults));
        ?>
        <div class="copy-all-section">
            <span style="font-size: var(--text-sm); color: var(--color-text-secondary);">
                <?= count($validResults) ?> giltiga UCI-ID
            </span>
            <button class="btn-admin btn-admin-secondary" onclick="copyToClipboard('<?= htmlspecialchars($allFormatted) ?>', this)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                    <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
                </svg>
                Kopiera alla
            </button>
        </div>
        <?php endif; ?>
        <?php endif; ?>
    </div>
</div>

<script>
function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><polyline points="20 6 9 17 4 12"/></svg> Kopierat!';
        btn.style.background = 'var(--color-success)';
        btn.style.color = 'white';
        btn.style.borderColor = 'var(--color-success)';

        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
            btn.style.color = '';
            btn.style.borderColor = '';
        }, 1500);
    });
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
