<?php
/**
 * TheHUB Achievements - Badge Collection Page
 * Grid layout with large illustrated badges
 *
 * @version 3.0 - Grid Layout Redesign
 * @package TheHUB
 */

// Include achievements system
$achievementsPath = dirname(__DIR__) . '/includes/achievements.php';
if (file_exists($achievementsPath)) {
    require_once $achievementsPath;
}

$achievementsClubPath = dirname(__DIR__) . '/includes/achievements-club.php';
if (file_exists($achievementsClubPath)) {
    require_once $achievementsClubPath;
}

// Get achievement definitions
$riderAchievements = getRiderAchievementDefinitions();
$clubAchievements = getClubAchievementDefinitions();

// Count visible badges (exclude hidden)
function countVisibleBadges($categories) {
    $count = 0;
    foreach ($categories as $cat) {
        foreach ($cat['badges'] as $badge) {
            if (!isset($badge['hidden']) || !$badge['hidden']) {
                $count++;
            }
        }
    }
    return $count;
}

$totalRiderBadges = countVisibleBadges($riderAchievements);
$totalClubBadges = countVisibleBadges($clubAchievements);
$totalBadges = $totalRiderBadges + $totalClubBadges;

// Demo: Mock earned badges (replace with real data from database)
$earnedCount = 0; // Will be replaced with actual user data
$progressPercent = $totalBadges > 0 ? round(($earnedCount / $totalBadges) * 100) : 0;
?>

<main class="main-content">
    <link rel="stylesheet" href="/assets/css/achievements.css?v=<?= filemtime(__DIR__ . '/../assets/css/achievements.css') ?>">

    <div class="badges-page">
        <!-- Header with progress -->
        <header class="badges-header">
            <div class="badges-header-content">
                <h1>Achievements</h1>
                <p class="badges-subtitle">Samla badges och fira dina prestationer i GravitySeries!</p>
            </div>
            <div class="progress-container">
                <div class="progress-stats">
                    <span class="earned"><?= $earnedCount ?></span>
                    <span class="total">/<?= $totalBadges ?></span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: <?= $progressPercent ?>%"></div>
                </div>
            </div>
        </header>

        <!-- Tab Navigation -->
        <nav class="badges-tabs">
            <button class="badge-tab active" data-tab="rider">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="8" r="4"/>
                    <path d="M20 21a8 8 0 1 0-16 0"/>
                </svg>
                Åkare
                <span class="tab-count"><?= $totalRiderBadges ?></span>
            </button>
            <button class="badge-tab" data-tab="club">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                Klubb
                <span class="tab-count"><?= $totalClubBadges ?></span>
            </button>
        </nav>

        <!-- RIDER ACHIEVEMENTS TAB -->
        <div class="badge-tab-content active" id="rider-tab">
            <?php foreach ($riderAchievements as $categoryId => $category): ?>
                <?php
                $visibleBadges = array_filter($category['badges'], fn($b) => !isset($b['hidden']) || !$b['hidden']);
                if (empty($visibleBadges)) continue;
                ?>
                <section class="badge-category">
                    <h2 class="category-title"><?= htmlspecialchars($category['title']) ?></h2>
                    <div class="badge-grid">
                        <?php foreach ($visibleBadges as $badge): ?>
                            <div class="badge-card"
                                 data-badge="<?= htmlspecialchars($badge['id']) ?>"
                                 data-name="<?= htmlspecialchars($badge['name']) ?>"
                                 data-requirement="<?= htmlspecialchars($badge['requirement']) ?>"
                                 data-description="<?= htmlspecialchars($badge['description']) ?>"
                                 data-counter="<?= $badge['has_counter'] ?? false ? 'true' : 'false' ?>">
                                <div class="badge-icon-wrapper">
                                    <?php if (isset($badge['svg_function']) && function_exists($badge['svg_function'])): ?>
                                        <?= call_user_func($badge['svg_function']) ?>
                                    <?php else: ?>
                                        <svg class="badge-svg" viewBox="0 0 100 116">
                                            <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="<?= $badge['accent'] ?? '#61CE70' ?>" opacity="0.2"/>
                                            <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="none" stroke="<?= $badge['accent'] ?? '#61CE70' ?>" stroke-width="2"/>
                                        </svg>
                                    <?php endif; ?>
                                </div>
                                <span class="badge-name"><?= htmlspecialchars($badge['name']) ?></span>
                            </div>
                        <?php endforeach; ?>
                    </div>
                </section>
            <?php endforeach; ?>
        </div>

        <!-- CLUB ACHIEVEMENTS TAB -->
        <div class="badge-tab-content" id="club-tab">
            <?php foreach ($clubAchievements as $categoryId => $category): ?>
                <?php
                $visibleBadges = array_filter($category['badges'], fn($b) => !isset($b['hidden']) || !$b['hidden']);
                if (empty($visibleBadges)) continue;
                ?>
                <section class="badge-category">
                    <h2 class="category-title"><?= htmlspecialchars($category['title']) ?></h2>
                    <div class="badge-grid">
                        <?php foreach ($visibleBadges as $badge): ?>
                            <div class="badge-card"
                                 data-badge="<?= htmlspecialchars($badge['id']) ?>"
                                 data-name="<?= htmlspecialchars($badge['name']) ?>"
                                 data-requirement="<?= htmlspecialchars($badge['requirement']) ?>"
                                 data-description="<?= htmlspecialchars($badge['description']) ?>"
                                 data-counter="<?= $badge['has_counter'] ?? false ? 'true' : 'false' ?>">
                                <div class="badge-icon-wrapper">
                                    <?php if (isset($badge['svg_function']) && function_exists($badge['svg_function'])): ?>
                                        <?= call_user_func($badge['svg_function']) ?>
                                    <?php else: ?>
                                        <svg class="badge-svg" viewBox="0 0 100 116">
                                            <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="<?= $badge['accent'] ?? '#61CE70' ?>" opacity="0.2"/>
                                            <path d="M50 3L95 29V87L50 113L5 87V29L50 3Z" fill="none" stroke="<?= $badge['accent'] ?? '#61CE70' ?>" stroke-width="2"/>
                                        </svg>
                                    <?php endif; ?>
                                </div>
                                <span class="badge-name"><?= htmlspecialchars($badge['name']) ?></span>
                            </div>
                        <?php endforeach; ?>
                    </div>
                </section>
            <?php endforeach; ?>
        </div>

        <!-- Info Section -->
        <section class="badges-info">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 16v-4M12 8h.01"/>
            </svg>
            <p>Badges tilldelas automatiskt när du tävlar och uppfyller kraven. Kolla din profil för att se vilka du samlat!</p>
        </section>
    </div>

    <!-- Badge Detail Modal -->
    <div class="badge-modal" id="badge-modal">
        <div class="badge-modal-overlay"></div>
        <div class="badge-modal-content">
            <button class="badge-modal-close" aria-label="Stäng">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
            </button>
            <div class="badge-modal-icon" id="modal-badge-icon"></div>
            <h3 class="badge-modal-title" id="modal-badge-name"></h3>
            <p class="badge-modal-requirement" id="modal-badge-requirement"></p>
            <p class="badge-modal-description" id="modal-badge-description"></p>
            <div class="badge-modal-counter-info" id="modal-counter-info">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                Kan samlas flera gånger
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Tab switching
        const tabs = document.querySelectorAll('.badge-tab');
        const tabContents = document.querySelectorAll('.badge-tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.dataset.tab;

                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));

                tab.classList.add('active');
                document.getElementById(tabId + '-tab').classList.add('active');
            });
        });

        // Badge modal
        const modal = document.getElementById('badge-modal');
        const modalOverlay = modal.querySelector('.badge-modal-overlay');
        const modalClose = modal.querySelector('.badge-modal-close');
        const modalIcon = document.getElementById('modal-badge-icon');
        const modalName = document.getElementById('modal-badge-name');
        const modalRequirement = document.getElementById('modal-badge-requirement');
        const modalDescription = document.getElementById('modal-badge-description');
        const modalCounterInfo = document.getElementById('modal-counter-info');

        document.querySelectorAll('.badge-card').forEach(card => {
            card.addEventListener('click', () => {
                const iconWrapper = card.querySelector('.badge-icon-wrapper');
                modalIcon.innerHTML = iconWrapper.innerHTML;
                modalName.textContent = card.dataset.name;
                modalRequirement.textContent = card.dataset.requirement;
                modalDescription.textContent = card.dataset.description;
                modalCounterInfo.style.display = card.dataset.counter === 'true' ? 'flex' : 'none';

                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            });
        });

        function closeModal() {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }

        modalOverlay.addEventListener('click', closeModal);
        modalClose.addEventListener('click', closeModal);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                closeModal();
            }
        });
    });
    </script>
</main>
