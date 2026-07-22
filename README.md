# Theofanis Papadopoulos — informational clinic website

This repository contains the source for a Greek-language, static, multi-page website for plastic surgeon Theofanis Papadopoulos. It uses plain HTML, CSS, and JavaScript; there is no framework, package manager, build step, template system, or client-side router.

Read [AGENTS.md](./AGENTS.md) and the preservation contract in [CODEX_GUARDRAILS.md](./CODEX_GUARDRAILS.md) before making any change. The Greek overview is in [README.el.md](./README.el.md), and detailed maintenance guidance is in [docs/MAINTENANCE.md](./docs/MAINTENANCE.md).

## Public pages

| Source file | Canonical public URL |
| --- | --- |
| `index.html` | `https://theofanispapadopoulos.gr/` |
| `about.html` | `https://theofanispapadopoulos.gr/about` |
| `procedures.html` | `https://theofanispapadopoulos.gr/procedures` |
| `non-invasive.html` | `https://theofanispapadopoulos.gr/non-invasive` |
| `reconstructive.html` | `https://theofanispapadopoulos.gr/reconstructive` |
| `media.html` | `https://theofanispapadopoulos.gr/media` |
| `faq.html` | `https://theofanispapadopoulos.gr/faq` |
| `contact.html` | `https://theofanispapadopoulos.gr/contact` |
| `guide-botouliniki-toxini.html` | `https://theofanispapadopoulos.gr/non-invasive/botouliniki-toxini` |
| `guide-yalouroniko-fillers.html` | `https://theofanispapadopoulos.gr/non-invasive/yalouroniko-fillers` |
| `guide-laser-apotrichosi.html` | `https://theofanispapadopoulos.gr/non-invasive/laser-apotrichosi` |
| `guide-lipoanarrofisi.html` | `https://theofanispapadopoulos.gr/procedures/lipoanarrofisi` |
| `guide-oules-egkavmaton.html` | `https://theofanispapadopoulos.gr/reconstructive/oules-egkavmaton` |
| `privacy.html` | `https://theofanispapadopoulos.gr/privacy` (`noindex`) |
| `image-credits.html` | `https://theofanispapadopoulos.gr/image-credits` (`noindex`) |

Canonical URLs use HTTPS, the apex domain, extensionless internal paths, and no trailing slash except for the homepage. The tracked `.htaccess` defines host, scheme, `.html`, trailing-slash, and nested-guide routing. The local preview helper reproduces flat extensionless and nested guide mappings, but production redirect behavior still requires Apache/nginx verification.

## Repository layout

- The HTML files are independent documents and the authoritative source for visible content, page metadata, breadcrumbs, and page-specific JSON-LD.
- `styles.css` contains the shared design tokens, dark and light themes, layout, responsive rules, and accessibility states.
- `script.js` progressively enhances the mobile navigation, procedure filtering and highlighting, and current footer year.
- `photos/` contains local content, social-preview, icon, and favicon assets.
- `sitemap.xml` lists the 13 indexable canonical pages and selected images; privacy and image credits stay outside it.
- `robots.txt` allows normal crawling, excludes site-search query variants, and declares the sitemap.
- `googlee2185726589adaa8.html` is the Google site-verification file and must retain its exact name and contents.

## Local preview

No installation is required. From the repository root, run:

```powershell
.\preview-site.cmd
```

Alternatively, run the route-aware helper directly:

```powershell
py tools/serve_local.py 8000
```

Then open `http://localhost:8000/`. Do not use `python -m http.server`: Python's basic static server returns `404` for the extensionless nested guide URLs. The project helper maps those routes to their source files. It does not emulate HTTPS, host canonicalization, `.html` redirects, or trailing-slash redirects; verify those production behaviors against Apache. Do not add client-side routing or an `index.html` fallback to compensate.

## Making changes

Keep changes narrow and use the implementation as the source of truth. A route-related change is a synchronized change across redirects/server configuration, canonical and Open Graph URLs, internal links, breadcrumbs, JSON-LD, `sitemap.xml`, and `robots.txt` where relevant. Contact data similarly appears in visible text, links, metadata, and structured data and must remain consistent.

Medical content must remain neutral, educational, and non-promotional. A technical edit does not justify changing a medical-review date. New or materially revised medical statements require physician review.

See [docs/MAINTENANCE.md](./docs/MAINTENANCE.md) for selectors that JavaScript depends on, theme and responsive conventions, accessibility requirements, deployment constraints, and the regression checklist.

## Licensing

No `LICENSE` file is present in this repository. Do not assume that the code, text, or images may be redistributed; confirm ownership and licensing with the site owner before reuse.
