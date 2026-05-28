<?php
/**
 * TheHUB V1.0 - Live Search Component
 * Reusable search component for riders and clubs
 *
 * Usage: include this file with optional variables:
 * $searchType = 'riders' | 'clubs' | 'all'
 * $placeholder = 'Sök...'
 * $allowAdd = false (show "add new" option)
 * $onSelect = 'callback' (JavaScript callback function name)
 */

$searchType = $searchType ?? 'all';
$placeholder = $placeholder ?? ($searchType === 'riders' ? 'Sök åkare...' : ($searchType === 'clubs' ? 'Sök klubbar...' : 'Sök åkare eller klubbar...'));
$allowAdd = $allowAdd ?? false;
$onSelect = $onSelect ?? '';
$inputId = 'search-' . uniqid();
?>

<div class="live-search"
     data-search-type="<?= htmlspecialchars($searchType) ?>"
     <?= $onSelect ? 'data-on-select="' . htmlspecialchars($onSelect) . '"' : '' ?>
     <?= $allowAdd ? 'data-allow-add="true"' : '' ?>>
    <div class="search-input-wrapper">
        <span class="search-icon" aria-hidden="true">🔍</span>
        <input type="text"
               id="<?= $inputId ?>"
               class="live-search-input"
               placeholder="<?= htmlspecialchars($placeholder) ?>"
               autocomplete="off"
               role="combobox"
               aria-haspopup="listbox"
               aria-expanded="false"
               aria-autocomplete="list">
        <button type="button" class="search-clear hidden" aria-label="Rensa sökning">✕</button>
    </div>
    <div class="live-search-results hidden" role="listbox" aria-label="Sökresultat"></div>
</div>
