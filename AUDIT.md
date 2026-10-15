# Audit sito personale — Lorenzo Gravina

Data: 15 ottobre 2026 · Versione analizzata: `lograz/sito-personale` (main) · Testato in locale su desktop 1440px e mobile 390px.

## In sintesi

Il sito ha un'identità riconoscibile (lime + blu notte, griglia a card, monogramma) e la nomination Awwwards/CSS Winner dà credibilità. Il problema è che **non racconta il designer che sei oggi**: dieci anni di esperienza, clienti come Bulgari, Enel, Sisal, Poligrafico e Zecca dello Stato e la guida di un team di designer non compaiono da nessuna parte nella home. I progetti sono gallerie di schermate senza processo, e chi arriva dal LinkedIn di un'azienda non capisce in 10 secondi perché dovrebbe scriverti.

## Priorità alta

| # | Problema | Dove | Perché conta | Fix |
|---|---|---|---|---|
| 1 | Il contenuto è nascosto finché il JS non gira (`.hidden` + timeout 500ms) e ScrollReveal con `reset: true` rifà sparire le card a ogni scroll | tutte le pagine | Senza JS o con JS lento la pagina è vuota; l'animazione ripetuta stanca e penalizza LCP | Contenuto visibile di default, una sola animazione d'ingresso, rispetto di `prefers-reduced-motion` |
| 2 | Le icone sono una font-ligature: se il font Material non carica si legge `arrow_forward` dentro ogni bottone | tutte | Succede su reti lente e con blocker: rompe ogni CTA | SVG inline |
| 3 | Clienti e seniority assenti: Bulgari, Enel, Sisal, Q8, CNHI, Aviva, Poligrafico sono solo nel PDF | home | È l'argomento più forte che hai e nessuno lo vede | Riga clienti sotto l'hero + esperienza dal 2016 |
| 4 | Case study = descrizione generica + screenshot | pagine progetto | Recruiter e clienti valutano il *come* (problema, ruolo, decisioni, risultato), non solo il risultato visivo | Struttura fissa: contesto, ruolo, cosa ho fatto, risultato — vedi "Contenuti da completare" |
| 5 | Link rotti: "Vai al Figma" di Geeba ha `href=""`, MegaApp ha `href="#"` | geeba.html, megaapp.html | Un CTA che non porta da nessuna parte toglie fiducia | Link reale o rimozione del bottone |
| 6 | Peso: foto profilo 1,6 MB, cover SM 1,4 MB, repo 40 MB, video 5 MB in autoplay con audio | img/ | Mobile lento, LCP alto | WebP ridimensionati (−90%), video muto, lazy e `preload="none"` |

## Priorità media — UX/UI

- **Gerarchia**: nella home non c'è un `h1`; la frase di presentazione è un `h2` e le competenze sono `h4`. Su mobile la frase occupa tutto lo schermo e nasconde il resto.
- **Tutto è una card uguale**: stesso raggio, stesso colore, stesso badge lime. Il progetto in evidenza, il CV e il contatto hanno lo stesso peso visivo delle competenze, quindi niente spicca.
- **Il CTA principale è debole**: "Conosciamoci!" è l'ultima card in basso, su un'immagine rumorosa (contrasto testo basso). Non c'è un'email visibile né un contatto nell'header.
- **Navigazione**: niente header/menu; nelle pagine progetto "Torna alla home" è l'unica uscita. "Next project" esiste ma non c'è un "precedente" né l'elenco.
- **Hover ovunque**: ogni card si rimpicciolisce all'hover (scale 0.98) e quelle "chi sono/competenze" si illuminano: l'effetto perde significato perché non distingue ciò che è cliccabile da ciò che non lo è (le card competenze non sono link).
- **Accessibilità**: 30 immagini con `alt=""`, focus da tastiera non visibile, link senza testo accessibile (solo icona), `lang="en"` su un sito in italiano.
- **Mobile**: la card "Ultimo progetto" usa un'immagine diversa da desktop via CSS; i bottoni-freccia si sovrappongono ai titoli lunghi.

## Contenuti

- Bio generica ("designer creativo con una passione per...") che potrebbe essere di chiunque. Meglio dire cosa fai, per chi e da quanto.
- Refusi e incoerenze: "PROGETTi", "Nominee Awwards" (è Awwwards), "Ciao! sono", `</span>` orfano, mix IT/EN ("next project", "Designed and Developed by me").
- Kimbo e MegaApp sono proposte di restyling non commissionate: va bene mostrarle, ma etichettale come *concept* — un selezionatore apprezza l'onestà, e i lavori reali (System Management, Geeba) guadagnano peso.
- Le descrizioni di Kimbo e MegaApp sono quasi identiche parola per parola.
- Manca un percorso: Maidiremedia (2014–15) → System Management (2016–oggi), da designer a Senior che coordina il team.

## SEO e tecnico

- Stessi `title`, `og:title` e `og:description` su tutte le pagine; nessuna `meta description`.
- Nessun dato strutturato (`Person`), nessuna sitemap.
- File duplicati: `style.css` in root identico a `css/style.css`, CV presente due volte; file con spazio nel nome (`img/geeba/ cover.png`).
- Footer duplicato: web component con Shadow DOM in home, HTML copiato nelle pagine progetto.
- README con struttura di cartelle e URL di clone errati.

## Contenuti da completare (solo tu puoi farlo)

Per ogni progetto aggiungi in `data/projects.json` i campi già previsti:

1. **Il tuo ruolo preciso** (es. "Lead designer, team di 3", "Design + sviluppo WordPress").
2. **Il problema** in una frase, con il punto di vista dell'utente.
3. **Un risultato misurabile o una conseguenza concreta** (adozione interna di Geeba, tempi di timbratura, numero di pagine, nomination…).
4. Il **link Figma** di Geeba e MegaApp, se condivisibili.
5. Un progetto recente (2025–2026): l'ultimo case study è del 2024.

I campi vuoti non vengono mostrati, quindi il sito resta pulito finché non li riempi.

## Verifica di accessibilità della nuova versione (15 ottobre 2026)

Controllo automatico con axe-core (regole WCAG 2.0/2.1/2.2 A e AA + best practice) su tutte e 6 le pagine, a 1440px e 390px, più controlli manuali.

- **Violazioni axe: 0** dopo le correzioni. L'unica trovata (logo-link senza nome accessibile su mobile) è stata risolta con un `aria-label`.
- **Contrasto colori** (WCAG 1.4.3): testo principale 16,9:1, testo secondario 7,4:1 su bianco e 6,7:1 sulle superfici grigie, testo sul lime 10,7:1. Tutto supera il livello AAA. Il lime non è mai usato come colore del testo, perché su bianco arriva solo a 1,6:1: resta un colore di superficie per bottoni, badge e il blocco contatti.
- **Tastiera**: ordine di tabulazione logico, link "Vai al contenuto" come primo elemento, focus sempre visibile con un contorno scuro. Nella lista lavori il focus cambia anche l'anteprima, come l'hover. L'header fisso non copre l'elemento a fuoco (`scroll-padding-top`).
- **Struttura**: un solo `h1` per pagina, titoli in ordine, `lang="it"`, landmark `header`/`nav`/`main`/`footer`, testo alternativo su ogni immagine.
- **Reflow**: nessuno scroll orizzontale a 320px (equivalente a zoom 400%).
- **Movimento**: animazione d'ingresso unica, disattivata con `prefers-reduced-motion`; il punto "disponibile" pulsa 3 volte e si ferma.
- **Video**: senza audio, con controlli, non parte da solo. Non servono sottotitoli.
- **Contatti**: il link email apre il programma di posta; accanto c'è "Copia indirizzo", perché chi non ha un client configurato altrimenti resterebbe bloccato. L'esito della copia è annunciato agli screen reader.

Da verificare a mano dopo la pubblicazione: lettura con VoiceOver/NVDA e navigazione con zoom del browser al 200%.
