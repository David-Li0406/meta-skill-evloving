            </div><!-- .page-content -->
        </main>
    </div>

    <?php include __DIR__ . '/admin-mobile-nav.php'; ?>
    <?php include HUB_ROOT . '/components/footer.php'; ?>

    <!-- Toast Container -->
    <div id="toast-container" class="toast-container"></div>

    <!-- Lucide Icons - pinned to specific version for stability -->
    <script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>
    <script>
        // Initialize icons - handle async loading
        function initLucideIcons() {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            } else {
                // Retry after a short delay if lucide hasn't loaded yet
                setTimeout(initLucideIcons, 50);
            }
        }

        // Initialize immediately
        initLucideIcons();

        // Re-initialize on DOMContentLoaded
        document.addEventListener('DOMContentLoaded', initLucideIcons);

        // Re-initialize after full page load
        window.addEventListener('load', initLucideIcons);
    </script>

    <!-- Theme.js removed - always light theme -->
    <script src="<?= hub_asset('js/app.js') ?>"></script>
</body>
</html>
