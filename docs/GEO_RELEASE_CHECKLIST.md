# GEO and medical-content release checklist

This package is a local draft until every hard gate below is recorded as passed. The site owner manages physician approval and performs the production upload.

## 1. Medical and editorial gate

- [ ] Open the private workbook `Theofanis-Papadopoulos-Medical-Evidence-and-GEO-Monitoring.xlsx`.
- [ ] A physician has reviewed every row in **Catalogue Audit** and **Claim Evidence**.
- [ ] Every disposition is no longer `Pending`; rejected or amended wording has been reflected in the HTML.
- [ ] The five guides, the 41-card source catalogue plus the separated service row, and the FAQ have been checked together.
- [ ] No testimonial, price, offer, guarantee, urgency, superiority claim, reviewer byline, public reference list, or technical update date is present.
- [ ] Contact, credential, emergency-routing, privacy, and licensed-clinical-setting wording is factually current.

## 2. Local technical gate

- [ ] Run `python tools/serve_local.py 8000` using an available Python runtime.
- [ ] Open all eight established pages, five nested guide URLs, `/privacy`, and `/image-credits` directly.
- [ ] Run the repository regression checks and retain their output with the release record.
- [ ] Confirm keyboard navigation, focus visibility, headings, landmarks, contents links, alternative text, contrast, and no horizontal overflow.
- [ ] Check dark and light schemes at 1440, 1280, 1024, 768, 640, and 360 pixels.
- [ ] Check current Chrome, Firefox, Edge, and Safari plus representative iPhone and Android widths.
- [ ] Run mobile Lighthouse on every public template; all four categories must score at least 90.
- [ ] Confirm that canonical URLs, Open Graph URLs, breadcrumbs, allowed JSON-LD types, internal links, sitemap membership, and `noindex` pages agree.

## 3. Hosting, privacy, and backup gate

- [ ] In cPanel, set archived raw access-log retention to 14 days.
- [ ] Ask the host to disable AWStats and Webalizer processing. If it cannot be disabled, record the host response and update `/privacy` before release so it states the actual limitation.
- [ ] Confirm that no analytics, forms, non-essential cookies, or cookie banner has been introduced.
- [ ] Record the exact commit intended for release.
- [ ] Create an annotated Git pre-release tag only after approval, for example `geo-medical-prerelease-YYYY-MM-DD`.
- [ ] Create and verify a complete cPanel backup immediately before upload. Record its filename, time, and restore path.

## 4. Coordinated upload

- [ ] Upload the approved HTML, CSS, JavaScript, images, `.htaccess`, `robots.txt`, and `sitemap.xml` as one release.
- [ ] Do not upload the private evidence workbook, source archive, screenshots, or monitoring folders.
- [ ] Purge the provider nginx cache after upload.
- [ ] Confirm that Apache still reads `.htaccess` and that nginx is not serving stale redirects or metadata.

## 5. Production smoke tests

- [ ] Every canonical URL returns `200`.
- [ ] Representative HTTP, `www`, root `.html`, flat guide-source `.html`, and trailing-slash variants reach the canonical URL in one `301` hop while preserving query strings.
- [ ] Invalid routes return `404`; collection routes such as `/procedures` remain unchanged.
- [ ] Page source contains the approved canonical, metadata, and JSON-LD—not a cached predecessor.
- [ ] `robots.txt`, `sitemap.xml`, `/privacy`, and `/image-credits` return the intended content.
- [ ] Map and YouTube links open as ordinary outbound links; no iframe or remote thumbnail is loaded.
- [ ] Core navigation, treatment search, mobile menu, guide contents links, and contact links work.

## 6. Google Search Console actions

- [ ] Resubmit `https://theofanispapadopoulos.gr/sitemap.xml`.
- [ ] Remove the obsolete 2012 `http://www` sitemap submission.
- [ ] Validate resolution of the five crawled-but-not-indexed `.html` duplicates.
- [ ] Inspect and, where appropriate, request indexing for each of the five guide URLs.
- [ ] Record screenshots and dates. Do not use Bing Webmaster Tools for this release.

## Rollback rule

Rollback from the recorded cPanel backup and Git tag if canonical routing, medical approval, privacy accuracy, indexability, or core navigation fails. Purge nginx again after restoration and repeat the smoke tests. Performance or cosmetic defects that do not cross a hard gate should still be logged and triaged, not hidden.
