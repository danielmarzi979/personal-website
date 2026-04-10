# EDILMERC - Guida Deploy Online

## Server Locale Attivo

Il sito web EDILMERC è ora disponibile localmente su:
- **HTTP Server**: http://localhost:8000 (file statici)
- **Flask Server**: http://localhost:5000 (con API dati)

## Opzioni per Condivisione Online

### 1. NGROK (Consigliato per test rapidi)

```bash
# Installa ngrok
# Scarica da https://ngrok.com/download

# Avvia tunnel per server Flask
ngrok http 5000

# Oppure per server HTTP statico
ngrok http 8000
```

NGROK ti darà un URL pubblico tipo: `https://random-string.ngrok.io`

### 2. Cloudflare Tunnel (Alternativa gratuita)

```bash
# Installa cloudflared
# Scarica da https://github.com/cloudflare/cloudflared/releases

# Avvia tunnel
cloudflared tunnel --url http://localhost:5000
```

### 3. Vercel/Netlify (Deploy statico professionale)

**Per Vercel:**
1. Installa Vercel CLI: `npm i -g vercel`
2. Esegui: `vercel`
3. Segui le istruzioni

**Per Netlify:**
1. Crea account su https://netlify.com
2. Trascina la cartella del progetto
3. Il sito sarà online in pochi minuti

### 4. PythonAnywhere (Hosting Python)

1. Crea account gratuito su https://pythonanywhere.com
2. Carica i file del progetto
3. Configura web app con Flask
4. Avvia il server

## Struttura File

```
personal-website/
|-- index.html          # Pagina principale
|-- styles.css          # Stili CSS
|-- script.js           # JavaScript frontend
|-- app.py              # Server Flask
|-- requirements.txt    # Dipendenze Python
|-- templates/          # Template Flask
|   |-- index.html
|-- dati_reali_edilmerc.json  # Dati (opzionale)
```

## Funzionalità Disponibili

- **Dashboard KPI**: Cantieri attivi, attestati validi
- **Gestione Cantieri**: Lista e stato cantieri
- **Attestati Sicurezza**: Monitoraggio scadenze
- **Collaboratori**: Anagrafica lavoratori
- **Registro Documenti**: Tracciamento operazioni
- **Design Responsivo**: Funziona su mobile/desktop

## Accesso Condiviso

Una volta attivato uno dei servizi sopra (NGROG, Cloudflare, etc), riceverai:
- URL pubblico es: `https://abc123.ngrok.io`
- Link condivisibile con chiunque
- Accesso da qualsiasi dispositivo con internet

## Note Tecniche

- Il server Flask è configurato per accettare connessioni da qualsiasi IP (`0.0.0.0`)
- I dati vengono forniti tramite API REST in formato JSON
- Il sito è completamente responsive e funzionante
- Non richiede database per funzionamento base

## Supporto

Per problemi tecnici:
- Verifica che le porte 5000/8000 siano libere
- Controlla il firewall Windows
- Assicurati che Python sia installato correttamente
