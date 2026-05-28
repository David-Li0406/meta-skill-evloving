<?php
/**
 * V3 Clubs Page - All clubs
 */

$db = hub_db();

// Get all clubs with member counts
$clubs = $db->query("
    SELECT
        c.id, c.name, c.city, c.logo,
        COUNT(DISTINCT r.id) as member_count,
        COUNT(DISTINCT res.id) as result_count,
        SUM(res.points) as total_points
    FROM clubs c
    LEFT JOIN riders r ON c.id = r.club_id AND r.active = 1
    LEFT JOIN results res ON r.id = res.cyclist_id
    WHERE c.active = 1
    GROUP BY c.id
    ORDER BY member_count DESC, c.name ASC
")->fetchAll(PDO::FETCH_ASSOC);

$total = count($clubs);
$totalMembers = array_sum(array_column($clubs, 'member_count'));
?>

<h1 class="text-2xl font-bold mb-lg">Klubbar</h1>

<div class="page-grid">
  <!-- Stats -->
  <section class="card grid-full">
    <div class="stats-row">
      <div class="stat-block">
        <div class="stat-value"><?= $total ?></div>
        <div class="stat-label">Klubbar</div>
      </div>
      <div class="stat-block">
        <div class="stat-value"><?= $totalMembers ?></div>
        <div class="stat-label">Medlemmar</div>
      </div>
    </div>
  </section>

  <!-- Clubs List -->
  <section class="card grid-full" aria-labelledby="clubs-title">
    <div class="card-header">
      <div>
        <h2 id="clubs-title" class="card-title">Alla klubbar</h2>
        <p class="card-subtitle"><?= $total ?> klubbar</p>
      </div>
    </div>

    <?php if (empty($clubs)): ?>
    <div class="text-center p-lg">
      <p class="text-muted">Inga klubbar registrerade</p>
    </div>
    <?php else: ?>
    <div class="table-wrapper">
      <table class="table table--striped table--clickable">
        <thead>
          <tr>
            <th scope="col" style="width: 50px;"></th>
            <th scope="col">Klubb</th>
            <th scope="col" class="table-col-hide-portrait">Ort</th>
            <th scope="col" class="text-right">Medlemmar</th>
            <th scope="col" class="text-right table-col-hide-portrait">Resultat</th>
            <th scope="col" class="text-right table-col-hide-portrait">Poäng</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($clubs as $club): ?>
          <tr data-href="/club/<?= $club['id'] ?>">
            <td>
              <?php if (!empty($club['logo'])): ?>
                <img src="<?= htmlspecialchars($club['logo']) ?>" alt=""
                     style="width: 32px; height: 32px; object-fit: contain; border-radius: var(--radius-sm); background: var(--color-bg-secondary);">
              <?php else: ?>
                <div style="width: 32px; height: 32px; border-radius: var(--radius-sm); background: var(--color-bg-secondary); display: flex; align-items: center; justify-content: center;">
                  <i data-lucide="building-2" style="width: 16px; height: 16px; opacity: 0.4;"></i>
                </div>
              <?php endif; ?>
            </td>
            <td class="col-rider"><?= htmlspecialchars($club['name']) ?></td>
            <td class="table-col-hide-portrait text-secondary"><?= htmlspecialchars($club['city'] ?? '-') ?></td>
            <td class="text-right"><?= $club['member_count'] ?></td>
            <td class="text-right table-col-hide-portrait"><?= $club['result_count'] ?></td>
            <td class="text-right table-col-hide-portrait col-points"><?= number_format($club['total_points'] ?? 0) ?></td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>

    <!-- Mobile Card View -->
    <div class="result-list">
      <?php foreach ($clubs as $club): ?>
      <a href="/club/<?= $club['id'] ?>" class="result-item">
        <div class="result-place" style="padding: 0;">
          <?php if (!empty($club['logo'])): ?>
            <img src="<?= htmlspecialchars($club['logo']) ?>" alt=""
                 style="width: 40px; height: 40px; object-fit: contain; border-radius: var(--radius-sm); background: var(--color-bg-secondary);">
          <?php else: ?>
            <div style="width: 40px; height: 40px; border-radius: var(--radius-sm); background: var(--color-bg-secondary); display: flex; align-items: center; justify-content: center;">
              <i data-lucide="building-2" style="width: 20px; height: 20px; opacity: 0.4;"></i>
            </div>
          <?php endif; ?>
        </div>
        <div class="result-info">
          <div class="result-name"><?= htmlspecialchars($club['name']) ?></div>
          <div class="result-club"><?= htmlspecialchars($club['city'] ?? '') ?></div>
        </div>
        <div class="result-time"><?= $club['member_count'] ?> medl.</div>
      </a>
      <?php endforeach; ?>
    </div>
    <?php endif; ?>
  </section>
</div>
