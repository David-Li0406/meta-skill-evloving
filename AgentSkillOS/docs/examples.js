(() => {
  const THEME_KEY = "agentskillos-theme";
  const LANG_KEY = "agentskillos-lang";

  let theme = localStorage.getItem(THEME_KEY)
    || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  let lang = localStorage.getItem(LANG_KEY) || "en";

  function applyTheme() {
    document.documentElement.setAttribute("data-theme", theme);
    const icon = document.getElementById("theme-icon");
    if (icon) icon.textContent = theme === "dark" ? "☀" : "☾";
  }

  function applyLang() {
    document.documentElement.lang = lang === "en" ? "en" : "zh-CN";
    document.querySelectorAll(".i18n").forEach((el) => {
      const next = lang === "en" ? el.dataset.en : el.dataset.zh;
      if (next) el.textContent = next;
    });

    const en = document.getElementById("lang-en");
    const zh = document.getElementById("lang-zh");
    if (en) en.classList.toggle("active", lang === "en");
    if (zh) zh.classList.toggle("active", lang === "zh");
  }

  function toggleTheme() {
    theme = theme === "dark" ? "light" : "dark";
    localStorage.setItem(THEME_KEY, theme);
    applyTheme();
  }

  function toggleLang() {
    lang = lang === "en" ? "zh" : "en";
    localStorage.setItem(LANG_KEY, lang);
    applyLang();
  }

  function openLightbox(img) {
    const box = document.getElementById("lightbox");
    const target = document.getElementById("lightbox-img");
    if (!box || !target || !img) return;
    target.src = img.src;
    box.classList.add("active");
  }

  function closeLightbox() {
    const box = document.getElementById("lightbox");
    if (box) box.classList.remove("active");
  }

  window.toggleTheme = toggleTheme;
  window.toggleLang = toggleLang;
  window.openLightbox = openLightbox;
  window.closeLightbox = closeLightbox;

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLightbox();
  });

  applyTheme();
  applyLang();
})();
