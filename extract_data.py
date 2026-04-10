#!/usr/bin/env python3
"""
Script per estrarre dati reali dall'applicazione Streamlit EDILMERC
e generarli in formato JSON per il sito web
"""

import os
import json
import csv
from datetime import datetime

# Percorsi base - modifica secondo la tua configurazione
P_BASE = "G:\\Il mio Drive\\EdilMerc"
P_SICUREZZA = os.path.join(P_BASE, "Sicurezza_Cantieri")
P_ATT = os.path.join(P_BASE, "Attestati")
P_INFO = os.path.join(P_BASE, "Info")
P_REGISTRO = os.path.join(P_BASE, "registro_documenti.csv")
P_SCADENZE = os.path.join(P_BASE, "scadenze_attestati.json")

def estrai_cantieri():
    """Estrae i dati dei cantieri"""
    cantieri = []
    
    if not os.path.exists(P_SICUREZZA):
        print("Cartella Sicurezza_Cantieri non trovata")
        return cantieri
    
    for cartella in os.listdir(P_SICUREZZA):
        path_c = os.path.join(P_SICUREZZA, cartella)
        if os.path.isdir(path_c):
            # Leggi stato.json se esiste
            stato_file = os.path.join(path_c, "stato.json")
            stato = {}
            if os.path.exists(stato_file):
                try:
                    with open(stato_file, encoding="utf-8") as f:
                        stato = json.load(f)
                except:
                    pass
            
            # Elenca documenti
            documenti = []
            if os.path.exists(path_c):
                for file in os.listdir(path_c):
                    if file.endswith(('.docx', '.pdf')):
                        tipo = 'POS' if 'POS' in file.upper() else 'PiMUS' if 'PIMUS' in file.upper() else 'DUVRI' if 'DUVRI' in file.upper() else 'Altro'
                        documenti.append({
                            "nome": file,
                            "tipo": tipo
                        })
            
            cantiere = {
                "id": cartella,
                "nome": stato.get("nome", cartella),
                "stato": stato.get("stato", "sconosciuto"),
                "indirizzo": stato.get("indirizzo", ""),
                "committente": stato.get("committente", ""),
                "direttoreLavori": stato.get("direttoreLavori", ""),
                "nLavoratori": stato.get("nLavoratori", 0),
                "dataInizio": stato.get("dataInizio", ""),
                "dataFine": stato.get("dataFine", ""),
                "documenti": documenti
            }
            cantieri.append(cantiere)
    
    return cantieri

def estrai_attestati():
    """Estrae i dati degli attestati"""
    attestati = []
    
    if not os.path.exists(P_ATT):
        print("Cartella Attestati non trovata")
        return attestati
    
    # Leggi scadenze se esiste
    scadenze = {}
    if os.path.exists(P_SCADENZE):
        try:
            with open(P_SCADENZE, encoding="utf-8") as f:
                scadenze = json.load(f)
        except:
            pass
    
    for file in os.listdir(P_ATT):
        if file.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            # Estrai nome dal filename
            nome = file.split('_')[0] if '_' in file else os.path.splitext(file)[0]
            
            # Determina tipo
            tipo = 'POS' if 'POS' in file.upper() else 'PiMUS' if 'PIMUS' in file.upper() else 'Altro'
            
            # Controlla scadenza
            oggi = datetime.now()
            scadenza_str = scadenze.get(nome, "")
            stato = "valido"
            
            if scadenza_str:
                try:
                    data_scadenza = datetime.strptime(scadenza_str, "%Y-%m-%d")
                    giorni_mancanti = (data_scadenza - oggi).days
                    
                    if giorni_mancanti < 0:
                        stato = "scaduto"
                    elif giorni_mancanti <= 30:
                        stato = "in_scadenza"
                except:
                    stato = "sconosciuto"
            
            attestato = {
                "id": f"ATT-{nome}",
                "collaboratore": nome,
                "tipo": tipo,
                "scadenza": scadenza_str,
                "stato": stato,
                "file": file
            }
            attestati.append(attestato)
    
    return attestati

def estrai_collaboratori():
    """Estrae i dati dei collaboratori"""
    collaboratori = []
    
    if not os.path.exists(P_INFO):
        print("Cartella Info non trovata")
        return collaboratori
    
    for file in os.listdir(P_INFO):
        if file.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.docx')):
            # Estrai nome dal filename
            nome = os.path.splitext(file)[0]
            
            collaboratore = {
                "id": f"COL-{nome}",
                "nome": nome,
                "ruolo": "Collaboratore",
                "telefono": "",
                "email": "",
                "dataAssunzione": "",
                "stato": "attivo",
                "file": file
            }
            collaboratori.append(collaboratore)
    
    return collaboratori

def estrai_registro():
    """Estrae i dati dal registro documenti"""
    registro = []
    
    if not os.path.exists(P_REGISTRO):
        print("File registro_documenti.csv non trovato")
        return registro
    
    try:
        with open(P_REGISTRO, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = {
                    "data": row.get("data", ""),
                    "ora": row.get("ora", ""),
                    "cantiere": row.get("cantiere", ""),
                    "tipo": row.get("tipo_doc", ""),
                    "nomeFile": row.get("nome_file", ""),
                    "operazione": row.get("operazione", "")
                }
                registro.append(doc)
    except Exception as e:
        print(f"Errore leggendo registro: {e}")
    
    return registro

def genera_dati_sito():
    """Genera il file JSON con tutti i dati per il sito"""
    print("Estrazione dati EDILMERC...")
    
    # Estrai tutti i dati
    cantieri = estrai_cantieri()
    attestati = estrai_attestati()
    collaboratori = estrai_collaboratori()
    registro = estrai_registro()
    
    # Crea il dizionario completo
    dati_completi = {
        "cantieri": cantieri,
        "attestati": attestati,
        "collaboratori": collaboratori,
        "registro": registro,
        "ultima_modifica": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    # Salva il file JSON
    output_file = "dati_reali_edilmerc.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dati_completi, f, ensure_ascii=False, indent=2)
        
        print(f"Dati salvati in {output_file}")
        print(f"- Cantieri: {len(cantieri)}")
        print(f"- Attestati: {len(attestati)}")
        print(f"- Collaboratori: {len(collaboratori)}")
        print(f"- Documenti registro: {len(registro)}")
        
        return True
        
    except Exception as e:
        print(f"Errore salvando dati: {e}")
        return False

if __name__ == "__main__":
    genera_dati_sito()
