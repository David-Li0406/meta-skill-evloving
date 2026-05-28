<?php http_response_code(404); $requested = $pageInfo['params']['requested'] ?? 'okänd sida'; ?>
<div class="page-grid">
  <section class="card grid-full text-center p-lg">
    <div class="mb-md text-muted">
      <i data-lucide="bike" class="icon-2xl"></i>
    </div>
    <h1 class="text-2xl font-bold mb-sm">404 – Sidan hittades inte</h1>
    <p class="text-secondary mb-lg">Sidan <code class="code"><?= htmlspecialchars($requested) ?></code> finns inte.</p>
    <div class="flex justify-center gap-md">
      <a href="/" class="btn btn--primary">Tillbaka till start</a>
      <a href="/results" class="btn btn--secondary">Visa resultat</a>
    </div>
  </section>
</div>
