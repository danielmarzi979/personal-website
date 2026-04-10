#!/usr/bin/env python3
"""
EDILMERC - Server Web Flask per deploy online
Permette di condividere il sito web tramite link accessibile
"""

from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configurazione
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    """Pagina principale del sito EDILMERC"""
    return render_template('index.html')

@app.route('/dati_reali_edilmerc.json')
def get_dati_reali():
    """Fornisce i dati reali per il sito web"""
    try:
        # Se esiste un file JSON reali, lo carica
        if os.path.exists('dati_reali_edilmerc.json'):
            with open('dati_reali_edilmerc.json', 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        else:
            # Altrimenti restituisce dati di esempio
            dati_esempio = {
                "cantieri": [
                    {
                        "id": "CANT-2026-001",
                        "nome": "Ristrutturazione Edificio Residenziale",
                        "committente": "Mario Rossi",
                        "indirizzo": "Via G. Venturi 43, Bibbiano (RE)",
                        "direttoreLavori": "Ing. Bianchi",
                        "nLavoratori": 8,
                        "dataInizio": "2026-01-15",
                        "dataFine": "2026-04-30",
                        "stato": "in_corso"
                    },
                    {
                        "id": "CANT-2026-002",
                        "nome": "Ristrutturazione Ufficio Commerciale",
                        "committente": "SRL Costruzioni",
                        "indirizzo": "Via Emilia 102, Reggio Emilia",
                        "direttoreLavori": "Ing. Verdi",
                        "nLavoratori": 5,
                        "dataInizio": "2026-02-01",
                        "dataFine": "2026-03-15",
                        "stato": "in_corso"
                    }
                ],
                "attestati": [
                    {
                        "id": "ATT-001",
                        "lavoratore": "Mario Bianchi",
                        "tipo": "Lavoro a Quota",
                        "rilascio": "2025-01-15",
                        "scadenza": "2028-01-15",
                        "stato": "valido"
                    },
                    {
                        "id": "ATT-002",
                        "lavoratore": "Giuseppe Rossi",
                        "tipo": "Prevenzione Incendi",
                        "rilascio": "2025-03-10",
                        "scadenza": "2028-03-10",
                        "stato": "valido"
                    }
                ],
                "collaboratori": [
                    {
                        "id": "COL-001",
                        "nome": "Mario Bianchi",
                        "mansione": "Muratore",
                        "dataInizio": "2024-01-15",
                        "stato": "attivo"
                    },
                    {
                        "id": "COL-002",
                        "nome": "Giuseppe Rossi",
                        "mansione": "Elettricista",
                        "dataInizio": "2024-02-01",
                        "stato": "attivo"
                    }
                ],
                "registro": [
                    {
                        "id": "REG-001",
                        "data": "2026-04-10",
                        "operazione": "Nuovo attestato aggiunto",
                        "dettagli": "Lavoro a Quota - Mario Bianchi"
                    },
                    {
                        "id": "REG-002",
                        "data": "2026-04-09",
                        "operazione": "Nuovo cantiere creato",
                        "dettagli": "Ristrutturazione Ufficio Commerciale"
                    }
                ]
            }
            return jsonify(dati_esempio)
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve file statici (CSS, JS, immagini)"""
    return send_from_directory('.', filename)

@app.route('/health')
def health_check():
    """Health check per monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "EDILMERC Web Server"
    })

if __name__ == '__main__':
    print("Avvio server EDILMERC...")
    print("Sito web disponibile su: http://localhost:5000")
    print("Per accesso online, usa servizi come:")
    print("- ngrok: ngrok http 5000")
    print("- cloudflare: cloudflared tunnel --url http://localhost:5000")
    print("- Vercel/Netlify per deploy statico")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
