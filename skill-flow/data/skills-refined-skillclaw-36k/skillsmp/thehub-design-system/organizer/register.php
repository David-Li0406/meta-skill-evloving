<?php
/**
 * Organizer App - Platsregistrering (Demo)
 */

require_once __DIR__ . '/config.php';
requireOrganizer();

$eventId = (int)($_GET['event'] ?? 0);
if (!$eventId) {
    header('Location: dashboard.php');
    exit;
}

$event = getEventWithClasses($eventId);
if (!$event) {
    die('Eventet hittades inte.');
}

$pageTitle = $event['name'];
$showHeader = true;
$headerTitle = $event['name'];
$showBackButton = true;
$backUrl = 'dashboard.php';
$mainClass = 'org-main--narrow'; // Keep narrow on all screens

include __DIR__ . '/includes/header.php';
?>

<!-- Steg 1: Sök eller ny -->
<div id="step-search" class="org-card">
    <div class="org-card__body">
        <h2 class="text-center mb-lg">Sök deltagare</h2>

        <div class="org-search mb-lg">
            <i data-lucide="search" class="org-search__icon"></i>
            <input type="text" id="search-input" class="org-input" placeholder="Skriv namn..." autocomplete="off">
        </div>

        <div id="search-results" class="mb-lg hidden" style="display:none;"></div>

        <div style="text-align: center; margin-bottom: 16px; color: var(--color-text-muted);">eller</div>

        <button type="button" id="btn-new" class="org-btn org-btn--ghost org-btn--large org-btn--block">
            <i data-lucide="user-plus"></i>
            Ny deltagare
        </button>
    </div>
</div>

<!-- Steg 2: Formulär -->
<div id="step-form" class="org-card hidden" style="display:none;">
    <div class="org-card__body">
        <h2 class="text-center mb-lg">Uppgifter</h2>

        <form id="rider-form">
            <input type="hidden" id="rider_id" value="">

            <div class="grid-2-col">
                <div class="org-form-group">
                    <label class="org-label">Förnamn *</label>
                    <input type="text" id="first_name" class="org-input" required>
                </div>
                <div class="org-form-group">
                    <label class="org-label">Efternamn *</label>
                    <input type="text" id="last_name" class="org-input" required>
                </div>
            </div>

            <div class="grid-2-col">
                <div class="org-form-group">
                    <label class="org-label">Födelseår</label>
                    <input type="number" id="birth_year" class="org-input" placeholder="1990">
                </div>
                <div class="org-form-group">
                    <label class="org-label">Kön</label>
                    <select id="gender" class="org-select">
                        <option value="">Välj...</option>
                        <option value="M">Man</option>
                        <option value="F">Kvinna</option>
                    </select>
                </div>
            </div>

            <div class="org-form-group">
                <label class="org-label">E-post</label>
                <input type="email" id="email" class="org-input" placeholder="namn@exempel.se">
            </div>

            <div class="org-form-group">
                <label class="org-label">Telefon</label>
                <input type="tel" id="phone" class="org-input" placeholder="070-123 45 67">
            </div>

            <div class="grid-2-col">
                <div class="org-form-group">
                    <label class="org-label">Klubb</label>
                    <input type="text" id="club" class="org-input" placeholder="Klubbnamn">
                </div>
                <div class="org-form-group">
                    <label class="org-label">Nationalitet</label>
                    <input type="text" id="nationality" class="org-input" placeholder="SWE" maxlength="3" style="text-transform: uppercase;">
                </div>
            </div>

            <div class="org-form-group">
                <label class="org-label">Licensnummer</label>
                <input type="text" id="license_number" class="org-input" placeholder="SCF/UCI licensnummer">
            </div>

            <hr style="border: none; border-top: 1px solid var(--color-border); margin: var(--space-lg) 0;">

            <h3 style="font-size: 14px; font-weight: 600; margin-bottom: var(--space-md); color: var(--color-text-secondary);">Nödkontakt (ICE)</h3>

            <div class="grid-2-col">
                <div class="org-form-group">
                    <label class="org-label">Kontaktperson</label>
                    <input type="text" id="ice_name" class="org-input" placeholder="Namn på anhörig">
                </div>
                <div class="org-form-group">
                    <label class="org-label">Telefon (ICE)</label>
                    <input type="tel" id="ice_phone" class="org-input" placeholder="070-123 45 67">
                </div>
            </div>

            <div class="mt-lg" style="display: flex; gap: 16px;">
                <button type="button" class="org-btn org-btn--ghost" onclick="showStep('search')">
                    <i data-lucide="arrow-left"></i> Tillbaka
                </button>
                <button type="submit" class="org-btn org-btn--primary flex-1">
                    Välj klass <i data-lucide="arrow-right"></i>
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Steg 3: Välj klass -->
<div id="step-class" class="org-card hidden" style="display:none;">
    <div class="org-card__body">
        <div id="rider-display" class="mb-lg text-center">
            <div id="display-name" style="font-size: 20px; font-weight: 600;"></div>
            <div id="display-club" class="text-muted"></div>
        </div>

        <h2 class="text-center mb-lg">Välj klass</h2>

        <div class="org-class-grid">
            <button type="button" class="org-class-btn" data-class="Elite Herr" data-price="450">
                <div class="org-class-btn__name">Elite Herr</div>
                <div class="org-class-btn__price">450 kr</div>
            </button>
            <button type="button" class="org-class-btn" data-class="Elite Dam" data-price="450">
                <div class="org-class-btn__name">Elite Dam</div>
                <div class="org-class-btn__price">450 kr</div>
            </button>
            <button type="button" class="org-class-btn" data-class="Sport Herr" data-price="350">
                <div class="org-class-btn__name">Sport Herr</div>
                <div class="org-class-btn__price">350 kr</div>
            </button>
            <button type="button" class="org-class-btn" data-class="Sport Dam" data-price="350">
                <div class="org-class-btn__name">Sport Dam</div>
                <div class="org-class-btn__price">350 kr</div>
            </button>
            <button type="button" class="org-class-btn" data-class="Junior" data-price="250">
                <div class="org-class-btn__name">Junior</div>
                <div class="org-class-btn__price">250 kr</div>
            </button>
            <button type="button" class="org-class-btn" data-class="Barn" data-price="150">
                <div class="org-class-btn__name">Barn</div>
                <div class="org-class-btn__price">150 kr</div>
            </button>
        </div>

        <div class="mt-lg">
            <button type="button" class="org-btn org-btn--ghost" onclick="showStep('form')">
                <i data-lucide="arrow-left"></i> Tillbaka
            </button>
        </div>
    </div>
</div>

<!-- Steg 4: Betalning -->
<div id="step-pay" class="org-card hidden" style="display:none;">
    <div class="org-card__body text-center">
        <div id="pay-info" class="mb-lg">
            <div id="pay-name" style="font-size: 18px; font-weight: 600;"></div>
            <div id="pay-class" class="text-muted"></div>
        </div>

        <div id="pay-amount" class="mb-lg" style="font-size: 48px; font-weight: 700;"></div>

        <div style="background: white; padding: 16px; border-radius: 12px; display: inline-block; margin-bottom: 16px;">
            <img id="qr-code" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=DEMO-BETALNING" alt="QR" style="width: 160px; height: 160px;">
        </div>

        <div class="mb-lg text-accent" style="font-size: 24px; font-weight: 600;">
            BETALA
        </div>

        <button type="button" class="org-btn org-btn--primary org-btn--large org-btn--block" onclick="showStep('done')">
            <i data-lucide="check"></i> Klar
        </button>

        <button type="button" class="org-btn org-btn--ghost mt-sm" onclick="showStep('class')">
            <i data-lucide="arrow-left"></i> Ändra klass
        </button>
    </div>
</div>

<!-- Steg 5: Klart -->
<div id="step-done" class="org-card hidden" style="display:none;">
    <div class="org-card__body" style="text-align: center; padding: 48px 24px;">
        <div style="width: 64px; height: 64px; background: var(--color-success); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px;">
            <i data-lucide="check" style="width: 32px; height: 32px; color: white;"></i>
        </div>

        <h1 class="mb-xs">Registrerad!</h1>
        <div id="done-name" style="font-size: 18px;"></div>
        <div id="done-class" class="mb-lg text-muted"></div>

        <div id="done-bib" class="text-accent" style="font-size: 64px; font-weight: 700; margin-bottom: 32px;">#42</div>

        <button type="button" class="org-btn org-btn--primary org-btn--large org-btn--block" onclick="resetAll()">
            <i data-lucide="plus"></i> Nästa deltagare
        </button>
    </div>
</div>

<script>
(function() {
    let riderData = {};
    let selectedClass = '';
    let selectedPrice = 0;

    // Sök
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    searchInput.addEventListener('input', function() {
        const q = this.value.trim();
        if (q.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        // Simulera sökning (demo)
        fetch('api/search-rider.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: q })
        })
        .then(r => r.json())
        .then(data => {
            if (data.riders && data.riders.length > 0) {
                searchResults.innerHTML = data.riders.map(r => `
                    <div class="org-event-card cursor-pointer mb-xs" onclick='selectRider(${JSON.stringify(r)})'>
                        <div class="org-event-card__info">
                            <div class="org-event-card__name">${r.firstname} ${r.lastname}</div>
                            <div class="org-event-card__meta">${r.club_name || ''} ${r.birth_year ? '• ' + r.birth_year : ''}</div>
                        </div>
                    </div>
                `).join('');
                searchResults.style.display = 'block';
                lucide.createIcons();
            } else {
                searchResults.innerHTML = '<div style="padding: 16px; text-align: center; color: var(--color-text-muted);">Ingen träff</div>';
                searchResults.style.display = 'block';
            }
        })
        .catch(() => {
            searchResults.innerHTML = '<div style="padding: 16px; text-align: center; color: var(--color-text-muted);">Ingen träff</div>';
            searchResults.style.display = 'block';
        });
    });

    // Välj från sök
    window.selectRider = function(r) {
        document.getElementById('rider_id').value = r.id || '';
        document.getElementById('first_name').value = r.firstname || '';
        document.getElementById('last_name').value = r.lastname || '';
        document.getElementById('birth_year').value = r.birth_year || '';
        document.getElementById('gender').value = r.gender || '';
        document.getElementById('email').value = r.email || '';
        document.getElementById('phone').value = r.phone || '';
        document.getElementById('club').value = r.club_name || '';
        document.getElementById('nationality').value = r.nationality || 'SWE';
        document.getElementById('license_number').value = r.license_number || '';
        document.getElementById('ice_name').value = r.ice_name || '';
        document.getElementById('ice_phone').value = r.ice_phone || '';
        showStep('form');
    };

    // Ny deltagare
    document.getElementById('btn-new').addEventListener('click', function() {
        document.getElementById('rider-form').reset();
        document.getElementById('rider_id').value = '';
        showStep('form');
    });

    // Formulär
    document.getElementById('rider-form').addEventListener('submit', function(e) {
        e.preventDefault();
        riderData = {
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value,
            club: document.getElementById('club').value
        };
        document.getElementById('display-name').textContent = riderData.first_name + ' ' + riderData.last_name;
        document.getElementById('display-club').textContent = riderData.club || '';
        showStep('class');
    });

    // Klassval
    document.querySelectorAll('.org-class-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.org-class-btn').forEach(b => b.classList.remove('org-class-btn--selected'));
            this.classList.add('org-class-btn--selected');

            selectedClass = this.dataset.class;
            selectedPrice = this.dataset.price;

            document.getElementById('pay-name').textContent = riderData.first_name + ' ' + riderData.last_name;
            document.getElementById('pay-class').textContent = selectedClass;
            document.getElementById('pay-amount').textContent = selectedPrice + ' kr';

            showStep('pay');
        });
    });

    // Visa steg
    window.showStep = function(step) {
        ['search', 'form', 'class', 'pay', 'done'].forEach(s => {
            document.getElementById('step-' + s).style.display = 'none';
        });
        document.getElementById('step-' + step).style.display = 'block';

        if (step === 'done') {
            document.getElementById('done-name').textContent = riderData.first_name + ' ' + riderData.last_name;
            document.getElementById('done-class').textContent = selectedClass;
            document.getElementById('done-bib').textContent = '#' + Math.floor(Math.random() * 100 + 1);
        }

        lucide.createIcons();
    };

    // Reset
    window.resetAll = function() {
        riderData = {};
        selectedClass = '';
        selectedPrice = 0;
        document.getElementById('rider-form').reset();
        document.getElementById('search-input').value = '';
        searchResults.style.display = 'none';
        document.querySelectorAll('.org-class-btn').forEach(b => b.classList.remove('org-class-btn--selected'));
        showStep('search');
    };

    lucide.createIcons();
})();
</script>

<?php include __DIR__ . '/includes/footer.php'; ?>
