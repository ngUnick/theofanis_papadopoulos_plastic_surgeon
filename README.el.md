# Θεοφάνης Παπαδόπουλος — Πλαστικός Χειρουργός (Ενημερωτική Ιστοσελίδα)

Γρήγορος, προσβάσιμος, στατικός ιστότοπος για πλαστικό χειρουργό στη Θεσσαλονίκη. Έμφαση στη σαφή ενημέρωση, στο καλό UX και στα Core Web Vitals.

> English version: see **[README.md](./README.md)**.

---

## Γενικές Πληροφορίες
- **Ιατρός:** Δρ. Θεοφάνης Παπαδόπουλος, Πλαστικός Χειρουργός (Θεσσαλονίκη).
- **Σκοπός:** Καθαρά, εκπαιδευτικά κείμενα για επεμβάσεις/μη επεμβατικές θεραπείες, τοποθεσίες ιατρείων και στοιχεία επικοινωνίας.
- **Σημείωση:** Το περιεχόμενο είναι ενημερωτικό (χωρίς προωθητικές πρακτικές). Κάθε ιατρική σελίδα περιλαμβάνει «Κίνδυνοι & Επιπλοκές», «Εναλλακτικές» και «Τελευταία ενημέρωση».

---

## Τεχνική Επισκόπηση

### Stack
- **Static** HTML/CSS/JS (χωρίς framework) για απλότητα και ταχύτητα
- **Hosting:** cPanel
- **SEO:** `sitemap.xml`, `robots.txt`
- **Προσβασιμότητα:** WCAG-AA αντίθεση, ορατό focus, reduced-motion, alt texts
- **Core Web Vitals:** προτεραιοποίηση LCP, `defer` σε scripts, λιτό CSS

### Δομή Έργου
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

```

### Sitemap & robots

**robots.txt**
```

User-agent: *
Allow: /

Sitemap: [https://theofanispapadopoulos.gr/sitemap.xml](https://theofanispapadopoulos.gr/sitemap.xml)

````

**sitemap.xml** (μικρό παράδειγμα)
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
````

### Προσβασιμότητα & UX

* Ορατός δακτύλιος focus
* Σταθερή αντίθεση χρωμάτων (WCAG-AA)
* Alt στις εικόνες
* `prefers-reduced-motion`

### Σημειώσεις Απόδοσης

* `defer` για μη κρίσιμη JS
* Lazy-load σε όλες τις μη-LCP εικόνες

---

## Contributing

PRs για βελτιώσεις προσβασιμότητας, CWV και SEO είναι ευπρόσδεκτα. Κρατάμε το περιεχόμενο καθαρά ενημερωτικό.

## License

Κώδικας: MIT.
Κείμενα/εικόνες: © αντίστοιχοι δημιουργοί (βλ. `LICENSE` / σημειώσεις).

```
