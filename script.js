/* =========================================================
   script.js — Site behaviors (organized & documented)
   Sections:
   1) NAVIGATION (mobile toggle, active link)
   2) PROCEDURES SEARCH (live filter + highlighting)
   3) FOOTER METADATA (year + lastUpdated datetime)
   ========================================================= */

/* =========================================================
   1) NAVIGATION — Burger toggle, a11y, and active link
   ========================================================= */
(() => {
  const nav = document.querySelector(".navlinks");
  const toggle = document.querySelector("#menuToggle");
  if (!nav || !toggle) return;

  const linksWrap = nav.querySelector(".links");

  const setExpanded = (open) => {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  };

  // Toggle on click
  toggle.addEventListener("click", () => {
    const willOpen = !nav.classList.contains("open");
    nav.classList.toggle("open", willOpen);
    setExpanded(willOpen);
  });

  // Close with Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("open")) {
      nav.classList.remove("open");
      setExpanded(false);
    }
  });

  // Close when clicking outside of the menu
  document.addEventListener("click", (e) => {
    if (!nav.contains(e.target) && nav.classList.contains("open")) {
      nav.classList.remove("open");
      setExpanded(false);
    }
  });

  // Close when a menu link is clicked (better UX on mobile)
  linksWrap?.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a) return;
    if (nav.classList.contains("open")) {
      nav.classList.remove("open");
      setExpanded(false);
    }
  });

  // Close if we resize back above burger breakpoint (1120px)
  const closeIfDesktop = () => {
    if (window.innerWidth > 1120 && nav.classList.contains("open")) {
      nav.classList.remove("open");
      setExpanded(false);
    }
  };
  window.addEventListener("resize", closeIfDesktop);

  // Highlight active link (by file name)
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".links a").forEach((a) => {
    const href = a.getAttribute("href");
    if (!href) return;
    // Match exact file (ignoring query/hash)
    const file = href.split("/").pop().split("?")[0].split("#")[0];
    if (file === path) a.classList.add("active");
  });
})();

/* =========================================================
   2) PROCEDURES SEARCH — Live filter + letter-accurate highlights
   ========================================================= */
(() => {
  const input = document.getElementById("procSearch");
  if (!input) return; // not on this page

  const sections = Array.from(document.querySelectorAll(".proc-section"));
  const resultCount = document.getElementById("resultCount");

  // Build cache of all cards once
  const cards = [];
  sections.forEach((section) => {
    section.querySelectorAll(".proc-grid .proc-card").forEach((card) => {
      const titleEl = card.querySelector(".proc-title");
      const descEl = card.querySelector(".proc-desc");
      const titleText = titleEl?.textContent || "";
      const descText = descEl?.textContent || "";
      cards.push({ section, card, titleEl, descEl, titleText, descText });
    });
  });

  const escapeRegExp = (str) => str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const highlight = (text, query) => {
    if (!query) return text;
    const pattern = new RegExp(escapeRegExp(query), "gi");
    return text.replace(pattern, (m) => `<mark class="hl">${m}</mark>`);
  };

  const updateSectionVisibility = () => {
    sections.forEach((section) => {
      const visibleCards = section.querySelectorAll(
        '.proc-grid .proc-card:not([data-hidden="true"])'
      ).length;
      section.classList.toggle("is-hidden", visibleCards === 0);
    });
  };

  const onSearch = () => {
    const q = input.value.trim();
    let visible = 0;

    cards.forEach(({ card, titleEl, descEl, titleText, descText }) => {
      // Reset to original content before applying highlights
      if (titleEl) titleEl.innerHTML = titleText;
      if (descEl) descEl.innerHTML = descText;

      if (!q) {
        card.style.display = "";
        card.removeAttribute("data-hidden");
        visible++;
        return;
      }

      const hay = (titleText + " " + descText).toLowerCase();
      const ok = hay.includes(q.toLowerCase());

      if (ok) {
        if (titleEl) titleEl.innerHTML = highlight(titleText, q);
        if (descEl) descEl.innerHTML = highlight(descText, q);
        card.style.display = "";
        card.removeAttribute("data-hidden");
        visible++;
      } else {
        card.style.display = "none";
        card.setAttribute("data-hidden", "true");
      }
    });

    updateSectionVisibility();

    if (resultCount) {
      resultCount.textContent = q
        ? `${visible} αποτέλεσμα(τα) για «${q}»`
        : "Εμφάνιση όλων των επεμβάσεων";
    }
  };

  // Input listeners
  input.addEventListener("input", onSearch);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      input.value = "";
      onSearch();
    }
  });

  // Initial render (no filter)
  onSearch();
})();

/* =========================================================
   3) FOOTER METADATA — Year & machine-readable last updated
   ========================================================= */
(() => {
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Keep machine-readable datetime in sync (human text already printed in HTML)
  const dt = document.getElementById("lastUpdated");
  if (dt) dt.setAttribute("datetime", "2025-09-21");
})();
