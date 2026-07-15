# Θεοφάνης Παπαδόπουλος — ενημερωτική ιατρική ιστοσελίδα

Το αποθετήριο περιέχει τον πηγαίο κώδικα μιας ελληνόφωνης, στατικής ιστοσελίδας πολλαπλών σελίδων για τον πλαστικό χειρουργό Θεοφάνη Παπαδόπουλο. Χρησιμοποιεί απλό HTML, CSS και JavaScript, χωρίς framework, package manager, build step, templates ή client-side router.

Πριν από οποιαδήποτε αλλαγή, διαβάστε τα [AGENTS.md](./AGENTS.md) και [CODEX_GUARDRAILS.md](./CODEX_GUARDRAILS.md). Η αναλυτική τεχνική τεκμηρίωση βρίσκεται στο [docs/MAINTENANCE.md](./docs/MAINTENANCE.md). Η αγγλική επισκόπηση βρίσκεται στο [README.md](./README.md).

## Δημόσιες σελίδες

| Αρχείο | Κανονικό δημόσιο URL |
| --- | --- |
| `index.html` | `https://theofanispapadopoulos.gr/` |
| `about.html` | `https://theofanispapadopoulos.gr/about` |
| `procedures.html` | `https://theofanispapadopoulos.gr/procedures` |
| `non-invasive.html` | `https://theofanispapadopoulos.gr/non-invasive` |
| `reconstructive.html` | `https://theofanispapadopoulos.gr/reconstructive` |
| `media.html` | `https://theofanispapadopoulos.gr/media` |
| `faq.html` | `https://theofanispapadopoulos.gr/faq` |
| `contact.html` | `https://theofanispapadopoulos.gr/contact` |

Τα canonical URLs χρησιμοποιούν HTTPS, apex domain, διαδρομές χωρίς `.html` και χωρίς τελική κάθετο, εκτός από την αρχική σελίδα. Το αποθετήριο δεν περιέχει το production Apache configuration ή αρχείο `.htaccess`. Επομένως, τα redirects και rewrites των clean URLs δεν μπορούν να αναπαραχθούν ή να επαληθευτούν μόνο από αυτό το checkout.

## Δομή

- Τα οκτώ αρχεία HTML είναι ανεξάρτητα έγγραφα και αποτελούν την πηγή αλήθειας για το ορατό περιεχόμενο, τα metadata, τα breadcrumbs και το page-specific JSON-LD.
- Το `styles.css` περιέχει design tokens, dark/light themes, layout, responsive κανόνες και accessibility states.
- Το `script.js` προσθέτει προοδευτικά το mobile menu, την αναζήτηση επεμβάσεων και τα footer metadata.
- Ο φάκελος `photos/` περιέχει τα τοπικά assets.
- Τα `sitemap.xml` και `robots.txt` ορίζουν τα canonical URLs και τις οδηγίες crawling.
- Το `googlee2185726589adaa8.html` είναι αρχείο επαλήθευσης Google και πρέπει να διατηρεί ακριβώς το όνομα και το περιεχόμενό του.

## Τοπική προεπισκόπηση

Δεν απαιτείται εγκατάσταση. Από τη ρίζα του αποθετηρίου:

```powershell
python -m http.server 8000
```

Ανοίξτε το `http://localhost:8000/index.html`. Ο απλός Python server δεν εφαρμόζει τα production rewrites, οπότε στην τοπική προεπισκόπηση χρησιμοποιήστε τα `.html` filenames. Μην προσθέσετε client-side routing ή fallback προς το `index.html` για να προσομοιώσετε τα clean URLs.

## Συντήρηση

Οι αλλαγές routes πρέπει να συγχρονίζουν server redirects, canonical και Open Graph URLs, εσωτερικούς συνδέσμους, breadcrumbs, JSON-LD, `sitemap.xml` και, όπου χρειάζεται, `robots.txt`. Τα στοιχεία επικοινωνίας πρέπει επίσης να συμφωνούν στο ορατό κείμενο, στα links, στα metadata και στο structured data.

Το ιατρικό περιεχόμενο πρέπει να παραμένει ουδέτερο, εκπαιδευτικό και μη προωθητικό. Μια τεχνική αλλαγή δεν δικαιολογεί αλλαγή ημερομηνίας ιατρικής ανασκόπησης. Νέες ή ουσιωδώς τροποποιημένες ιατρικές διατυπώσεις απαιτούν έλεγχο από τον ιατρό.

Για selectors, themes, responsive και accessibility απαιτήσεις, deployment περιορισμούς και regression checks, δείτε το [docs/MAINTENANCE.md](./docs/MAINTENANCE.md).

## Άδεια χρήσης

Δεν υπάρχει αρχείο `LICENSE` στο αποθετήριο. Μην θεωρείτε ότι ο κώδικας, τα κείμενα ή οι εικόνες επιτρέπεται να αναδιανεμηθούν χωρίς επιβεβαίωση της ιδιοκτησίας και των δικαιωμάτων από τον υπεύθυνο της ιστοσελίδας.
