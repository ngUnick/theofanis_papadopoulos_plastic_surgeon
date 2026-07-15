# Website maintenance guide

This guide describes the implementation currently stored in this repository. The mandatory preservation rules remain authoritative in [`AGENTS.md`](../AGENTS.md) and [`CODEX_GUARDRAILS.md`](../CODEX_GUARDRAILS.md).

## Architecture and sources of truth

The site is a static, Greek-language, multi-page application: each public route has its own HTML document and must work through a direct request without JavaScript. `script.js` is progressive enhancement, not routing infrastructure. Do not introduce a generic homepage fallback, History API navigation, or JavaScript-dependent primary navigation.

The HTML documents are authoritative for visible content, canonical tags, Open Graph metadata, breadcrumbs, and JSON-LD. `sitemap.xml` is the crawl inventory, not a generator for those values. There is no template or shared data layer, so repeated navigation, footer, identity, and schema values must be updated carefully in every affected file.

The production server configuration is not versioned. No `.htaccess` exists in this checkout even though production depends on server-side canonicalization and extensionless-to-file rewriting. Obtain and review the deployed Apache/cPanel rules before changing or claiming to validate redirect behavior.

## Routing, SEO, and structured data

The canonical URL policy is HTTPS, the apex domain, extensionless internal paths, no trailing slash on internal pages, and `/` for the homepage. Alternative HTTP, `www`, `.html`, `/index.html`, and trailing-slash forms should converge on that format at the server.

Treat a route as a synchronized system. Review all of the following whenever a public URL changes:

- production redirects and rewrite rules;
- `<link rel="canonical">` and `og:url`;
- header, footer, breadcrumb, card, and in-content links;
- visible breadcrumbs and `BreadcrumbList` data;
- JSON-LD `url` and `@id` references;
- `sitemap.xml`, including `hreflang` and image entries;
- `robots.txt` and any server-level `X-Robots-Tag` behavior.

Structured data is intentionally page-specific. Preserve stable entity `@id` values and validate each page's graph against visible content. Do not copy one page's graph to another, infer credentials or services, add unsupported review/rating claims, or treat external media links as hosted videos without complete supporting metadata.

The sitemap currently contains eight canonical URLs. Its `<lastmod>` values are editorial signals; do not update them mechanically for comment-only or technical work. `robots.txt` permits the public site, excludes query URLs containing `s=`, and declares the production sitemap.

## Contact and medical content

Contact information is duplicated by design across visible content, `tel:`/`mailto:`/map links, metadata, and JSON-LD. Search the entire repository and verify the authoritative value before changing an address, phone number, email address, hours, physician name, title, or credential. Keep each clinic's fields associated with the correct location.

Legacy source material, physician-reviewed website copy, technical modification dates, and genuine medical-review dates are different concepts. Do not present source material as reviewed copy, change a review date after a technical edit, or strengthen cautious medical language. Public content must remain neutral, educational, medically responsible, and non-promotional. Material medical revisions require physician review.

## JavaScript contracts

The following selectors and state values are functional contracts, even when they also have styling rules:

- `.navlinks`, `.navlinks .links`, `#menuToggle`, `.open`, and `.active` control the responsive navigation.
- `#procSearch`, `#resultCount`, `.proc-section`, `.proc-grid`, `.proc-card`, `.proc-title`, `.proc-desc`, `.hl`, `.is-hidden`, and `data-hidden` control procedure filtering and highlighting.
- `#year` receives the current year.
- `#lastUpdated` receives a machine-readable `datetime`; its visible text remains authored in HTML.

Do not rename or remove these hooks without updating and testing HTML, CSS, and JavaScript together. The search temporarily replaces the title and description elements' `innerHTML` with escaped, highlighted versions derived from their original text. Preserve those elements as text-only content unless that behavior is deliberately redesigned.

The navigation closes on its toggle, Escape, outside clicks, link activation, and resize above the JavaScript threshold. Keep `aria-expanded` synchronized with the `.open` class. The implementation does not currently move focus or return it when the menu closes; treat any future focus-management change as a behavior change requiring dedicated accessibility testing.

## CSS, themes, and responsive behavior

`styles.css` defines the shared color and layout variables in `:root` and overrides color variables for `prefers-color-scheme: light`. New styles should use the existing tokens instead of raw colors where an appropriate token exists. Preserve the 60–30–10 division documented in the stylesheet: foundation/background and text, surfaces, then restrained brand/accent use.

Responsive behavior is distributed across several content-driven breakpoints rather than one device taxonomy. When layout-affecting work is requested, check representative widths around 1440, 1280, 1024, 768, 640, and 360 pixels, as well as the actual breakpoints near the affected component. Check both color schemes, long Greek text, navigation wrapping, touch targets, focus visibility, image proportions, and horizontal overflow.

Accessibility is functional correctness. Preserve semantic links and buttons, heading order, labels, alternative text, keyboard activation, visible focus, ARIA state relationships, and the `prefers-reduced-motion` rules. JavaScript-disabled pages must retain their primary content and navigation.

## Assets and performance

Assets are served from `photos/`. Keep filenames and paths stable unless every HTML, metadata, sitemap, and CSS reference is updated together. Preserve explicit image dimensions and lazy loading for below-the-fold images; do not lazy-load the genuine LCP image blindly. The Google verification file at the repository root is infrastructure, not an ordinary content page.

No dependency or build configuration exists. Do not add a framework, documentation generator, formatter, analytics script, external asset, or third-party widget as incidental maintenance.

## Safe preview and validation

For a local file-based preview, start a basic server from the repository root:

```powershell
python -m http.server 8000
```

Use `.html` paths locally because this server does not reproduce Apache rewrites. For markup or style changes, manually check representative pages in dark and light mode at 1440, 1280, 1024, 768, 640, and 360 pixels. Verify keyboard navigation, Escape behavior, procedure search, focus visibility, contact links, images, and the browser console.

Useful repository checks that require no new dependency include:

```powershell
git diff --check
git diff -- AGENTS.md CODEX_GUARDRAILS.md
rg -n 'href="[^"]+\.html' -g '*.html'
rg -n 'https?://(www\.)?theofanispapadopoulos\.gr' -g '*.html' -g '*.xml' -g '*.txt'
rg -n 'procSearch|proc-title|proc-desc|menuToggle|lastUpdated' -g '*.html' -g '*.js' -g '*.css'
```

The `.html`-link search should be reviewed rather than blindly replaced: local or verification references may be intentional. Parse every JSON-LD block as JSON, confirm one canonical per indexable page, compare each canonical with `og:url`, inspect breadcrumb agreement, and confirm that the sitemap contains only canonical pages.

Production routing requires tests against the deployed host or an equivalent Apache configuration. For each public page, check the canonical URL plus HTTP, `www`, `.html`, trailing-slash, and direct-refresh variants. Record status codes, redirect chains, and the final URL. Do not claim those checks from a local static server.

## Deployment

The documentation previously identified cPanel hosting, but this checkout contains no deployment script, CI workflow, server configuration, or authoritative upload procedure. Before deployment, obtain the hosting instructions and deployed rewrite configuration from the site owner. Uploading only these files without preserving server rules may break canonical routes, redirects, and query noindex behavior.
