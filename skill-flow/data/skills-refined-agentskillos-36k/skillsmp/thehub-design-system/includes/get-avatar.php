<?php
/**
 * Avatar Display Helper Functions
 *
 * Functions for displaying rider avatars with fallbacks
 */

/**
 * Get rider avatar URL with fallback to UI Avatars
 *
 * @param array $rider The rider data array (must contain 'firstname', 'lastname', optionally 'avatar_url')
 * @param int $size The size of the avatar in pixels (default: 200)
 * @return string The avatar URL
 */
function get_rider_avatar($rider, $size = 200) {
    // If rider has an avatar URL stored, use it
    if (!empty($rider['avatar_url'])) {
        return $rider['avatar_url'];
    }

    // Fallback: generate avatar using UI Avatars service
    return get_initials_avatar($rider, $size);
}

/**
 * Get UI Avatars URL for rider initials
 *
 * @param array $rider The rider data array
 * @param int $size The size in pixels
 * @return string The UI Avatars URL
 */
function get_initials_avatar($rider, $size = 200) {
    $firstName = $rider['firstname'] ?? '';
    $lastName = $rider['lastname'] ?? '';

    // Build name for avatar
    $name = trim($firstName . ' ' . $lastName);
    if (empty($name)) {
        $name = 'Rider';
    }

    // URL encode the name
    $encodedName = urlencode($name);

    // Generate UI Avatars URL with TheHUB colors
    // Using --color-accent (#61CE70) as background
    return "https://ui-avatars.com/api/?name={$encodedName}&size={$size}&background=61CE70&color=ffffff&bold=true&format=svg";
}

/**
 * Get rider initials
 *
 * @param array $rider The rider data array
 * @return string The initials (max 2 characters)
 */
function get_rider_initials($rider) {
    $firstName = $rider['firstname'] ?? '';
    $lastName = $rider['lastname'] ?? '';

    $initials = '';

    if (!empty($firstName)) {
        $initials .= mb_substr($firstName, 0, 1);
    }

    if (!empty($lastName)) {
        $initials .= mb_substr($lastName, 0, 1);
    }

    if (empty($initials)) {
        $initials = '?';
    }

    return mb_strtoupper($initials);
}

/**
 * Generate HTML for rider avatar with fallback
 *
 * @param array $rider The rider data array
 * @param int $size The size in pixels
 * @param string $class Additional CSS classes
 * @return string HTML for the avatar
 */
function render_rider_avatar($rider, $size = 200, $class = '') {
    $avatarUrl = get_rider_avatar($rider, $size);
    $initials = get_rider_initials($rider);
    $name = htmlspecialchars(($rider['firstname'] ?? '') . ' ' . ($rider['lastname'] ?? ''), ENT_QUOTES, 'UTF-8');

    $sizeStyle = "width: {$size}px; height: {$size}px;";

    // If we have a custom avatar URL (not ui-avatars fallback)
    if (!empty($rider['avatar_url'])) {
        return <<<HTML
<div class="avatar-container {$class}" style="{$sizeStyle}">
    <img
        src="{$avatarUrl}"
        alt="Profilbild för {$name}"
        class="avatar-image"
        loading="lazy"
        onerror="this.onerror=null; this.style.display='none'; this.nextElementSibling.style.display='flex';"
    >
    <div class="avatar-fallback" style="display: none;">
        <span class="avatar-initials">{$initials}</span>
    </div>
</div>
HTML;
    }

    // Fallback avatar (UI Avatars or initials)
    return <<<HTML
<div class="avatar-container {$class}" style="{$sizeStyle}">
    <img
        src="{$avatarUrl}"
        alt="Profilbild för {$name}"
        class="avatar-image"
        loading="lazy"
    >
</div>
HTML;
}

/**
 * Generate inline CSS for avatar styles
 *
 * Include this in your page's <style> or CSS file
 *
 * @return string CSS styles
 */
function get_avatar_styles() {
    return <<<CSS
.avatar-container {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    overflow: hidden;
    background: var(--color-accent, #61CE70);
    flex-shrink: 0;
}

.avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

.avatar-fallback {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-accent, #61CE70);
    color: #ffffff;
    font-weight: 700;
    font-size: 2.5rem;
}

.avatar-container[style*="width: 40px"] .avatar-fallback,
.avatar-container[style*="width: 48px"] .avatar-fallback {
    font-size: 1rem;
}

.avatar-container[style*="width: 64px"] .avatar-fallback {
    font-size: 1.25rem;
}

.avatar-container[style*="width: 80px"] .avatar-fallback,
.avatar-container[style*="width: 100px"] .avatar-fallback {
    font-size: 1.5rem;
}

/* Avatar upload preview */
.avatar-upload-container {
    position: relative;
    display: inline-block;
}

.avatar-upload-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    opacity: 0;
    transition: opacity 0.3s ease;
    cursor: pointer;
}

.avatar-upload-container:hover .avatar-upload-overlay {
    opacity: 1;
}

.avatar-upload-overlay i,
.avatar-upload-overlay svg {
    color: #ffffff;
    width: 32px;
    height: 32px;
}

.avatar-upload-input {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
}

/* Loading state */
.avatar-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
}

.avatar-loading::after {
    content: '';
    width: 32px;
    height: 32px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: avatar-spin 0.8s linear infinite;
}

@keyframes avatar-spin {
    to { transform: rotate(360deg); }
}
CSS;
}
