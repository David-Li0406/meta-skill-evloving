<?php
/**
 * MINIMAL WORKING RIDER PAGE
 * Replace your broken pages/rider.php with this if needed
 */

require_once __DIR__ . '/../config.php';

$rider_id = $_GET['id'] ?? null;

if (!$rider_id) {
    die("No rider ID provided");
}

// Get rider data
$rider = $db->getRow("
    SELECT 
        r.*,
        c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.id = ?
", [$rider_id]);

if (!$rider) {
    die("Rider not found");
}

// Get ranking (simple version)
$ranking = $db->getRow("
    SELECT 
        position,
        total_points,
        events_counted
    FROM ranking_snapshots
    WHERE rider_id = ?
      AND discipline = 'enduro'
      AND snapshot_date = (
          SELECT MAX(snapshot_date) 
          FROM ranking_snapshots 
          WHERE rider_id = ?
      )
", [$rider_id, $rider_id]);

// Get results
$results = $db->getAll("
    SELECT 
        r.*,
        e.name as event_name,
        e.date as event_date,
        e.discipline,
        v.name as venue_name
    FROM results r
    INNER JOIN events e ON r.event_id = e.id
    LEFT JOIN venues v ON e.venue_id = v.id
    WHERE r.rider_id = ?
    ORDER BY e.date DESC
    LIMIT 50
", [$rider_id]);

include __DIR__ . '/../components/header.php';
?>

<div class="container" style="padding: 2rem; max-width: 1200px; margin: 0 auto;">
    <!-- Rider Header -->
    <div style="background: var(--card-bg); padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h1 style="margin: 0 0 1rem 0;"><?= htmlspecialchars($rider['name']) ?></h1>
        
        <?php if ($rider['club_name']): ?>
            <p style="color: var(--text-muted); margin: 0;">
                🏢 <?= htmlspecialchars($rider['club_name']) ?>
            </p>
        <?php endif; ?>
    </div>
    
    <!-- Ranking -->
    <?php if ($ranking): ?>
    <div style="background: var(--card-bg); padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
        <h2>🏆 Ranking</h2>
        
        <div style="display: flex; gap: 2rem; margin-top: 1rem;">
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">
                    #<?= $ranking['position'] ?>
                </div>
                <div style="color: var(--text-muted);">Position</div>
            </div>
            
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">
                    <?= number_format($ranking['total_points'], 1) ?>
                </div>
                <div style="color: var(--text-muted);">Poäng</div>
            </div>
            
            <div>
                <div style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">
                    <?= $ranking['events_counted'] ?>
                </div>
                <div style="color: var(--text-muted);">Event</div>
            </div>
        </div>
    </div>
    <?php endif; ?>
    
    <!-- Results -->
    <div style="background: var(--card-bg); padding: 2rem; border-radius: 8px;">
        <h2>📊 Resultat (<?= count($results) ?>)</h2>
        
        <?php if (empty($results)): ?>
            <p style="color: var(--text-muted); margin-top: 1rem;">Inga resultat hittades</p>
        <?php else: ?>
            <table style="width: 100%; margin-top: 1rem; border-collapse: collapse;">
                <thead>
                    <tr style="border-bottom: 2px solid var(--border-color);">
                        <th style="padding: 0.75rem; text-align: left;">Datum</th>
                        <th style="padding: 0.75rem; text-align: left;">Event</th>
                        <th style="padding: 0.75rem; text-align: left;">Bana</th>
                        <th style="padding: 0.75rem; text-align: center;">Placering</th>
                        <th style="padding: 0.75rem; text-align: right;">Tid</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results as $result): ?>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 0.75rem;">
                                <?= date('Y-m-d', strtotime($result['event_date'])) ?>
                            </td>
                            <td style="padding: 0.75rem;">
                                <a href="/event/<?= $result['event_id'] ?>" style="color: var(--primary-color); text-decoration: none;">
                                    <?= htmlspecialchars($result['event_name']) ?>
                                </a>
                            </td>
                            <td style="padding: 0.75rem;">
                                <?= htmlspecialchars($result['venue_name'] ?? '-') ?>
                            </td>
                            <td style="padding: 0.75rem; text-align: center; font-weight: bold;">
                                <?php if ($result['position'] <= 3): ?>
                                    <?= ['🥇','🥈','🥉'][$result['position']-1] ?>
                                <?php endif; ?>
                                <?= $result['position'] ?>
                            </td>
                            <td style="padding: 0.75rem; text-align: right; font-family: monospace;">
                                <?= $result['finish_time'] ?? '-' ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/../components/footer.php'; ?>
