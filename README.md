# Lorenzo Gravina — portfolio

Sito personale statico: HTML, CSS e JavaScript senza dipendenze. Online su [lorenzogravina.vercel.app](https://lorenzogravina.vercel.app/).

## Struttura

```
index.html              home (generata)
<progetto>.html         case study (generati)
data/projects.json      contenuti dei progetti: si modifica qui
build.py                genera le pagine da projects.json
css/site.css            stile (token colore in :root)
css/fonts.css           font self-hosted (Bricolage Grotesque, Instrument Sans)
js/site.js              interazioni: ingresso, anteprima lavori, copia email
img/                    immagini in WebP
AUDIT.md                audit UX/UI e contenuti del vecchio sito
```

## Aggiungere o modificare un progetto

1. Metti le immagini in `img/work/<slug>/` (WebP, 1600px per cover e schermate desktop, 630px per schermate mobile).
2. Aggiungi o modifica l'oggetto in `data/projects.json`. I campi `problem`, `outcome`, `link` e `recognition` sono facoltativi: se vuoti non vengono mostrati.
3. Lancia `python3 build.py` e committa le pagine generate.

## In locale

```bash
python3 -m http.server 8000
```

Poi apri http://localhost:8000.

## Contatti

gravinalrn@gmail.com · [LinkedIn](https://www.linkedin.com/in/lorenzo-gravina-a4175037/)
