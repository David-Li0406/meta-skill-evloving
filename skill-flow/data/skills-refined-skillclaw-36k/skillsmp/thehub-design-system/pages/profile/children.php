<?php
/**
 * TheHUB V1.0 - Linked Children
 * Manage parent-child relationships for registration
 */

$currentUser = hub_current_user();
if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();
$linkedChildren = hub_get_linked_children($currentUser['id']);
$message = $_GET['msg'] ?? '';
?>

<div class="page-header">
    <nav class="breadcrumb">
        <a href="/profile">Min Sida</a>
        <span class="breadcrumb-sep">›</span>
        <span>Kopplade barn</span>
    </nav>
    <h1 class="page-title">
        <i data-lucide="users" class="page-icon"></i>
        Kopplade barn
    </h1>
    <p class="page-subtitle">Hantera barn du kan anmäla till tävlingar</p>
</div>

<?php if ($message === 'added'): ?>
    <div class="alert alert-success">Barn har lagts till!</div>
<?php elseif ($message === 'removed'): ?>
    <div class="alert alert-success">Koppling har tagits bort.</div>
<?php endif; ?>

<?php if (empty($linkedChildren)): ?>
    <div class="empty-state card">
        <div class="empty-icon"><i data-lucide="users" class="icon-xl"></i></div>
        <h3>Inga kopplade barn</h3>
        <p>Du har inga barn kopplade till din profil ännu. Koppla barn för att kunna anmäla dem till tävlingar.</p>
    </div>
<?php else: ?>
    <div class="children-list">
        <?php foreach ($linkedChildren as $child): ?>
            <div class="child-card">
                <div class="child-avatar">
                    <?= strtoupper(substr($child['firstname'], 0, 1)) ?>
                </div>
                <div class="child-info">
                    <a href="/database/rider/<?= $child['id'] ?>" class="child-name">
                        <?= htmlspecialchars($child['firstname'] . ' ' . $child['lastname']) ?>
                    </a>
                    <?php if ($child['birth_year']): ?>
                        <span class="child-age">Född <?= $child['birth_year'] ?></span>
                    <?php endif; ?>
                </div>
                <div class="child-actions">
                    <a href="/profile/edit-child/<?= $child['id'] ?>" class="btn btn-sm btn-outline">Redigera</a>
                    <button type="button" class="btn btn-sm btn-danger-outline"
                            onclick="confirmRemove(<?= $child['id'] ?>, '<?= htmlspecialchars($child['firstname']) ?>')">
                        Ta bort
                    </button>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<!-- Add Child Section -->
<div class="add-section card">
    <h2>Lägg till barn</h2>
    <p>Sök efter ditt barn i databasen eller skapa en ny profil.</p>

    <div class="add-options">
        <div class="add-option">
            <h3>Sök befintlig åkare</h3>
            <?php
            $searchType = 'riders';
            $placeholder = 'Sök barnets namn...';
            $onSelect = 'handleChildSelect';
            include HUB_ROOT . '/components/search-live.php';
            ?>
        </div>

        <div class="add-divider">eller</div>

        <div class="add-option">
            <h3>Skapa ny profil</h3>
            <a href="/profile/add-child" class="btn btn-outline">+ Skapa ny barnprofil</a>
        </div>
    </div>
</div>


<!-- CSS loaded from /assets/css/pages/profile-children.css -->
