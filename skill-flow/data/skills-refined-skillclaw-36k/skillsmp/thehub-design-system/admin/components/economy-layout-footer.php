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
        function initLucideIcons() {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            } else {
                setTimeout(initLucideIcons, 50);
            }
        }
        initLucideIcons();
        document.addEventListener('DOMContentLoaded', initLucideIcons);
        window.addEventListener('load', initLucideIcons);
    </script>

    <script src="<?= hub_asset('js/app.js') ?>"></script>
</body>
</html>
