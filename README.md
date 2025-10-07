# Theofanis Papadopoulos — Plastic Surgeon (Informational Website)

A fast, accessible, static website for a plastic surgeon in Thessaloniki, Greece. Focused on helpful public information, good UX, and strong Core Web Vitals.

> Greek version of the README: see **[README.el.md](./README.el.md)**.

---

## General Info
- **Doctor:** Dr. Theofanis Papadopoulos, Plastic Surgeon (Thessaloniki).
- **Purpose:** Clear, educational pages about procedures and non-invasive treatments, clinic locations, and contact info.
- **Notes:** Content is written to be informative (no promotions/testimonials). Each medical page lists “Risks & Complications,” “Alternatives,” and “Last updated” date.

---

## Technical Overview

### Stack
- **Static** HTML/CSS/JS (no framework) for speed and simplicity
- **Hosting:** cPanel
- **SEO:** `sitemap.xml`, `robots.txt`
- **Accessibility:** WCAG-AA contrast, keyboard focus, reduced motion, alt texts
- **Core Web Vitals:** LCP prioritization, `defer` scripts, lean CSS

### Project Structure
```

/
├─ index.html
├─ about.html
├─ procedures.html
├─ non-invasive.html
├─ reconstructive.html
├─ faq.html
├─ contact.html
├─ styles.css
├─ script.js
├─ photos/
├─ robots.txt
└─ sitemap.xml

````

### Sitemap & robots

**robots.txt**

```
User-agent: *
Allow: /

Sitemap: https://theofanispapadopoulos.gr/sitemap.xml
```

**sitemap.xml** (minimal example)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://theofanispapadopoulos.gr/</loc>
    <lastmod>2025-10-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://theofanispapadopoulos.gr/photos/main-4_3.webp</image:loc>
      <image:title>Ουδέτερη φωτογραφία ιατρικού χώρου</image:title>
    </image:image>
  </url>
  <!-- + add about, procedures, non-invasive, reconstructive, media, faq, contact -->
</urlset>
```

### Accessibility & UX

* Visible focus ring
* Consistent color contrast (WCAG-AA)
* `alt` text on images
* `prefers-reduced-motion` support

### Performance Notes

* `defer` non-critical JS
* Lazy-load all non-LCP images

---

## Contributing

PRs for accessibility, CWV, and SEO improvements are welcome. Keep content neutral/informative and avoid promotional claims.

## License

Code: MIT.
Content and images: © respective authors.
