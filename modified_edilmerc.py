"""
EDILMERC 2026 - Gestionale Aziendale
Versione completa con: Dashboard KPI, Scadenze Attestati, Registro Documenti,
Stato Cantieri, Galleria Foto, Backup Automatico, Validazione Campi,
Tema Professionale, Gestione G:Drive offline.
"""

import streamlit as st
import os
import shutil
import json
import csv
import zipfile
import logging
from datetime import datetime, date, timedelta
from pathlib import Path

# ── Dipendenza opzionale ──────────────────────────────────────────────────────
try:
    from docxtpl import DocxTemplate
    DOCXTPL_OK = True
except ImportError:
    DOCXTPL_OK = False

try:
    from docx2pdf import convert as docx2pdf_convert
    DOCX2PDF_OK = True
except ImportError:
    DOCX2PDF_OK = False

# ── Configurazione pagina ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDILMERC 2026",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Tema personalizzato ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;900&family=Barlow+Condensed:wght@700;900&display=swap');

/* Variabili colore */
:root {
    --rosso-em:   #E02B2B;
    --arancio-em: #FF8C00;
    --bordeaux:    #8B0000;
    --arancio:   #FF8C00;
    --arancio-d: #E67E00;
    --nero:      #FFFFFF;
    --grigio-s:  #F5F5F5;
    --grigio-m:  #E8E8E8;
    --grigio-c:  #D0D0D0;
    --testo:     #8B0000;
    --testo-s:   #A0522D;
    --verde:     #27AE60;
    --giallo:    #F1C40F;
    --rosso:     #E02B2B;
    --blu:       #2980B9;
}

/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--nero) !important;
    color: var(--testo) !important;
    font-family: 'Barlow', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--grigio-s) !important;
    border-right: 2px solid var(--rosso-em);
}
[data-testid="stSidebar"] * { color: var(--testo) !important; }

/* Titoli */
h1 { font-family: 'Barlow Condensed', sans-serif; font-weight: 900; font-size: 2.4rem; color: var(--rosso-em) !important; letter-spacing: 0.04em; text-transform: uppercase; }
h2 { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; color: var(--rosso-em) !important; }
h3 { font-family: 'Barlow', sans-serif; font-weight: 600; color: var(--bordeaux) !important; }

/* Bottoni */
.stButton > button {
    background: var(--arancio) !important;
    color: var(--nero) !important;
    font-family: 'Barlow', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.45rem 1rem !important;
    transition: background 0.2s ease, transform 0.1s ease;
    letter-spacing: 0.03em;
}
.stButton > button:hover {
    background: var(--arancio-d) !important;
    transform: translateY(-1px);
}
.stButton > button:active { transform: translateY(0px); }

/* Bottone danger (Sì/Elimina) */
.btn-danger > button {
    background: var(--rosso) !important;
    color: white !important;
}
.btn-secondary > button {
    background: var(--grigio-c) !important;
    color: var(--testo) !important;
}

/* Input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input,
.stSelectbox > div > div {
    background: var(--grigio-m) !important;
    color: var(--testo) !important;
    border: 1px solid var(--grigio-c) !important;
    border-radius: 6px !important;
    font-family: 'Barlow', sans-serif;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--arancio) !important;
    box-shadow: 0 0 0 2px rgba(242,140,30,0.25) !important;
}

/* Label */
label { color: var(--testo-s) !important; font-size: 0.82rem !important; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }

/* Expander */
details {
    background: var(--grigio-m) !important;
    border: 1px solid var(--grigio-c) !important;
    border-radius: 8px !important;
    margin-bottom: 0.6rem;
}
summary { color: var(--arancio) !important; font-weight: 700; font-family: 'Barlow Condensed', sans-serif; font-size: 1.05rem; letter-spacing: 0.04em; }

/* Metric */
[data-testid="stMetricValue"] { color: var(--arancio) !important; font-family: 'Barlow Condensed', sans-serif; font-weight: 900; font-size: 2rem; }
[data-testid="stMetricLabel"] { color: var(--testo-s) !important; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricDelta"] { font-size: 0.8rem; }

/* Divider */
hr { border-color: var(--grigio-c) !important; margin: 1.2rem 0; }

/* Alert personalizzati */
.alert-box {
    padding: 0.8rem 1.1rem;
    border-radius: 8px;
    margin-bottom: 0.7rem;
    font-family: 'Barlow', sans-serif;
    font-size: 0.93rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.alert-rosso  { background: rgba(224,43,43,0.15);  border-left: 4px solid var(--rosso-em);  color: var(--rosso-em); }
.alert-giallo { background: rgba(241,196,15,0.12); border-left: 4px solid var(--giallo); color: #F39C12; }
.alert-verde  { background: rgba(39,174,96,0.12);  border-left: 4px solid var(--verde);  color: #27AE60; }
.alert-blu    { background: rgba(41,128,185,0.12); border-left: 4px solid var(--blu);    color: #2980B9; }

/* Card cantiere */
.card-cantiere {
    background: var(--grigio-m);
    border: 1px solid var(--grigio-c);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

/* Badge stato */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-verde  { background: rgba(39,174,96,0.2);  color: #27AE60; border: 1px solid rgba(39,174,96,0.4); }
.badge-giallo { background: rgba(241,196,15,0.2); color: #F39C12; border: 1px solid rgba(241,196,15,0.4); }
.badge-rosso  { background: rgba(224,43,43,0.2);  color: var(--rosso-em); border: 1px solid rgba(224,43,43,0.4); }
.badge-grigio { background: rgba(139,0,0,0.2);color: var(--bordeaux); border: 1px solid rgba(139,0,0,0.4); }

/* Radio — POS / PiMUS ben visibili */
.stRadio > div { gap: 0.6rem; }
.stRadio > div > label {
    color: var(--testo) !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    background: var(--grigio-c) !important;
    padding: 0.35rem 1rem !important;
    border-radius: 6px !important;
    border: 1px solid #555 !important;
    cursor: pointer;
    transition: background 0.15s ease, border-color 0.15s ease;
}
.stRadio > div > label:hover {
    background: #B0B0B0 !important;
    border-color: var(--arancio) !important;
}
/* Opzione selezionata */
.stRadio > div [data-checked="true"] > div,
.stRadio > div > label[data-checked="true"] {
    background: var(--arancio) !important;
    color: var(--nero) !important;
    border-color: var(--arancio) !important;
}
/* Cerchietto radio — nascondilo, usiamo lo sfondo come indicatore */
.stRadio input[type="radio"] { accent-color: var(--arancio); }

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--grigio-m) !important;
    border: 1px dashed var(--grigio-c) !important;
    border-radius: 8px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--grigio-s); }
::-webkit-scrollbar-thumb { background: var(--grigio-c); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--rosso-em); }

/* Nasconde completamente sidebar e toggle */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

/* ── Tab fascicolo ── */
[data-testid="stTabsTabList"] {
    background: var(--grigio-s) !important;
    border-bottom: 3px solid var(--rosso-em) !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 0 0.5rem !important;
    gap: 0.1rem !important;
    overflow-x: auto;
}
[data-testid="stTabsTabList"] button[role="tab"] {
    background: var(--grigio-m) !important;
    color: var(--testo-s) !important;
    border: 1px solid var(--grigio-c) !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.3rem !important;
    margin-bottom: -3px !important;
    transition: background 0.15s ease, color 0.15s ease;
}
[data-testid="stTabsTabList"] button[role="tab"]:hover {
    background: var(--grigio-c) !important;
    color: var(--testo) !important;
}
[data-testid="stTabsTabList"] button[role="tab"][aria-selected="true"] {
    background: var(--arancio-em) !important;
    color: var(--nero) !important;
    border-color: var(--arancio-em) !important;
}
[data-testid="stTabsContent"] {
    background: var(--grigio-m) !important;
    border: 1px solid var(--grigio-c) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 1.5rem 1.5rem 2rem !important;
}

/* Nasconde la toolbar Streamlit */
[data-testid="stToolbar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Logging ───────────────────────────────────────────────────────────────────
def setup_logging(base_path: str):
    log_file = os.path.join(base_path, "edilmerc_errori.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

# ── Percorsi G:Drive ──────────────────────────────────────────────────────────
P_BASE      = r"G:\Il mio Drive\EdilMerc"
P_ATT       = os.path.join(P_BASE, "Attestati")
P_INFO      = os.path.join(P_BASE, "Info")
P_SICUREZZA = os.path.join(P_BASE, "Sicurezza_Cantieri")
P_BACKUP    = os.path.join(P_BASE, "_Backup")
P_REGISTRO  = os.path.join(P_BASE, "registro_documenti.csv")
P_SCADENZE  = os.path.join(P_BASE, "scadenze_attestati.json")

# ── Verifica disponibilità G:Drive ────────────────────────────────────────────
DRIVE_OK = os.path.exists(P_BASE)

if DRIVE_OK:
    setup_logging(P_BASE)
    for cartella in [P_ATT, P_INFO, P_SICUREZZA, P_BACKUP]:
        os.makedirs(cartella, exist_ok=True)

# ── Helper: alert HTML ────────────────────────────────────────────────────────
def alert(testo: str, tipo: str = "blu", icona: str = "ℹ️"):
    st.markdown(
        f'<div class="alert-box alert-{tipo}">{icona} {testo}</div>',
        unsafe_allow_html=True,
    )

def badge_html(testo: str, tipo: str) -> str:
    return f'<span class="badge badge-{tipo}">{testo}</span>'

# ── Helper: semaforo scadenza ─────────────────────────────────────────────────
def semaforo_scadenza(data_scad: date) -> tuple[str, str, str]:
    """Restituisce (colore_badge, testo_badge, tipo_alert) in base alla scadenza."""
    oggi = date.today()
    delta = (data_scad - oggi).days
    if delta < 0:
        return "rosso", "SCADUTO", "rosso"
    elif delta <= 30:
        return "giallo", f"Scade in {delta}g", "giallo"
    elif delta <= 90:
        return "giallo", f"Scade in {delta}g", "giallo"
    else:
        return "verde", f"OK ({delta}g)", "verde"

# ── Registro CSV ──────────────────────────────────────────────────────────────
REGISTRO_INTESTAZIONE = ["data", "ora", "cantiere", "tipo_doc", "nome_file", "operazione"]

def leggi_registro() -> list[dict]:
    if not os.path.exists(P_REGISTRO):
        return []
    try:
        with open(P_REGISTRO, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        logging.error(f"leggi_registro: {e}")
        return []

def scrivi_registro(cantiere: str, tipo_doc: str, nome_file: str, operazione: str = "Creazione"):
    try:
        esiste = os.path.exists(P_REGISTRO)
        with open(P_REGISTRO, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=REGISTRO_INTESTAZIONE)
            if not esiste:
                w.writeheader()
            w.writerow({
                "data": datetime.now().strftime("%d/%m/%Y"),
                "ora": datetime.now().strftime("%H:%M"),
                "cantiere": cantiere,
                "tipo_doc": tipo_doc,
                "nome_file": nome_file,
                "operazione": operazione,
            })
    except Exception as e:
        logging.error(f"scrivi_registro: {e}")

def aggiorna_sito_web():
    """Aggiorna automaticamente i dati del sito web"""
    try:
        # Esegui lo script di estrazione dati
        import subprocess
        import sys
        
        # Percorso dello script di estrazione
        script_path = os.path.join(os.path.dirname(__file__), "extract_data.py")
        
        # Esegui lo script in un subprocesso
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=os.path.dirname(script_path))
        
        if result.returncode == 0:
            logging.info("Dati del sito web aggiornati con successo")
        else:
            logging.error(f"Errore aggiornamento sito web: {result.stderr}")
            
    except Exception as e:
        logging.error(f"Errore durante aggiornamento sito web: {e}")

# Funzione per aggiornare il sito web
def aggiorna_sito_web():
    """Esegue extract_data.py per aggiornare i dati del sito"""
    try:
        import subprocess
        script_path = os.path.join(os.path.dirname(__file__), "extract_data.py")
        
        if os.path.exists(script_path):
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                st.success("Dati estratti con successo!")
                st.info("Carica i dati su GitHub con il pulsante 'Deploy Sito'")
            else:
                st.error(f"Errore nell'estrazione dati: {result.stderr}")
        else:
            st.error("Script extract_data.py non trovato")
            
    except Exception as e:
        st.error(f"Errore durante l'estrazione dati: {e}")

# Funzione per deploy automatico su GitHub
def deploy_sito_web():
    """Esegue il deploy automatico del sito su GitHub"""
    try:
        import subprocess
        script_path = os.path.join(os.path.dirname(__file__), "auto_deploy.py")
        
        if os.path.exists(script_path):
            with st.spinner("Deploy in corso... estrazione dati e caricamento su GitHub"):
                result = subprocess.run([sys.executable, script_path], 
                                      capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                st.success("Deploy completato con successo!")
                st.info("Il sito sarà aggiornato in 1-2 minuti")
                st.success("URL: https://danielmarzi979.github.io/personal-website")
            else:
                st.error(f"Errore nel deploy: {result.stderr}")
        else:
            st.error("Script auto_deploy.py non trovato")
            
    except Exception as e:
        st.error(f"Errore durante il deploy: {e}")

# ── Scadenze JSON ─────────────────────────────────────────────────────────────
def leggi_scadenze() -> dict:
    if not os.path.exists(P_SCADENZE):
        return {}
    try:
        with open(P_SCADENZE, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"leggi_scadenze: {e}")
        return {}

def salva_scadenze(dati: dict):
    try:
        with open(P_SCADENZE, "w", encoding="utf-8") as f:
            json.dump(dati, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"salva_scadenze: {e}")
        st.error(f"Errore salvataggio scadenze: {e}")

# ── Stato cantieri JSON ───────────────────────────────────────────────────────
def leggi_stato_cantiere(path_cartella: str) -> str:
    p = os.path.join(path_cartella, "stato.json")
    if not os.path.exists(p):
        return "in corso"
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("stato", "in corso")
    except Exception:
        return "in corso"

def salva_stato_cantiere(path_cartella: str, stato: str):
    p = os.path.join(path_cartella, "stato.json")
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"stato": stato, "aggiornato": datetime.now().isoformat()}, f)
    except Exception as e:
        logging.error(f"salva_stato_cantiere: {e}")

STATI_CANTIERE = ["in corso", "completato", "sospeso"]
STATO_BADGE    = {"in corso": "verde", "completato": "grigio", "sospeso": "giallo"}
STATO_ICONA    = {"in corso": "🟢", "completato": "✅", "sospeso": "⏸️"}

# ── Numerazione automatica cantieri ──────────────────────────────────────────
def genera_codice_cantiere() -> str:
    anno = datetime.now().year
    if not os.path.exists(P_SICUREZZA):
        return f"CANT-{anno}-001"
    esistenti = [
        d for d in os.listdir(P_SICUREZZA)
        if os.path.isdir(os.path.join(P_SICUREZZA, d)) and not d.startswith("Modello")
    ]
    progressivo = len(esistenti) + 1
    return f"CANT-{anno}-{progressivo:03d}"

# ── Apertura file ─────────────────────────────────────────────────────────────
def apri_doc(p: str):
    p = os.path.normpath(p)
    if os.path.exists(p):
        try:
            os.startfile(p)
        except Exception as e:
            logging.error(f"apri_doc: {e}")
            st.error(f"Errore apertura file: {e}")
    else:
        st.error(f"File non trovato: {p}")

# ── Eliminazione file ─────────────────────────────────────────────────────────
def elimina_file(p: str):
    try:
        os.remove(p)
        pulisci_cartelle_vuote()
        st.rerun()
    except Exception as e:
        logging.error(f"elimina_file: {e}")
        st.error(f"Errore eliminazione: {e}")

def pulisci_cartelle_vuote():
    if not os.path.exists(P_SICUREZZA):
        return
    for d in os.listdir(P_SICUREZZA):
        p_c = os.path.join(P_SICUREZZA, d)
        if os.path.isdir(p_c) and not d.startswith("Modello"):
            contenuto = [f for f in os.listdir(p_c) if f != "stato.json"]
            if not contenuto:
                try:
                    shutil.rmtree(p_c)
                except Exception:
                    pass

def rinomina_file_esistenti():
    """Rinomina i file esistenti per includere l'indirizzo del cantiere nel nome"""
    if not os.path.exists(P_SICUREZZA):
        return 0
    
    file_rinominati = 0
    
    for codice_cantiere in os.listdir(P_SICUREZZA):
        path_cantiere = os.path.join(P_SICUREZZA, codice_cantiere)
        
        if not os.path.isdir(path_cantiere) or codice_cantiere.startswith("Modello"):
            continue
            
        # Leggi i dati del cantiere dal file stato.json
        indirizzo = ""
        stato_file = os.path.join(path_cantiere, "stato.json")
        
        if os.path.exists(stato_file):
            try:
                with open(stato_file, 'r', encoding='utf-8') as f:
                    dati = json.load(f)
                    indirizzo = dati.get('indirizzo', '')
            except:
                pass
        
        if not indirizzo:
            continue  # Salta se non trovo l'indirizzo
        
        # Pulisci l'indirizzo per il nome file
        indirizzo_pulito = indirizzo.replace(" ", "_").replace(",", "").replace("/", "_")
        
        # Rinomina i file nella cartella
        for file in os.listdir(path_cantiere):
            if file.endswith(('.docx', '.pdf')) and not file.startswith('Modello'):
                vecchio_path = os.path.join(path_cantiere, file)
                
                # Estrai tipo documento dal nome file
                if file.startswith('POS_'):
                    tipo_doc = 'POS'
                elif file.startswith('PiMUS_'):
                    tipo_doc = 'PiMUS'
                elif file.startswith('DUVRI_'):
                    tipo_doc = 'DUVRI'
                else:
                    continue  # Salta file non riconosciuti
                
                # Crea nuovo nome
                vecchio_nome = os.path.splitext(file)[0]
                if '_' in vecchio_nome and len(vecchio_nome.split('_')) >= 2:
                    # Se ha già formato vecchio (tipo_codice), sostituisci
                    nuovo_nome = f"{tipo_doc}_{codice_cantiere}_{indirizzo_pulito}"
                else:
                    continue  # Formato non riconosciuto
                
                estensione = os.path.splitext(file)[1]
                nuovo_file = f"{nuovo_nome}{estensione}"
                nuovo_path = os.path.join(path_cantiere, nuovo_file)
                
                # Rinomina se il nuovo nome è diverso e non esiste già
                if vecchio_path != nuovo_path and not os.path.exists(nuovo_path):
                    try:
                        os.rename(vecchio_path, nuovo_path)
                        file_rinominati += 1
                        logging.info(f"File rinominato: {file} -> {nuovo_file}")
                        
                        # Aggiorna il registro
                        scrivi_registro(codice_cantiere, tipo_doc, nuovo_file, "Rinomina automatica")
                        
                    except Exception as e:
                        logging.error(f"Errore rinomina file {file}: {e}")
    
    return file_rinominati

def rinomina_file_manuale(codice_cantiere, nuovo_indirizzo):
    """Rinomina manualmente i file di un cantiere specifico"""
    path_cantiere = os.path.join(P_SICUREZZA, codice_cantiere)
    
    if not os.path.exists(path_cantiere):
        return 0, "Cantiere non trovato"
    
    file_rinominati = 0
    errori = []
    debug_info = []
    
    # DEBUG: Mostra tutti i file nella cartella
    tutti_i_file = os.listdir(path_cantiere)
    debug_info.append(f"File trovati in {codice_cantiere}: {tutti_i_file}")
    
    # Pulisci l'indirizzo per il nome file
    indirizzo_pulito = nuovo_indirizzo.replace(" ", "_").replace(",", "").replace("/", "_")
    debug_info.append(f"Indirizzo pulito: {indirizzo_pulito}")
    
    # Rinomina i file nella cartella
    for file in tutti_i_file:
        if file.endswith(('.docx', '.pdf')) and not file.startswith('Modello'):
            vecchio_path = os.path.join(path_cantiere, file)
            debug_info.append(f"Analizzo file: {file}")
            
            # Estrai tipo documento dal nome file
            if file.startswith('POS_'):
                tipo_doc = 'POS'
            elif file.startswith('PiMUS_'):
                tipo_doc = 'PiMUS'
            elif file.startswith('DUVRI_'):
                tipo_doc = 'DUVRI'
            else:
                debug_info.append(f"File {file} non riconosciuto (non inizia con POS_, PiMUS_ o DUVRI_)")
                continue  # Salta file non riconosciuti
            
            debug_info.append(f"Tipo documento rilevato: {tipo_doc}")
            
            # Crea nuovo nome
            vecchio_nome = os.path.splitext(file)[0]
            if '_' in vecchio_nome and len(vecchio_nome.split('_')) >= 2:
                # Se ha già formato vecchio (tipo_codice), sostituisci
                nuovo_nome = f"{tipo_doc}_{codice_cantiere}_{indirizzo_pulito}"
                debug_info.append(f"Nuovo nome calcolato: {nuovo_nome}")
            else:
                debug_info.append(f"File {file} formato non riconosciuto")
                continue  # Formato non riconosciuto
            
            estensione = os.path.splitext(file)[1]
            nuovo_file = f"{nuovo_nome}{estensione}"
            nuovo_path = os.path.join(path_cantiere, nuovo_file)
            
            debug_info.append(f"Confronto: {file} -> {nuovo_file}")
            
            # Rinomina se il nuovo nome è diverso
            if vecchio_path != nuovo_path:
                try:
                    os.rename(vecchio_path, nuovo_path)
                    file_rinominati += 1
                    debug_info.append(f"SUCCESSO: File rinominato: {file} -> {nuovo_file}")
                    logging.info(f"File rinominato: {file} -> {nuovo_file}")
                    
                    # Aggiorna il registro
                    scrivi_registro(codice_cantiere, tipo_doc, nuovo_file, "Rinomina manuale")
                    
                except Exception as e:
                    errore_msg = f"Errore rinomina {file}: {e}"
                    debug_info.append(f"ERRORE: {errore_msg}")
                    errori.append(errore_msg)
            else:
                debug_info.append(f"File {file} già ha il nome corretto")
    
    # Aggiorna il file stato.json con il nuovo indirizzo
    stato_file = os.path.join(path_cantiere, "stato.json")
    try:
        dati_stato = {}
        if os.path.exists(stato_file):
            with open(stato_file, 'r', encoding='utf-8') as f:
                dati_stato = json.load(f)
        
        dati_stato['indirizzo'] = nuovo_indirizzo
        
        with open(stato_file, 'w', encoding='utf-8') as f:
            json.dump(dati_stato, f, ensure_ascii=False, indent=2)
            
        debug_info.append("File stato.json aggiornato")
            
    except Exception as e:
        errore_msg = f"Errore aggiornamento stato.json: {e}"
        debug_info.append(f"ERRORE: {errore_msg}")
        errori.append(errore_msg)
    
    # Aggiungi info debug al risultato
    risultato_debug = " | ".join(debug_info)
    if file_rinominati == 0 and not errori:
        return 0, f"Nessun file rinominato. Debug: {risultato_debug}"
    
    return file_rinominati, f"{'; '.join(errori) if errori else 'Successo'} | Debug: {risultato_debug}"

def rinomina_file_manuale_con_selezione(codice_cantiere, nuovo_indirizzo, file_types):
    """Rinomina i file usando le selezioni manuali dei tipi di documento"""
    path_cantiere = os.path.join(P_SICUREZZA, codice_cantiere)
    
    if not os.path.exists(path_cantiere):
        return 0, "Cantiere non trovato"
    
    file_rinominati = 0
    errori = []
    debug_info = []
    
    # Pulisci l'indirizzo per il nome file
    indirizzo_pulito = nuovo_indirizzo.replace(" ", "_").replace(",", "").replace("/", "_")
    debug_info.append(f"Indirizzo pulito: {indirizzo_pulito}")
    
    # Rinomina i file nella cartella usando le selezioni manuali
    for file, tipo_selezionato in file_types.items():
        if tipo_selezionato == "Ignora":
            debug_info.append(f"File {file} ignorato dall'utente")
            continue
            
        vecchio_path = os.path.join(path_cantiere, file)
        debug_info.append(f"Processo file: {file} come {tipo_selezionato}")
        
        # Crea nuovo nome usando il tipo selezionato manualmente
        estensione = os.path.splitext(file)[1]
        nuovo_file = f"{tipo_selezionato}_{codice_cantiere}_{indirizzo_pulito}{estensione}"
        nuovo_path = os.path.join(path_cantiere, nuovo_file)
        
        debug_info.append(f"Confronto: {file} -> {nuovo_file}")
        
        # Rinomina se il nuovo nome è diverso
        if vecchio_path != nuovo_path:
            try:
                os.rename(vecchio_path, nuovo_path)
                file_rinominati += 1
                debug_info.append(f"SUCCESSO: File rinominato: {file} -> {nuovo_file}")
                logging.info(f"File rinominato: {file} -> {nuovo_file}")
                
                # Aggiorna il registro
                scrivi_registro(codice_cantiere, tipo_selezionato, nuovo_file, "Rinomina manuale")
                
            except Exception as e:
                errore_msg = f"Errore rinomina {file}: {e}"
                debug_info.append(f"ERRORE: {errore_msg}")
                errori.append(errore_msg)
        else:
            debug_info.append(f"File {file} già ha il nome corretto")
    
    # Aggiorna il file stato.json con il nuovo indirizzo
    stato_file = os.path.join(path_cantiere, "stato.json")
    try:
        dati_stato = {}
        if os.path.exists(stato_file):
            with open(stato_file, 'r', encoding='utf-8') as f:
                dati_stato = json.load(f)
        
        dati_stato['indirizzo'] = nuovo_indirizzo
        
        with open(stato_file, 'w', encoding='utf-8') as f:
            json.dump(dati_stato, f, ensure_ascii=False, indent=2)
            
        debug_info.append("File stato.json aggiornato")
            
    except Exception as e:
        errore_msg = f"Errore aggiornamento stato.json: {e}"
        debug_info.append(f"ERRORE: {errore_msg}")
        errori.append(errore_msg)
    
    # Aggiungi info debug al risultato
    risultato_debug = " | ".join(debug_info)
    if file_rinominati == 0 and not errori:
        return 0, f"Nessun file rinominato. Debug: {risultato_debug}"
    
    return file_rinominati, f"{'; '.join(errori) if errori else 'Successo'} | Debug: {risultato_debug}"

def rinomina_cartella_cantiere(codice_cantiere, nuovo_indirizzo):
    """Rinomina la cartella del cantiere per includere l'indirizzo"""
    vecchia_cartella = os.path.join(P_SICUREZZA, codice_cantiere)
    
    if not os.path.exists(vecchia_cartella):
        return False, "Cartella cantiere non trovata"
    
    # Pulisci l'indirizzo per il nome della cartella
    indirizzo_pulito = nuovo_indirizzo.replace(" ", "_").replace(",", "").replace("/", "_")
    nuovo_nome_cartella = f"{codice_cantiere}_{indirizzo_pulito}"
    nuova_cartella = os.path.join(P_SICUREZZA, nuovo_nome_cartella)
    
    # Verifica che la nuova cartella non esista già
    if os.path.exists(nuova_cartella):
        return False, f"La cartella {nuovo_nome_cartella} esiste già"
    
    try:
        # Rinomina la cartella
        os.rename(vecchia_cartella, nuova_cartella)
        
        # Aggiorna il file stato.json con il nuovo indirizzo e codice
        stato_file = os.path.join(nuova_cartella, "stato.json")
        try:
            dati_stato = {}
            if os.path.exists(stato_file):
                with open(stato_file, 'r', encoding='utf-8') as f:
                    dati_stato = json.load(f)
            
            dati_stato['indirizzo'] = nuovo_indirizzo
            dati_stato['codice_originale'] = codice_cantiere
            dati_stato['nuovo_codice'] = nuovo_nome_cartella
            
            with open(stato_file, 'w', encoding='utf-8') as f:
                json.dump(dati_stato, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logging.error(f"Errore aggiornamento stato.json: {e}")
        
        # Aggiorna il registro
        scrivi_registro(nuovo_nome_cartella, "", "", "Rinomina cartella cantiere")
        
        return True, f"Cartella rinominata: {codice_cantiere} -> {nuovo_nome_cartella}"
        
    except Exception as e:
        return False, f"Errore rinomina cartella: {e}"

def rinomina_file_singolo(codice_cantiere, nome_file, nuovo_indirizzo):
    """Rinomina un singolo file con l'indirizzo specificato"""
    path_cantiere = os.path.join(P_SICUREZZA, codice_cantiere)
    vecchio_path = os.path.join(path_cantiere, nome_file)
    
    if not os.path.exists(vecchio_path):
        return False, "File non trovato"
    
    # Estrai tipo documento dal nome file
    if nome_file.startswith('POS_'):
        tipo_doc = 'POS'
    elif nome_file.startswith('PiMUS_'):
        tipo_doc = 'PiMUS'
    elif nome_file.startswith('DUVRI_'):
        tipo_doc = 'DUVRI'
    else:
        return False, "Tipo documento non riconosciuto"
    
    # Pulisci l'indirizzo per il nome file
    indirizzo_pulito = nuovo_indirizzo.replace(" ", "_").replace(",", "").replace("/", "_")
    
    # Crea nuovo nome
    estensione = os.path.splitext(nome_file)[1]
    nuovo_file = f"{tipo_doc}_{codice_cantiere}_{indirizzo_pulito}{estensione}"
    nuovo_path = os.path.join(path_cantiere, nuovo_file)
    
    # Rinomina se il nuovo nome è diverso
    if vecchio_path != nuovo_path:
        try:
            os.rename(vecchio_path, nuovo_path)
            
            # Aggiorna il registro
            scrivi_registro(codice_cantiere, tipo_doc, nuovo_file, "Rinomina singola")
            
            return True, f"File rinominato: {nome_file} -> {nuovo_file}"
            
        except Exception as e:
            return False, f"Errore: {e}"
    
    return False, "Il file ha già il nome corretto"

# ── Conversione DOCX → PDF ────────────────────────────────────────────────────
def converti_pdf(input_path: str, output_path: str):
    """Tenta docx2PDF; fallback su comtypes (richiede Word installato)."""
    if DOCX2PDF_OK:
        docx2pdf_convert(input_path, output_path)
        return
    # Fallback comtypes
    try:
        import comtypes.client
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False
        try:
            doc = word.Documents.Open(os.path.abspath(input_path))
            doc.SaveAs(os.path.abspath(output_path), FileFormat=17)
            doc.Close()
        finally:
            word.Quit()
    except ImportError:
        raise RuntimeError(
            "Nessun convertitore PDF disponibile. "
            "Installa docx2PDF con: pip install docx2pdf"
        )

# ── Backup ────────────────────────────────────────────────────────────────────
def esegui_backup() -> str:
    os.makedirs(P_BACKUP, exist_ok=True)
    nome_zip = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    path_zip = os.path.join(P_BACKUP, nome_zip)
    with zipfile.ZipFile(path_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for cartella_radice in [P_SICUREZZA, P_ATT, P_INFO]:
            if os.path.exists(cartella_radice):
                for root, _, files in os.walk(cartella_radice):
                    for file in files:
                        fp = os.path.join(root, file)
                        arcname = os.path.relpath(fp, P_BASE)
                        zf.write(fp, arcname)
    return path_zip

# ── Salvataggio file caricato ─────────────────────────────────────────────────
def salva_file_caricato(upload, cartella_dest: str, prefisso: str = "") -> bool:
    if upload is None:
        return False
    try:
        nome_file = prefisso + upload.name
        path_dest = os.path.join(cartella_dest, nome_file)
        with open(path_dest, "wb") as f:
            f.write(upload.getbuffer())
        return True
    except Exception as e:
        logging.error(f"salva_file_caricato: {e}")
        st.error(f"Errore salvataggio: {e}")
        return False

# ── Reset campi form ──────────────────────────────────────────────────────────
def reset_campi():
    for k in ["clie", "cf_cl", "ind", "cit", "prov_camp", "dir_lav", "n_lav_c", "opera_desc"]:
        st.session_state[k] = ""
    st.session_state["d_inizio"] = datetime.now().date()
    st.session_state["d_fine"]   = datetime.now().date()
    st.session_state["codice_cant_gen"] = genera_codice_cantiere()

# ── Validazione form ──────────────────────────────────────────────────────────
def valida_form() -> list[str]:
    errori = []
    campi = {
        "Committente":         st.session_state.get("clie", "").strip(),
        "Indirizzo Cantiere":  st.session_state.get("ind", "").strip(),
        "Città":               st.session_state.get("cit", "").strip(),
        "Provincia":           st.session_state.get("prov_camp", "").strip(),
        "N° Lavoratori":       st.session_state.get("n_lav_c", "").strip(),
        "Descrizione Opere":   st.session_state.get("opera_desc", "").strip(),
    }
    for nome, valore in campi.items():
        if not valore:
            errori.append(nome)
    return errori

# ── KPI Dashboard ─────────────────────────────────────────────────────────────
def calcola_kpi() -> dict:
    kpi = {
        "cantieri_attivi": 0,
        "cantieri_totali": 0,
        "docs_totali": 0,
        "attestati_in_scadenza": 0,
        "attestati_scaduti": 0,
    }
    if os.path.exists(P_SICUREZZA):
        cantieri = [
            d for d in os.listdir(P_SICUREZZA)
            if os.path.isdir(os.path.join(P_SICUREZZA, d)) and not d.startswith("Modello")
        ]
        kpi["cantieri_totali"] = len(cantieri)
        for c in cantieri:
            p_c = os.path.join(P_SICUREZZA, c)
            stato = leggi_stato_cantiere(p_c)
            if stato == "in corso":
                kpi["cantieri_attivi"] += 1
            kpi["docs_totali"] += len([
                f for f in os.listdir(p_c) if f.lower().endswith((".pdf", ".docx"))
            ])
    scadenze = leggi_scadenze()
    oggi = date.today()
    for lav_data in scadenze.values():
        for att in lav_data.values():
            try:
                data_s = date.fromisoformat(att.get("scadenza", ""))
                delta  = (data_s - oggi).days
                if delta < 0:
                    kpi["attestati_scaduti"] += 1
                elif delta <= 60:
                    kpi["attestati_in_scadenza"] += 1
            except (ValueError, AttributeError):
                pass
    return kpi

# ══════════════════════════════════════════════════════════════════════════════
# INTESTAZIONE
# ══════════════════════════════════════════════════════════════════════════════
col_backup, col_logo = st.columns([1, 5])
with col_backup:
    st.markdown("<div style='padding-top:0.9rem;'>", unsafe_allow_html=True)
    if DRIVE_OK:
        if st.button(" Backup", use_container_width=True):
            with st.spinner("Backup..."):
                try:
                    path_zip = esegui_backup()
                    st.success(f" {os.path.basename(path_zip)}")
                except Exception as e:
                    logging.error(f"Backup: {e}")
                    st.error(f"Errore: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

with col_logo:
    st.markdown(
        '<div style="padding:0.8rem 0 0.4rem;text-align:right;display:flex;align-items:center;justify-content:flex-end;">'
        '<svg width="60" height="40" viewBox="0 0 60 40" style="margin-right:0.5rem;">'
        '<rect x="5" y="25" width="8" height="12" fill="#FF8C00"/>'  # Arancione - base sinistra
        '<rect x="15" y="20" width="8" height="17" fill="#E02B2B"/>'  # Rosso - centro sinistra
        '<rect x="25" y="15" width="8" height="22" fill="#FF8C00"/>'  # Arancione - centro
        '<rect x="35" y="10" width="8" height="27" fill="#E02B2B"/>'  # Rosso - centro destra
        '<rect x="45" y="5" width="8" height="32" fill="#FF8C00"/>'   # Arancione - destra
        '<polygon points="13,25 13,20 15,20 15,25" fill="#8B0000"/>'  # Bordeau dettaglio
        '<polygon points="23,20 23,15 25,15 25,20" fill="#8B0000"/>'  # Bordeau dettaglio
        '<polygon points="33,15 33,10 35,10 35,15" fill="#8B0000"/>'  # Bordeau dettaglio
        '<polygon points="43,10 43,5 45,5 45,10" fill="#8B0000"/>'   # Bordeau dettaglio
        '</svg>'
        '<span style="font-family:Barlow Condensed,sans-serif;font-weight:900;'
        'font-size:2.2rem;color:#E02B2B;letter-spacing:0.06em;">EDILMERC</span>'
        '<span style="font-size:0.8rem;color:#8B0000;letter-spacing:0.12em;'
        'margin-left:1rem;vertical-align:middle;">di Mercurio Davide</span>'
        '</div>',
        unsafe_allow_html=True,
    )

if not DRIVE_OK:
    alert("G:Drive non raggiungibile. Controlla la connessione.", "rosso", "⚠️")

pulisci_cartelle_vuote()

# ══════════════════════════════════════════════════════════════════════════════
# TABS — FASCICOLO
# ══════════════════════════════════════════════════════════════════════════════
tab_dash, tab_cant, tab_att, tab_coll, tab_imp, tab_reg = st.tabs([
    "🏠  Dashboard",
    "🚧  Sicurezza & Cantieri",
    "👷  Attestati",
    "👥  Collaboratori",
    "⚙️  Impostazioni Aziendali",
    "📋  Registro Documenti",
])


# ══════════════════════════════════════════════════════════════════════════════
# 1. DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
        st.title("Dashboard Aziendale")

        if not DRIVE_OK:
            alert("G:Drive non raggiungibile — i dati mostrati potrebbero non essere aggiornati.", "rosso", "⚠️")

        # ── Dati aziendali ────────────────────────────────────────────────────────
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("📋 Dati Fiscali", expanded=True):
                st.markdown("""
    | Campo | Valore |
    |---|---|
    | **Titolare** | Davide Mercurio |
    | **P.IVA** | 02964520352 |
    | **Codice Fiscale** | MRCDVD89A10H223F |
    | **PEC** | edilmerc@legalmail.it |
    | **Indirizzo** | Via G. Venturi 43, 42021 Bibbiano (RE) |
    """)
        with col_b:
            with st.expander("🏦 Coordinate Bancarie", expanded=True):
                st.markdown("""
    | Campo | Valore |
    |---|---|
    | **Banca** | Banco BPM |
    | **Intestato a** | EDILMERC DI MERCURIO DAVIDE |
    """)
                st.code("IT 08 L 02008 66250 000106132902", language=None)

        if DRIVE_OK:
            st.divider()
            st.subheader("📊 KPI Aziendali")
            kpi = calcola_kpi()

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Cantieri Attivi",       kpi["cantieri_attivi"])
            c2.metric("Cantieri Totali",        kpi["cantieri_totali"])
            c3.metric("Documenti Cantieri",     kpi["docs_totali"])
            c4.metric("Attestati in scadenza",  kpi["attestati_in_scadenza"],
                      delta=f"-{kpi['attestati_in_scadenza']}" if kpi["attestati_in_scadenza"] else None,
                      delta_color="inverse")
            c5.metric("Attestati scaduti",      kpi["attestati_scaduti"],
                      delta=f"-{kpi['attestati_scaduti']}" if kpi["attestati_scaduti"] else None,
                      delta_color="inverse")

            # Semaforo attestati
            if kpi["attestati_scaduti"] > 0:
                alert(f"{kpi['attestati_scaduti']} attestato/i SCADUTO/I. Rinnovare subito!", "rosso", "🚨")
            elif kpi["attestati_in_scadenza"] > 0:
                alert(f"{kpi['attestati_in_scadenza']} attestato/i in scadenza entro 60 giorni.", "giallo", "⚠️")
            else:
                alert("Tutti gli attestati sono in regola.", "verde", "✅")

            # Backup recenti
            if os.path.exists(P_BACKUP):
                backups = sorted(
                    [f for f in os.listdir(P_BACKUP) if f.endswith(".zip")], reverse=True
                )
                if backups:
                    st.divider()
                    st.subheader("💾 Ultimi Backup")
                    for b in backups[:3]:
                        st.markdown(f"🗜️ `{b}`")

    # ══════════════════════════════════════════════════════════════════════════════
    # 2. SICUREZZA & CANTIERI
    # ══════════════════════════════════════════════════════════════════════════════
with tab_cant:
        st.title("Sicurezza & Cantieri")

        # ── DVR Aziendale ────────────────────────────────────────────────────────
        with st.container():
            st.subheader("🛡️ Documentazione Generale")
            if st.button("📄 Apri DVR Aziendale", use_container_width=False):
                if os.path.exists(P_INFO):
                    dvr_files = [f for f in os.listdir(P_INFO) if "DVR" in f.upper()]
                    if dvr_files:
                        apri_doc(os.path.join(P_INFO, dvr_files[0]))
                    else:
                        alert("Documento DVR non trovato nella cartella Info.", "rosso", "❌")
                else:
                    alert("Cartella Info non trovata.", "rosso", "❌")

        st.divider()

        # ── Inizializzazione session_state ────────────────────────────────────────
        for k, v in {
            "clie": "", "cf_cl": "", "ind": "", "cit": "",
            "prov_camp": "", "dir_lav": "", "n_lav_c": "", "opera_desc": "",
            "d_inizio": datetime.now().date(),
            "d_fine":   datetime.now().date(),
        }.items():
            if k not in st.session_state:
                st.session_state[k] = v

        if "codice_cant_gen" not in st.session_state:
            st.session_state["codice_cant_gen"] = genera_codice_cantiere()

        # ── Form generazione documenti ────────────────────────────────────────────
        with st.expander("🆕 Genera Nuovo Documento", expanded=False):

            # Codice cantiere automatico
            cod = st.session_state["codice_cant_gen"]
            st.markdown(
                f'<div style="margin-bottom:1rem;">'
                f'Codice Cantiere assegnato: <strong style="color:#F28C1E;font-size:1.1rem;">{cod}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            with c1:
                st.session_state.clie       = st.text_input("Committente *",             value=st.session_state.clie)
                st.session_state.cf_cl      = st.text_input("Codice Fiscale Direttore Lavori",    value=st.session_state.cf_cl)
                st.session_state.ind        = st.text_input("Indirizzo Cantiere *",      value=st.session_state.ind)
                st.session_state.cit        = st.text_input("Città *",                   value=st.session_state.cit)
                st.session_state.prov_camp  = st.text_input("Provincia *",               value=st.session_state.prov_camp)
            with c2:
                st.session_state.dir_lav    = st.text_input("Direttore Lavori",          value=st.session_state.dir_lav)
                st.session_state.n_lav_c    = st.text_input("N° Lavoratori *",           value=st.session_state.n_lav_c)
                st.session_state.opera_desc = st.text_area("Descrizione Opere *",        value=st.session_state.opera_desc, height=120)
                d_in = st.date_input("Inizio Lavori",                                    value=st.session_state.d_inizio)
                d_fi = st.date_input("Fine Lavori",                                      value=st.session_state.d_fine)
                st.session_state.d_inizio = d_in
                st.session_state.d_fine   = d_fi

            tipo_doc = st.radio("Tipo Documento", ["POS", "PiMUS"], horizontal=True)

            col1, col2, col3 = st.columns(3)

            # ── Genera Word ───────────────────────────────────────────────────────
            if col1.button("📝 1. Genera Word"):
                errori = valida_form()
                if errori:
                    alert(f"Campi obbligatori mancanti: {', '.join(errori)}", "rosso", "❌")
                elif not DOCXTPL_OK:
                    alert("Libreria docxtpl non installata. Esegui: pip install docxtpl", "rosso", "❌")
                else:
                    m_path = os.path.join(P_SICUREZZA, f"Modello_{tipo_doc}.docx")
                    if not os.path.exists(m_path):
                        alert(f"Modello {tipo_doc} non trovato in {P_SICUREZZA}", "rosso", "❌")
                    else:
                        try:
                            doc = DocxTemplate(m_path)
                            ctx = {
                                "CODICE_CANTIERE":  cod,
                                "CLIENTE":          st.session_state.clie,
                                "CODICE_FISCALE":   st.session_state.cf_cl,
                                "INDIRIZZO":        st.session_state.ind,
                                "CITTA":            st.session_state.cit,
                                "PROVINCIA":        st.session_state.prov_camp,
                                "DIRETTORE_LAVORI": st.session_state.dir_lav,
                                "N":                st.session_state.n_lav_c,
                                "DESCRIZIONE_OPERA":st.session_state.opera_desc,
                                "DATA_INIZIO":      st.session_state.d_inizio.strftime("%d/%m/%Y"),
                                "DATA_FINE":        st.session_state.d_fine.strftime("%d/%m/%Y"),
                            }
                            doc.render(ctx)
                            # Crea prima la cartella con codice base
                            cart_p_base = os.path.join(P_SICUREZZA, cod)
                            os.makedirs(cart_p_base, exist_ok=True)
                            salva_stato_cantiere(cart_p_base, "in corso")
                            
                            # Pulisci l'indirizzo per il nome della cartella e file
                            indirizzo_pulito = st.session_state.ind.replace(" ", "_").replace(",", "").replace("/", "_")
                            
                            # Rinomina la cartella per includere l'indirizzo
                            nuovo_nome_cartella = f"{cod}_{indirizzo_pulito}"
                            cart_p_nuova = os.path.join(P_SICUREZZA, nuovo_nome_cartella)
                            
                            try:
                                if cart_p_base != cart_p_nuova:
                                    os.rename(cart_p_base, cart_p_nuova)
                                    cart_p = cart_p_nuova
                                    # Aggiorna il codice cantiere con il nuovo nome
                                    cod_con_indirizzo = nuovo_nome_cartella
                                else:
                                    cart_p = cart_p_base
                                    cod_con_indirizzo = cod
                            except Exception as e:
                                logging.error(f"Errore rinomina cartella: {e}")
                                cart_p = cart_p_base
                                cod_con_indirizzo = cod
                            
                            # Salva l'indirizzo nel file stato.json per usi futuri
                            stato_file = os.path.join(cart_p, "stato.json")
                            try:
                                dati_stato = {"stato": "in corso", "indirizzo": st.session_state.ind, "codice_originale": cod}
                                with open(stato_file, 'w', encoding='utf-8') as f:
                                    json.dump(dati_stato, f, ensure_ascii=False, indent=2)
                            except Exception as e:
                                logging.error(f"Errore salvataggio stato.json: {e}")
                            
                            # Crea il nome del file usando il codice con indirizzo
                            nome_word = f"{tipo_doc}_{cod_con_indirizzo}.docx"
                            f_word    = os.path.join(cart_p, nome_word)
                            doc.save(f_word)
                            apri_doc(f_word)
                            scrivi_registro(cod_con_indirizzo, tipo_doc, nome_word, "Creazione Word")
                            alert(f"Documento Word creato: {nome_word}", "verde", "✅")
                        except Exception as e:
                            logging.error(f"Genera Word: {e}")
                            alert(f"Errore generazione Word: {e}", "rosso", "❌")

            # ── Crea PDF ──────────────────────────────────────────────────────────
            if col2.button("📄 2. Crea PDF"):
                # Trova la cartella corretta con l'indirizzo
                indirizzo_pulito = st.session_state.ind.replace(" ", "_").replace(",", "").replace("/", "_")
                nome_cartella_cercata = f"{cod}_{indirizzo_pulito}"
                cartella_con_indirizzo = os.path.join(P_SICUREZZA, nome_cartella_cercata)
                
                # Se esiste la cartella con indirizzo, usala, altrimenti usa quella base
                if os.path.exists(cartella_con_indirizzo):
                    f_word = os.path.join(cartella_con_indirizzo, f"{tipo_doc}_{nome_cartella_cercata}.docx")
                else:
                    f_word = os.path.join(P_SICUREZZA, cod, f"{tipo_doc}_{cod}_{indirizzo_pulito}.docx")
                if not os.path.exists(f_word):
                    alert("Genera prima il documento Word (Step 1).", "giallo", "⚠️")
                else:
                    try:
                        f_pdf = f_word.replace(".docx", ".pdf")
                        with st.spinner("Conversione in corso..."):
                            converti_pdf(f_word, f_pdf)
                        scrivi_registro(cod, tipo_doc, os.path.basename(f_pdf), "Creazione PDF")
                        alert("PDF creato con successo.", "verde", "✅")
                    except Exception as e:
                        logging.error(f"Crea PDF: {e}")
                        alert(f"Errore creazione PDF: {e}", "rosso", "❌")

            # ── Svuota campi ──────────────────────────────────────────────────────
            if col3.button("🧹 Svuota Campi"):
                reset_campi()
                st.rerun()

        st.divider()

        # ── Lista cantieri ────────────────────────────────────────────────────────
        st.subheader("📍 Cantieri")

        # Filtro stato
        filtro_stato = st.selectbox(
            "Filtra per stato",
            ["Tutti"] + STATI_CANTIERE,
            index=0,
            label_visibility="visible",
        )

        if os.path.exists(P_SICUREZZA):
            cantieri = sorted([
                d for d in os.listdir(P_SICUREZZA)
                if os.path.isdir(os.path.join(P_SICUREZZA, d)) and not d.startswith("Modello")
            ])

            if not cantieri:
                alert("Nessun cantiere trovato.", "blu", "📂")
            else:
                for via in cantieri:
                    path_c = os.path.join(P_SICUREZZA, via)
                    stato_c = leggi_stato_cantiere(path_c)

                    if filtro_stato != "Tutti" and stato_c != filtro_stato:
                        continue

                    badge_tipo = STATO_BADGE.get(stato_c, "grigio")
                    icona_s    = STATO_ICONA.get(stato_c, "")

                    with st.expander(
                        f"{icona_s} {via.upper()}  ·  Stato: {stato_c.upper()}",
                        expanded=(stato_c == "in corso"),
                    ):
                        # ── Cambio stato ──────────────────────────────────────────
                        col_stato, _ = st.columns([2, 3])
                        nuovo_stato = col_stato.selectbox(
                            "Stato cantiere",
                            STATI_CANTIERE,
                            index=STATI_CANTIERE.index(stato_c),
                            key=f"stato_{via}",
                        )
                        if nuovo_stato != stato_c:
                            salva_stato_cantiere(path_c, nuovo_stato)
                            st.rerun()

                        st.divider()

                        # Mostra campo indirizzo solo se si attiva la rinomina
                        if st.session_state.get(f"show_rename_{via}", False):
                            # Leggi indirizzo corrente se disponibile
                            indirizzo_corrente = ""
                            stato_file = os.path.join(path_c, "stato.json")
                            if os.path.exists(stato_file):
                                try:
                                    with open(stato_file, 'r', encoding='utf-8') as f:
                                        dati = json.load(f)
                                        indirizzo_corrente = dati.get('indirizzo', '')
                                except:
                                    pass
                            
                            st.markdown("** Rinomina File con Selezione Manuale**")
                            st.info("Seleziona manualmente il tipo di ogni documento, poi inserisci l'indirizzo")
                            
                            # Mostra i file e permetti di selezionare il tipo
                            file_types = {}
                            docs_for_rename = [f for f in os.listdir(path_c) if f.endswith(('.docx', '.pdf')) and not f.startswith('Modello')]
                            
                            if docs_for_rename:
                                st.markdown("**Seleziona tipo documento:**")
                                for file in docs_for_rename:
                                    col_file, col_tipo = st.columns([3, 1])
                                    col_file.write(f" {file}")
                                    file_types[file] = col_tipo.selectbox(
                                        "Tipo",
                                        ["POS", "PiMUS", "DUVRI", "Ignora"],
                                        key=f"tipo_{via}_{file}",
                                        label_visibility="collapsed"
                                    )
                            
                            nuovo_indirizzo = st.text_input(
                                "Indirizzo cantiere",
                                value=indirizzo_corrente,
                                placeholder="Es: Via Roma 123, Novi di Modena (MO)",
                                key=f"indirizzo_{via}"
                            )
                            
                            # Opzione per rinominare anche la cartella
                            rinomina_cartella = st.checkbox(" Rinomina anche la cartella del cantiere", key=f"rename_folder_{via}")
                            
                            col_conf, col_ann = st.columns([1, 1])
                            if col_conf.button(" Conferma Rinomina", key=f"confirm_rename_{via}"):
                                if nuovo_indirizzo.strip():
                                    with st.spinner("Rinomina in corso..."):
                                        # Prima rinomina la cartella se richiesto
                                        if rinomina_cartella:
                                            successo, risultato = rinomina_cartella_cantiere(via, nuovo_indirizzo.strip())
                                            if successo:
                                                st.success(f" {risultato}")
                                                # Aggiorna il nome del cantiere per le operazioni successive
                                                nuovo_nome_cantiere = risultato.split(" -> ")[1].strip()
                                            else:
                                                st.error(f" Errore rinomina cartella: {risultato}")
                                                st.stop()
                                        
                                        # Poi rinomina i file
                                        nome_cantiere_usato = nuovo_nome_cantiere if rinomina_cartella else via
                                        file_rinominati, risultato = rinomina_file_manuale_con_selezione(nome_cantiere_usato, nuovo_indirizzo.strip(), file_types)
                                        if file_rinominati > 0:
                                            st.success(f" {file_rinominati} file rinominati!")
                                            # Resetta lo stato e ricarica
                                            st.session_state[f"show_rename_{via}"] = False
                                            st.rerun()
                                        else:
                                            st.warning(f" Nessun file rinominato: {risultato}")
                                else:
                                    st.error(" Inserisci un indirizzo valido")
                            
                            if col_ann.button(" Annulla", key=f"cancel_rename_{via}"):
                                st.session_state[f"show_rename_{via}"] = False
                                st.rerun()
                            
                            st.divider()
                        
                        st.divider()

                        files = [f for f in os.listdir(path_c) if f != "stato.json"]
                        docs  = [f for f in files if f.lower().endswith((".pdf", ".docx"))]
                        imgs  = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

                        col_docs, col_imgs = st.columns([3, 2])

                        # ── Documenti ─────────────────────────────────────────────
                        with col_docs:
                            st.markdown("**📁 Documenti**")
                            if not docs:
                                st.markdown('<span style="color:#555;font-size:0.85rem;">Nessun documento</span>', unsafe_allow_html=True)
                            for f in docs:
                                fp = os.path.join(path_c, f)
                                ic = " " if f.endswith(".docx") else " "
                                r1, r2, r3 = st.columns([4, 1, 1])
                                r1.write(f"{ic} {f}")
                                if r2.button("Apri", key=f"v_{via}_{f}"):
                                    apri_doc(fp)
                                if r3.button("Elimina", key=f"d_{via}_{f}"):
                                    st.session_state[f"confirm_{via}_{f}"] = True

                                if st.session_state.get(f"confirm_{via}_{f}"):
                                    alert(f"Confermi eliminazione di **{f}**?", "rosso", " ")
                                    yes_c, no_c, _ = st.columns([1, 1, 4])
                                    if yes_c.button(" Sì, elimina", key=f"y_{via}_{f}"):
                                        elimina_file(fp)
                                        scrivi_registro(via, "", f, "Eliminazione")
                                        del st.session_state[f"confirm_{via}_{f}"]
                                    if no_c.button(" No", key=f"n_{via}_{f}"):
                                        del st.session_state[f"confirm_{via}_{f}"]
                                        st.rerun()

                            # Pulsante unico di rinomina per il cantiere
                            st.markdown("---")
                            if st.button(" Rinomina File Cantiere", key=f"rename_cantiere_{via}", use_container_width=True):
                                st.session_state[f"show_rename_{via}"] = True
                                st.rerun()

                            # Upload documento aggiuntivo
                            st.markdown("---")
                            up_doc = st.file_uploader(
                                "Aggiungi documento al cantiere",
                                key=f"up_{via}",
                                type=["pdf", "docx"],
                                label_visibility="visible",
                            )
                            if up_doc:
                                if st.button(f"Salva documento", key=f"btn_up_{via}"):
                                    if salva_file_caricato(up_doc, path_c):
                                        scrivi_registro(via, "", up_doc.name, "Upload")
                                        alert("Documento salvato.", "verde", "✅")
                                        st.rerun()

                        # ── Galleria foto ─────────────────────────────────────────
                        with col_imgs:
                            st.markdown("**🖼️ Foto Cantiere**")
                            if imgs:
                                idx_key = f"img_idx_{via}"
                                if idx_key not in st.session_state:
                                    st.session_state[idx_key] = 0
                                idx = st.session_state[idx_key]
                                idx = max(0, min(idx, len(imgs) - 1))

                                st.image(os.path.join(path_c, imgs[idx]), use_container_width=True)
                                st.caption(f"{imgs[idx]}  ({idx+1}/{len(imgs)})")

                                nav_l, nav_r = st.columns(2)
                                if nav_l.button("◀", key=f"img_l_{via}") and idx > 0:
                                    st.session_state[idx_key] = idx - 1
                                    st.rerun()
                                if nav_r.button("▶", key=f"img_r_{via}") and idx < len(imgs) - 1:
                                    st.session_state[idx_key] = idx + 1
                                    st.rerun()
                            else:
                                st.markdown('<span style="color:#555;font-size:0.85rem;">Nessuna foto</span>', unsafe_allow_html=True)

                            # Upload foto
                            up_foto = st.file_uploader(
                                "Aggiungi foto",
                                key=f"foto_{via}",
                                type=["jpg", "jpeg", "png"],
                                accept_multiple_files=True,
                                label_visibility="visible",
                            )
                            if up_foto:
                                if st.button("Salva foto", key=f"btn_foto_{via}"):
                                    ok = 0
                                    for foto in up_foto:
                                        if salva_file_caricato(foto, path_c):
                                            ok += 1
                                    if ok:
                                        alert(f"{ok} foto salvate.", "verde", "✅")
                                        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════════
    # 3. ATTESTATI
    # ════════════════════════════════════════════════════════════════════════════
with tab_att:
        st.title("Registro Attestati")

        LAVORATORI = ["DAVIDE", "AHMED", "ANTONIO", "LALA"]

        scadenze = leggi_scadenze()
        oggi     = date.today()

        if os.path.exists(P_ATT):
            files_att = [f for f in os.listdir(P_ATT) if f.lower().endswith(".pdf")]
        else:
            files_att = []

        for lav in LAVORATORI:
            docs_lav = [f for f in files_att if lav in f.upper()]
            sc_lav   = scadenze.get(lav, {})

            # Conta eventuali problemi
            n_scad   = sum(
                1 for att_data in sc_lav.values()
                if (date.fromisoformat(att_data.get("scadenza", str(oggi + timedelta(days=999)))) - oggi).days < 0
            )
            n_warn   = sum(
                1 for att_data in sc_lav.values()
                if 0 <= (date.fromisoformat(att_data.get("scadenza", str(oggi + timedelta(days=999)))) - oggi).days <= 60
            )

            icona_lav = "🚨" if n_scad else ("⚠️" if n_warn else "👤")

            with st.expander(f"{icona_lav} {lav}", expanded=True):

                if not docs_lav:
                    alert("Nessun attestato caricato.", "blu", "📂")
                else:
                    for d in docs_lav:
                        fp      = os.path.join(P_ATT, d)
                        att_key = d.replace(".pdf", "")
                        info_att = sc_lav.get(att_key, {})

                        # Riga principale
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 2, 1])
                        c1.write(f"📜 {d}")

                        # Semaforo scadenza
                        if info_att:
                            try:
                                data_s = date.fromisoformat(info_att.get("scadenza", ""))
                                b_tipo, b_testo, _ = semaforo_scadenza(data_s)
                                c4.markdown(badge_html(b_testo, b_tipo), unsafe_allow_html=True)
                            except (ValueError, KeyError):
                                c4.markdown(badge_html("Scadenza ?", "grigio"), unsafe_allow_html=True)
                        else:
                            c4.markdown(badge_html("Scadenza ?", "grigio"), unsafe_allow_html=True)

                        if c2.button("Apri", key=f"a_{d}"):
                            apri_doc(fp)
                        if c3.button("🗑️",  key=f"del_{d}"):
                            st.session_state[f"ca_{d}"] = True
                        # Bottone modifica scadenza
                        if c5.button("✏️", key=f"edit_{d}", help="Modifica data scadenza"):
                            st.session_state[f"edit_mode_{d}"] = not st.session_state.get(f"edit_mode_{d}", False)

                        # ── Pannello modifica scadenza ────────────────────────────
                        if st.session_state.get(f"edit_mode_{d}"):
                            with st.container():
                                st.markdown(
                                    '<div style="background:#A9A9A9;border:1px solid #F28C1E;'
                                    'border-radius:8px;padding:0.8rem 1rem;margin:0.4rem 0 0.6rem;">',
                                    unsafe_allow_html=True,
                                )
                                st.markdown(
                                    f'<span style="color:#F28C1E;font-weight:700;font-size:0.9rem;">'
                                    f'✏️ Modifica Scadenza — {d}</span>',
                                    unsafe_allow_html=True,
                                )
                                em1, em2, em3 = st.columns([2, 2, 2])

                                # Valori attuali come default
                                try:
                                    val_cons = date.fromisoformat(info_att.get("conseguimento", date.today().isoformat()))
                                except ValueError:
                                    val_cons = date.today()
                                try:
                                    val_scad = date.fromisoformat(info_att.get("scadenza", (date.today() + timedelta(days=365*5)).isoformat()))
                                except ValueError:
                                    val_scad = date.today() + timedelta(days=365*5)

                                nuovo_tipo = em1.text_input(
                                    "Tipo Corso",
                                    value=info_att.get("tipo_corso", ""),
                                    key=f"nt_{d}",
                                )
                                nuova_cons = em2.date_input(
                                    "Data Conseguimento",
                                    value=val_cons,
                                    key=f"nc_{d}",
                                )
                                nuova_scad = em3.date_input(
                                    "Nuova Data Scadenza",
                                    value=val_scad,
                                    key=f"ns_{d}",
                                )

                                salva_btn, annulla_btn, _ = st.columns([1, 1, 4])
                                if salva_btn.button("💾 Salva", key=f"save_scad_{d}"):
                                    if lav not in scadenze:
                                        scadenze[lav] = {}
                                    scadenze[lav][att_key] = {
                                        "tipo_corso":    nuovo_tipo,
                                        "conseguimento": nuova_cons.isoformat(),
                                        "scadenza":      nuova_scad.isoformat(),
                                    }
                                    salva_scadenze(scadenze)
                                    del st.session_state[f"edit_mode_{d}"]
                                    alert(f"Scadenza aggiornata: {nuova_scad.strftime('%d/%m/%Y')}", "verde", "✅")
                                    st.rerun()
                                if annulla_btn.button("✖ Annulla", key=f"ann_scad_{d}"):
                                    del st.session_state[f"edit_mode_{d}"]
                                    st.rerun()
                                st.markdown("</div>", unsafe_allow_html=True)

                        # ── Conferma eliminazione ─────────────────────────────────
                        if st.session_state.get(f"ca_{d}"):
                            alert(f"Confermi eliminazione di **{d}**?", "rosso", "⚠️")
                            ya_c, na_c, _ = st.columns([1, 1, 4])
                            if ya_c.button("✅ Sì", key=f"ya_{d}"):
                                elimina_file(fp)
                                if lav in scadenze and att_key in scadenze[lav]:
                                    del scadenze[lav][att_key]
                                    salva_scadenze(scadenze)
                                del st.session_state[f"ca_{d}"]
                            if na_c.button("❌ No", key=f"na_{d}"):
                                del st.session_state[f"ca_{d}"]
                                st.rerun()

                st.markdown("---")
                st.markdown("**➕ Aggiungi Attestato**")
                col_up, col_sc = st.columns(2)

                with col_up:
                    up_att = st.file_uploader(
                        f"PDF attestato per {lav}",
                        key=f"up_att_{lav}",
                        type=["pdf"],
                        label_visibility="visible",
                    )

                with col_sc:
                    tipo_corso  = st.text_input("Tipo Corso",          key=f"tc_{lav}", placeholder="es. Sicurezza Base 8h")
                    data_cons   = st.date_input("Data Conseguimento",   key=f"dc_{lav}", value=date.today())
                    data_scad_i = st.date_input("Data Scadenza",        key=f"ds_{lav}", value=date.today() + timedelta(days=365*5))

                if st.button(f"Salva Attestato {lav}", key=f"btn_att_{lav}"):
                    if up_att is None:
                        alert("Seleziona un file PDF prima di salvare.", "giallo", "⚠️")
                    else:
                        prefisso = f"{lav}_"
                        if salva_file_caricato(up_att, P_ATT, prefisso=prefisso):
                            # Salva scadenza
                            if lav not in scadenze:
                                scadenze[lav] = {}
                            att_key_new = (prefisso + up_att.name).replace(".pdf", "")
                            scadenze[lav][att_key_new] = {
                                "tipo_corso":    tipo_corso,
                                "conseguimento": data_cons.isoformat(),
                                "scadenza":      data_scad_i.isoformat(),
                            }
                            salva_scadenze(scadenze)
                            alert(f"Attestato salvato. Scadenza: {data_scad_i.strftime('%d/%m/%Y')}", "verde", "✅")
                            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════════
    # 4. COLLABORATORI
    # ══════════════════════════════════════════════════════════════════════════════
with tab_coll:
        st.title("Collaboratori & Documentazione Tecnica")

        COLLABORATORI = [
            ("DAVIDE MERCURIO", "TITOLARE"),
            ("ANTONIO SERIO",   "COLLABORATORE"),
            ("LALA ESAT",       "COLLABORATORE"),
        ]

        if os.path.exists(P_INFO):
            files_info = [f for f in os.listdir(P_INFO) if f.lower().endswith(".pdf")]
        else:
            files_info = []

        for nome, ruolo in COLLABORATORI:
            parole = nome.upper().split()
            docs_c = [f for f in files_info if any(p in f.upper() for p in parole)]

            with st.expander(f"👤 {nome}  ·  {ruolo}", expanded=True):
                if not docs_c:
                    alert("Nessun documento caricato.", "blu", "📂")
                else:
                    for d in docs_c:
                        fp = os.path.join(P_INFO, d)
                        c1, c2, c3 = st.columns([4, 1, 1])
                        c1.write(f"📁 {d}")
                        if c2.button("Apri",  key=f"c_{d}"):
                            apri_doc(fp)
                        if c3.button("🗑️",    key=f"dc_{d}"):
                            st.session_state[f"cc_{d}"] = True
                        if st.session_state.get(f"cc_{d}"):
                            alert(f"Confermi eliminazione di **{d}**?", "rosso", "⚠️")
                            yc_c, nc_c, _ = st.columns([1, 1, 4])
                            if yc_c.button("✅ Sì", key=f"yc_{d}"):
                                elimina_file(fp)
                                del st.session_state[f"cc_{d}"]
                            if nc_c.button("❌ No", key=f"nc_{d}"):
                                del st.session_state[f"cc_{d}"]
                                st.rerun()

                st.markdown("---")
                up_info = st.file_uploader(
                    f"Aggiungi documento per {nome}",
                    key=f"up_info_{nome}",
                    type=["pdf"],
                    label_visibility="visible",
                )
                if up_info:
                    if st.button(f"Salva Documento", key=f"btn_info_{nome}"):
                        prefisso = f"{nome.replace(' ', '_').upper()}_"
                        if salva_file_caricato(up_info, P_INFO, prefisso=prefisso):
                            alert("Documento salvato.", "verde", "✅")
                            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════════
    # 5. REGISTRO DOCUMENTI
    # ════════════════════════════════════════════════════════════════════════════
with tab_reg:
        st.title("Registro Storico Documenti")

        righe = leggi_registro()

        if not righe:
            alert("Nessuna voce nel registro. Le operazioni future verranno tracciate automaticamente.", "blu", "📋")
        else:
            # Filtri
            col_f1, col_f2 = st.columns(2)
            cantieri_unici = sorted(set(r["cantiere"] for r in righe if r["cantiere"]))
            filtro_cant    = col_f1.selectbox("Filtra cantiere", ["Tutti"] + cantieri_unici)
            filtro_op      = col_f2.selectbox("Filtra operazione", ["Tutte", "Creazione Word", "Creazione PDF", "Upload", "Eliminazione"])

            righe_filtrate = [
                r for r in righe
                if (filtro_cant == "Tutti" or r["cantiere"] == filtro_cant)
                and (filtro_op == "Tutte" or r["operazione"] == filtro_op)
            ]

            # Tabella
            st.markdown(
                '<div style="background:var(--grigio-m);border-radius:8px;padding:0.8rem;margin-top:0.5rem;">',
                unsafe_allow_html=True,
            )
            header = st.columns([1, 1, 2, 1, 3, 2])
            for col, testo in zip(header, ["Data", "Ora", "Cantiere", "Tipo", "File", "Operazione"]):
                col.markdown(f"<small style='color:#666666;font-weight:700;text-transform:uppercase;letter-spacing:.05em;'>{testo}</small>", unsafe_allow_html=True)

            st.markdown("<hr style='margin:0.3rem 0;border-color:#808080;'>", unsafe_allow_html=True)

            OP_COLORE = {
                "Creazione Word": "blu",
                "Creazione PDF":  "verde",
                "Upload":         "giallo",
                "Eliminazione":   "rosso",
            }
            for r in reversed(righe_filtrate):
                row_cols = st.columns([1, 1, 2, 1, 3, 2])
                row_cols[0].write(r.get("data", ""))
                row_cols[1].write(r.get("ora", ""))
                row_cols[2].write(r.get("cantiere", ""))
                row_cols[3].write(r.get("tipo_doc", ""))
                row_cols[4].write(r.get("nome_file", ""))
                op = r.get("operazione", "")
                b_tipo = OP_COLORE.get(op, "grigio")
                row_cols[5].markdown(badge_html(op, b_tipo), unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"<small style='color:#555;'>Totale righe: {len(righe_filtrate)}</small>", unsafe_allow_html=True)

    # 5. IMPOSTAZIONI AZIENDALI
    # 
with tab_imp:
        st.title("Impostazioni Aziendali")

        # 
        # Servizi Online
        # 
        st.subheader(" Servizi Online")
        
        # Nuova sezione per il sito web
        st.markdown("""
        <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:10px;padding:1.5rem;margin-bottom:1.5rem;">
            <h3 style="color:var(--rosso-em);margin-bottom:1rem;"> Sito Web Aziendale</h3>
            <p style="color:var(--testo);margin-bottom:1rem;">Accedi al sito web aziendale per visualizzare dati e documenti in tempo reale</p>
            <ul style="color:var(--testo-s);margin-bottom:1rem;">
                <li>Dati cantieri in tempo reale</li>
                <li>Stato attestati e scadenze</li>
                <li>Registro documenti completo</li>
                <li>Anteprime documenti online</li>
                <li>Dati collaboratori aggiornati</li>
            </ul>
            <div style="text-align:center;">
                <a href="https://danielmarzi979.github.io/personal-website" target="_blank" 
                   style="display:inline-block;padding:0.8rem 2rem;background:linear-gradient(135deg, var(--rosso-em), var(--arancio-em));color:white;text-decoration:none;border-radius:6px;font-weight:700;box-shadow:0 4px 8px rgba(0,0,0,0.1);transition:all 0.3s ease;"
                   onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.15)'"
                   onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'">
                   Apri Sito Web
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pulsanti per aggiornamento sito
        st.markdown("---")
        st.subheader(" Aggiornamento Sito Web")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(" Estrai Dati", use_container_width=True, help="Estrae i dati dall'applicazione per il sito web"):
                aggiorna_sito_web()
        
        with col2:
            if st.button(" Deploy Sito", use_container_width=True, help="Estrae dati e carica tutto su GitHub automaticamente"):
                deploy_sito_web()
        
        st.markdown("""
        <div style="background:#f0f8ff;border:1px solid #cce5ff;border-radius:8px;padding:1rem;margin-top:1rem;">
            <h4 style="color:#0066cc;margin-bottom:0.5rem;"> Come funziona:</h4>
            <ol style="color:#333;font-size:0.9rem;margin:0;">
                <li><strong>Estrai Dati:</strong> Estrae i dati dall'applicazione e crea il file JSON</li>
                <li><strong>Deploy Sito:</strong> Estrae dati + Git commit/push automatico su GitHub</li>
                <li>Il sito si aggiorna in 1-2 minuti su GitHub Pages</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        col_email, col_fatt = st.columns(2)
        
        with col_email:
            st.markdown("""
            <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:10px;padding:1.5rem;">
                <h3 style="color:var(--rosso-em);margin-bottom:1rem;"> Casella Postale</h3>
                <p style="color:var(--testo);margin-bottom:1rem;">Accedi alla casella email aziendale</p>
                <ul style="color:var(--testo-s);margin-bottom:1rem;">
                    <li>Posta in arrivo</li>
                    <li>Posta inviata</li>
                    <li>Contatti aziendali</li>
                    <li>Calendario condiviso</li>
                </ul>
                <div style="text-align:center;">
                    <a href="https://mail.google.com" target="_blank" 
                       style="display:inline-block;padding:0.8rem 2rem;background:var(--arancio-em);color:white;text-decoration:none;border-radius:6px;font-weight:700;">
                        Apri Email
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_fatt:
            st.markdown("""
            <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:10px;padding:1.5rem;">
                <h3 style="color:var(--rosso-em);margin-bottom:1rem;"> Sistema Fatturazione</h3>
                <p style="color:var(--testo);margin-bottom:1rem;">Gestione fatture e documenti fiscali</p>
                <ul style="color:var(--testo-s);margin-bottom:1rem;">
                    <li>Creazione fatture</li>
                    <li>Clienti e fornitori</li>
                    <li>Scadenziario</li>
                    <li>Reportistica</li>
                </ul>
                <div style="text-align:center;">
                    <a href="https://asit.cloudwebtec.it/wt00020897/login.sto?Login_Service=https%3A%2F%2Fasit.cloudwebtec.it%2Fwt00020897%2Fcliente.sto&StwTokenSel=3147800398371024&utentebak=|wt00020897" 
                       target="_blank" 
                       style="display:inline-block;padding:0.8rem 2rem;background:var(--arancio-em);color:white;text-decoration:none;border-radius:6px;font-weight:700;">
                        Accedi Fatture
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 
        # Link Utili
        # 
        st.subheader(" Link Utili")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:8px;padding:1rem;text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"> </div>
                <h4 style="color:var(--bordeaux);margin-bottom:0.5rem;">Agenzia Entrate</h4>
                <a href="https://www.agenziaentrate.gov.it" target="_blank" 
                   style="color:var(--rosso-em);text-decoration:none;font-weight:600;">
                    Accedi
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:8px;padding:1rem;text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"> </div>
                <h4 style="color:var(--bordeaux);margin-bottom:0.5rem;">INPS</h4>
                <a href="https://www.inps.it" target="_blank" 
                   style="color:var(--rosso-em);text-decoration:none;font-weight:600;">
                    Accedi
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:8px;padding:1rem;text-align:center;">
                <div style="font-size:2rem;margin-bottom:0.5rem;"> </div>
                <h4 style="color:var(--bordeaux);margin-bottom:0.5rem;">SUAP</h4>
                <a href="https://www.impresainungiorni.gov.it" target="_blank" 
                   style="color:var(--rosso-em);text-decoration:none;font-weight:600;">
                    Accedi
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 
        # Informazioni Aziendali
        # 
        st.subheader(" Informazioni Aziendali")
        
        with st.expander(" Dati Aziendali Completi", expanded=True):
            st.markdown("""
            <div style="background:var(--grigio-m);border:1px solid var(--grigio-c);border-radius:8px;padding:1.5rem;">
                <table style="width:100%;border-collapse:collapse;">
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;width:30%;">Ragione Sociale:</td>
                        <td style="padding:0.5rem;color:var(--testo);font-weight:600;">EDILMERC DI MERCURIO DAVIDE</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">Partita IVA:</td>
                        <td style="padding:0.5rem;color:var(--testo);">02964520352</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">Codice Fiscale Direttore Lavori:</td>
                        <td style="padding:0.5rem;color:var(--testo);">MRCDVD89A10H223F</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">PEC:</td>
                        <td style="padding:0.5rem;color:var(--testo);">edilmerc@legalmail.it</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">Email:</td>
                        <td style="padding:0.5rem;color:var(--testo);">info@edilmerc.it</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">Telefono:</td>
                        <td style="padding:0.5rem;color:var(--testo);">+39 0522 123456</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">Indirizzo:</td>
                        <td style="padding:0.5rem;color:var(--testo);">Via G. Venturi 43, 42021 Bibbiano (RE)</td>
                    </tr>
                    <tr>
                        <td style="padding:0.5rem;color:var(--testo-s);font-weight:600;">Coordinate Bancarie:</td>
                        <td style="padding:0.5rem;color:var(--testo);">IT 08 L 02008 66250 000106132902</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
