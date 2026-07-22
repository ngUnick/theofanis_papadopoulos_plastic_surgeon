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

Τα canonical URLs χρησιμοποιούν HTTPS, apex domain, διαδρομές χωρίς `.html` και χωρίς τελική κάθετο, εκτός από την αρχική σελίδα. Το αποθετήριο δεν περιέχει το production Apache configuration ή tracked αρχείο `.htaccess`, επομένως τα production clean-URL redirects δεν μπορούν να επαληθευτούν μόνο από αυτό το checkout. Ο helper τοπικής προεπισκόπησης αναπαράγει μόνο το extensionless-to-HTML mapping.

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
.\preview-site.cmd
```

Εναλλακτικά, εκτελέστε απευθείας τον server προεπισκόπησης του έργου:

```powershell
py tools/serve_local.py 8000
```

Ανοίξτε το `http://localhost:8000/`. Μη χρησιμοποιείτε `python -m http.server`: ο βασικός server της Python επιστρέφει `404` για τις καθαρές nested διαδρομές των οδηγών. Ο server του έργου αντιστοιχίζει σωστά τις extensionless διαδρομές στα αντίστοιχα HTML αρχεία. Δεν προσομοιώνει HTTPS, host canonicalization, redirects από `.html` ή redirects τελικής καθέτου· αυτά πρέπει να ελέγχονται στον Apache. Μην προσθέσετε client-side routing ή fallback προς το `index.html`.

## Συντήρηση

Οι αλλαγές routes πρέπει να συγχρονίζουν server redirects, canonical και Open Graph URLs, εσωτερικούς συνδέσμους, breadcrumbs, JSON-LD, `sitemap.xml` και, όπου χρειάζεται, `robots.txt`. Τα στοιχεία επικοινωνίας πρέπει επίσης να συμφωνούν στο ορατό κείμενο, στα links, στα metadata και στο structured data.

Το ιατρικό περιεχόμενο πρέπει να παραμένει ουδέτερο, εκπαιδευτικό και μη προωθητικό. Μια τεχνική αλλαγή δεν δικαιολογεί αλλαγή ημερομηνίας ιατρικής ανασκόπησης. Νέες ή ουσιωδώς τροποποιημένες ιατρικές διατυπώσεις απαιτούν έλεγχο από τον ιατρό.

Για selectors, themes, responsive και accessibility απαιτήσεις, deployment περιορισμούς και regression checks, δείτε το [docs/MAINTENANCE.md](./docs/MAINTENANCE.md).

## Άδεια χρήσης

Δεν υπάρχει αρχείο `LICENSE` στο αποθετήριο. Μην θεωρείτε ότι ο κώδικας, τα κείμενα ή οι εικόνες επιτρέπεται να αναδιανεμηθούν χωρίς επιβεβαίωση της ιδιοκτησίας και των δικαιωμάτων από τον υπεύθυνο της ιστοσελίδας.
