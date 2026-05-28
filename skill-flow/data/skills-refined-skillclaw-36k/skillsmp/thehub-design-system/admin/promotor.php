<?php
/**
 * Promotor Panel - Shows promotor's assigned events
 * Uses standard admin layout with sidebar
 */

require_once __DIR__ . '/../config.php';
require_admin();

// Require at least promotor role
if (!hasRole('promotor')) {
    set_flash('error', 'Du har inte behörighet till denna sida');
    redirect('/');
}

$db = getDB();
$currentUser = getCurrentAdmin();
$userId = $currentUser['id'] ?? 0;

// Get promotor's series
$series = [];
try {
    $series = $db->getAll("
        SELECT s.*,
               pr.swish_number as recipient_swish,
               pr.swish_name as recipient_swish_name,
               m.filepath as banner_url,
               COUNT(DISTINCT e.id) as event_count
        FROM series s
        JOIN promotor_series ps ON ps.series_id = s.id
        LEFT JOIN payment_recipients pr ON s.payment_recipient_id = pr.id
        LEFT JOIN media m ON s.banner_media_id = m.id
        LEFT JOIN events e ON e.series_id = s.id AND YEAR(e.date) = YEAR(CURDATE())
        WHERE ps.user_id = ?
        GROUP BY s.id
        ORDER BY s.name
    ", [$userId]);
} catch (Exception $e) {
    error_log("Promotor series error: " . $e->getMessage());
}

// Get promotor's events
$events = [];
try {
    $events = $db->getAll("
        SELECT e.*,
               s.name as series_name,
               s.logo as series_logo,
               COALESCE(reg.registration_count, 0) as registration_count,
               COALESCE(reg.confirmed_count, 0) as confirmed_count,
               COALESCE(reg.pending_count, 0) as pending_count,
               COALESCE(ord.total_paid, 0) as total_paid,
               COALESCE(ord.total_pending, 0) as total_pending
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        JOIN promotor_events pe ON pe.event_id = e.id
        LEFT JOIN (
            SELECT event_id,
                   COUNT(*) as registration_count,
                   SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed_count,
                   SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_count
            FROM event_registrations
            GROUP BY event_id
        ) reg ON reg.event_id = e.id
        LEFT JOIN (
            SELECT event_id,
                   SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END) as total_paid,
                   SUM(CASE WHEN payment_status = 'pending' THEN total_amount ELSE 0 END) as total_pending
            FROM orders
            GROUP BY event_id
        ) ord ON ord.event_id = e.id
        WHERE pe.user_id = ?
        ORDER BY e.date DESC
    ", [$userId]);
} catch (Exception $e) {
    error_log("Promotor events error: " . $e->getMessage());
}

// Page config for unified layout
$page_title = 'Mina Tävlingar';
$breadcrumbs = [
    ['label' => 'Mina Tävlingar']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.promotor-grid {
    display: grid;
    gap: var(--space-lg);
}
.event-card {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    border: 1px solid var(--color-border);
    overflow: hidden;
}
.event-card-header {
    padding: var(--space-lg);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}
.event-info {
    flex: 1;
}
.event-title {
    font-size: var(--text-xl);
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 var(--space-xs) 0;
}
.event-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
}
.event-meta-item {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}
.event-meta-item i {
    width: 16px;
    height: 16px;
}
.event-series {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    background: var(--color-bg-sunken);
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-full);
}
.event-series img {
    width: 20px;
    height: 20px;
    object-fit: contain;
}
.event-card-body {
    padding: var(--space-lg);
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-sm);
    margin-bottom: var(--space-lg);
}
@media (max-width: 600px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Mobile edge-to-edge design */
@media (max-width: 767px) {
    .event-card,
    .series-card {
        margin-left: calc(-1 * var(--space-md));
        margin-right: calc(-1 * var(--space-md));
        border-radius: 0;
        border-left: none;
        border-right: none;
        width: calc(100% + var(--space-md) * 2);
    }
    .series-grid,
    .promotor-grid {
        gap: 0;
    }
    .series-grid {
        grid-template-columns: 1fr;
    }
    .event-card + .event-card,
    .series-card + .series-card {
        border-top: none;
    }
}
.stat-box {
    background: var(--color-bg-sunken);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    text-align: center;
}
.stat-value {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-accent);
}
.stat-value.success {
    color: var(--color-success);
}
.stat-value.pending {
    color: var(--color-warning);
}
.stat-label {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.event-actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
}
.event-actions .btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
}
.event-actions .btn i {
    width: 16px;
    height: 16px;
}
.empty-state {
    text-align: center;
    padding: var(--space-2xl);
    color: var(--color-text-secondary);
}
.empty-state i {
    width: 48px;
    height: 48px;
    margin-bottom: var(--space-md);
    opacity: 0.5;
}
.empty-state h2 {
    margin: 0 0 var(--space-sm) 0;
    color: var(--color-text-primary);
}

/* Series section */
.section-title {
    font-size: var(--text-xl);
    font-weight: 600;
    margin: 0 0 var(--space-lg) 0;
    color: var(--color-text-primary);
}
.series-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--space-lg);
    margin-bottom: var(--space-2xl);
}
.series-card {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    border: 1px solid var(--color-border);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.series-card-header {
    padding: var(--space-lg);
    display: flex;
    align-items: center;
    gap: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}
.series-logo {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-md);
    background: var(--color-bg-sunken);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
}
.series-logo img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
.series-info h3 {
    margin: 0 0 var(--space-2xs) 0;
    font-size: var(--text-lg);
}
.series-info p {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.series-card-body {
    padding: var(--space-lg);
    flex: 1;
}
.series-detail {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-sm);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.series-detail i {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
}
.series-detail.missing {
    color: var(--color-warning);
}
.series-card-footer {
    padding: var(--space-md) var(--space-lg);
    background: var(--color-bg-sunken);
    border-top: 1px solid var(--color-border);
}
.series-card-footer .btn {
    width: 100%;
}

/* Modal styles */
.modal {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    padding: var(--space-lg);
    overflow-y: auto;
}
.modal.active {
    display: flex;
    align-items: flex-start;
    justify-content: center;
}
.modal-content {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    max-width: 500px;
    width: 100%;
    margin-top: var(--space-xl);
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}
.modal-header h3 {
    margin: 0;
}
.modal-close {
    background: none;
    border: none;
    padding: var(--space-xs);
    cursor: pointer;
    color: var(--color-text-secondary);
    font-size: 24px;
    line-height: 1;
}
.modal-body {
    padding: var(--space-lg);
}
.modal-footer {
    padding: var(--space-md) var(--space-lg);
    background: var(--color-bg-sunken);
    border-top: 1px solid var(--color-border);
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
}
.form-group {
    margin-bottom: var(--space-md);
}
.form-label {
    display: block;
    margin-bottom: var(--space-xs);
    font-weight: 500;
    font-size: var(--text-sm);
}
.form-input {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-sunken);
    color: var(--color-text-primary);
}
.form-hint {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}
.logo-preview {
    width: 100%;
    height: 80px;
    background: var(--color-bg-sunken);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--space-sm);
    overflow: hidden;
}
.logo-preview img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
.logo-actions {
    display: flex;
    gap: var(--space-sm);
}

@media (max-width: 599px) {
    .modal {
        padding: 0;
    }
    .modal-content {
        max-width: 100%;
        height: 100%;
        margin: 0;
        border-radius: 0;
        display: flex;
        flex-direction: column;
    }
    .modal-body {
        flex: 1;
        overflow-y: auto;
    }
}
</style>

<!-- MINA SERIER -->
<?php if (!empty($series)): ?>
<h2 class="section-title">Mina Serier</h2>
<div class="series-grid">
    <?php foreach ($series as $s): ?>
    <div class="series-card" data-series-id="<?= $s['id'] ?>">
        <div class="series-card-header">
            <div class="series-logo">
                <?php if ($s['logo']): ?>
                    <img src="<?= h($s['logo']) ?>" alt="<?= h($s['name']) ?>">
                <?php else: ?>
                    <i data-lucide="medal"></i>
                <?php endif; ?>
            </div>
            <div class="series-info">
                <h3><?= h($s['name']) ?></h3>
                <p><?= (int)$s['event_count'] ?> tävlingar <?= date('Y') ?></p>
            </div>
        </div>
        <div class="series-card-body">
            <?php
            $swishNumber = $s['swish_number'] ?? $s['recipient_swish'] ?? null;
            $swishName = $s['swish_name'] ?? $s['recipient_swish_name'] ?? null;
            ?>
            <?php if ($swishNumber): ?>
            <div class="series-detail">
                <i data-lucide="smartphone"></i>
                <span>Swish: <?= h($swishNumber) ?></span>
            </div>
            <?php else: ?>
            <div class="series-detail missing">
                <i data-lucide="alert-triangle"></i>
                <span>Swish ej konfigurerat</span>
            </div>
            <?php endif; ?>

            <?php if ($s['banner_media_id'] ?? null): ?>
            <div class="series-detail">
                <i data-lucide="image"></i>
                <span>Banner konfigurerad</span>
            </div>
            <?php else: ?>
            <div class="series-detail missing">
                <i data-lucide="image-off"></i>
                <span>Ingen banner</span>
            </div>
            <?php endif; ?>
        </div>
        <div class="series-card-footer">
            <button class="btn btn-secondary" onclick="editSeries(<?= $s['id'] ?>)">
                <i data-lucide="settings"></i>
                Redigera inställningar
            </button>
        </div>
    </div>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- MINA TÄVLINGAR -->
<?php if (empty($events)): ?>
<div class="event-card">
    <div class="empty-state">
        <i data-lucide="calendar-x"></i>
        <h2>Inga tävlingar</h2>
        <p>Du har inga tävlingar tilldelade ännu. Kontakta administratören för att få tillgång.</p>
    </div>
</div>
<?php else: ?>
<div class="promotor-grid">
    <?php foreach ($events as $event): ?>
    <div class="event-card">
        <div class="event-card-header">
            <div class="event-info">
                <h2 class="event-title"><?= h($event['name']) ?></h2>
                <div class="event-meta">
                    <span class="event-meta-item">
                        <i data-lucide="calendar"></i>
                        <?= date('j M Y', strtotime($event['date'])) ?>
                    </span>
                    <?php if ($event['location']): ?>
                    <span class="event-meta-item">
                        <i data-lucide="map-pin"></i>
                        <?= h($event['location']) ?>
                    </span>
                    <?php endif; ?>
                </div>
            </div>
            <?php if ($event['series_name']): ?>
            <span class="event-series">
                <?php if ($event['series_logo']): ?>
                <img src="<?= h($event['series_logo']) ?>" alt="">
                <?php endif; ?>
                <?= h($event['series_name']) ?>
            </span>
            <?php endif; ?>
        </div>

        <div class="event-card-body">
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-value"><?= (int)$event['registration_count'] ?></div>
                    <div class="stat-label">Anmälda</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value success"><?= (int)$event['confirmed_count'] ?></div>
                    <div class="stat-label">Bekräftade</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value pending"><?= (int)$event['pending_count'] ?></div>
                    <div class="stat-label">Väntande</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value"><?= number_format($event['total_paid'], 0, ',', ' ') ?> kr</div>
                    <div class="stat-label">Betalat</div>
                </div>
            </div>

            <div class="event-actions">
                <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" class="btn btn-primary">
                    <i data-lucide="pencil"></i>
                    Redigera event
                </a>
                <a href="/admin/promotor-registrations.php?event_id=<?= $event['id'] ?>" class="btn btn-secondary">
                    <i data-lucide="users"></i>
                    Anmälningar
                </a>
                <a href="/admin/promotor-payments.php?event_id=<?= $event['id'] ?>" class="btn btn-secondary">
                    <i data-lucide="credit-card"></i>
                    Betalningar
                </a>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Series Edit Modal -->
<div class="modal" id="seriesModal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="seriesModalTitle">Redigera serie</h3>
            <button type="button" class="modal-close" onclick="closeSeriesModal()">&times;</button>
        </div>
        <form id="seriesForm" onsubmit="saveSeries(event)">
            <input type="hidden" id="seriesId" name="id">
            <div class="modal-body">
                <h4 style="margin: 0 0 var(--space-md) 0; font-size: var(--text-md);">
                    <i data-lucide="smartphone" style="width: 18px; height: 18px; vertical-align: middle;"></i>
                    Swish-betalning
                </h4>
                <p style="font-size: var(--text-sm); color: var(--color-text-secondary); margin-bottom: var(--space-md);">
                    Konfigurerar Swish för alla tävlingar i serien (om inte tävlingen har egen inställning).
                </p>

                <div class="form-group">
                    <label class="form-label">Swish-nummer</label>
                    <input type="text" class="form-input" id="seriesSwishNumber" name="swish_number" placeholder="070-1234567 eller 123-456 78 90">
                    <div class="form-hint">Telefonnummer eller organisationsnummer kopplat till Swish</div>
                </div>

                <div class="form-group">
                    <label class="form-label">Swish-namn</label>
                    <input type="text" class="form-input" id="seriesSwishName" name="swish_name" placeholder="Förening ABC">
                    <div class="form-hint">Namnet som visas för mottagaren i Swish-appen</div>
                </div>

                <hr style="margin: var(--space-lg) 0; border: none; border-top: 1px solid var(--color-border);">

                <h4 style="margin: 0 0 var(--space-md) 0; font-size: var(--text-md);">
                    <i data-lucide="image" style="width: 18px; height: 18px; vertical-align: middle;"></i>
                    Serie-banner
                </h4>
                <p style="font-size: var(--text-sm); color: var(--color-text-secondary); margin-bottom: var(--space-md);">
                    Visas på alla tävlingar i serien (om inte tävlingen har egen banner).
                </p>

                <div class="form-group">
                    <label class="form-label">Banner <code style="background: var(--color-bg-sunken); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">1200×150px</code></label>
                    <div class="logo-preview" id="seriesBannerPreview">
                        <i data-lucide="image-plus" style="width: 24px; height: 24px; opacity: 0.5;"></i>
                    </div>
                    <input type="hidden" id="seriesBannerMediaId" name="banner_media_id">
                    <div class="logo-actions">
                        <input type="file" id="seriesBannerUpload" accept="image/*" style="display:none" onchange="uploadSeriesBanner(this)">
                        <button type="button" class="btn btn-sm btn-primary" onclick="document.getElementById('seriesBannerUpload').click()">
                            <i data-lucide="upload"></i> Ladda upp
                        </button>
                        <button type="button" class="btn btn-sm btn-ghost" onclick="clearSeriesBanner()">
                            <i data-lucide="x"></i> Ta bort
                        </button>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeSeriesModal()">Avbryt</button>
                <button type="submit" class="btn btn-primary">Spara</button>
            </div>
        </form>
    </div>
</div>

<script>
// Store series data for modal
const seriesData = <?= json_encode(array_column($series, null, 'id')) ?>;
let currentSeriesId = null;

function editSeries(id) {
    const s = seriesData[id];
    if (!s) {
        alert('Kunde inte hitta seriedata');
        return;
    }

    currentSeriesId = id;
    document.getElementById('seriesId').value = id;
    document.getElementById('seriesModalTitle').textContent = 'Redigera ' + s.name;

    // Set Swish fields - try series-specific first, then payment recipient
    document.getElementById('seriesSwishNumber').value = s.swish_number || s.recipient_swish || '';
    document.getElementById('seriesSwishName').value = s.swish_name || s.recipient_swish_name || '';

    // Set banner preview
    clearSeriesBanner();
    if (s.banner_media_id && s.banner_url) {
        document.getElementById('seriesBannerMediaId').value = s.banner_media_id;
        document.getElementById('seriesBannerPreview').innerHTML = `<img src="${s.banner_url}" alt="Banner">`;
    }

    document.getElementById('seriesModal').classList.add('active');
    // Reinitialize Lucide icons in the modal
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function closeSeriesModal() {
    document.getElementById('seriesModal').classList.remove('active');
    currentSeriesId = null;
}

async function uploadSeriesBanner(input) {
    const file = input.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        alert('Välj en bildfil (JPG, PNG, etc.)');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('Filen är för stor. Max 10MB.');
        return;
    }

    const preview = document.getElementById('seriesBannerPreview');
    preview.innerHTML = '<span style="font-size: 12px; color: var(--color-text-secondary);">Laddar upp...</span>';

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('folder', 'series');

        const response = await fetch('/api/media.php?action=upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success && result.media) {
            document.getElementById('seriesBannerMediaId').value = result.media.id;
            preview.innerHTML = `<img src="/${result.media.filepath}" alt="Banner">`;
        } else {
            alert('Uppladdning misslyckades: ' + (result.error || 'Okänt fel'));
            clearSeriesBanner();
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert('Ett fel uppstod vid uppladdning');
        clearSeriesBanner();
    }

    input.value = '';
}

function clearSeriesBanner() {
    document.getElementById('seriesBannerMediaId').value = '';
    document.getElementById('seriesBannerPreview').innerHTML = '<i data-lucide="image-plus" style="width: 24px; height: 24px; opacity: 0.5;"></i>';
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function saveSeries(event) {
    event.preventDefault();

    const form = document.getElementById('seriesForm');
    const formData = new FormData(form);

    const data = {
        id: currentSeriesId,
        swish_number: formData.get('swish_number') || null,
        swish_name: formData.get('swish_name') || null,
        banner_media_id: formData.get('banner_media_id') || null
    };

    try {
        const response = await fetch('/api/series.php?action=update_promotor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            closeSeriesModal();
            location.reload();
        } else {
            alert(result.error || 'Kunde inte spara');
        }
    } catch (error) {
        console.error('Save error:', error);
        alert('Ett fel uppstod');
    }
}

// Close modal on escape or background click
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSeriesModal();
});
document.getElementById('seriesModal').addEventListener('click', e => {
    if (e.target === document.getElementById('seriesModal')) closeSeriesModal();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
