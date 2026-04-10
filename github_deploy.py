#!/usr/bin/env python3
"""
Script per deploy automatico su GitHub Pages
Aggiorna i dati e fa commit/push su GitHub
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def deploy_to_github():
    """Deploy automatico su GitHub Pages"""
    try:
        print("=== DEPLOY AUTOMATICO GITHUB PAGES ===")
        
        # 1. Estrai dati reali dall'app Streamlit
        print("1. Estrazione dati reali...")
        extract_script = os.path.join(os.path.dirname(__file__), "extract_data.py")
        
        if os.path.exists(extract_script):
            result = subprocess.run([sys.executable, extract_script], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("   Dati estratti con successo")
                print(f"   {result.stdout}")
            else:
                print(f"   Errore estrazione dati: {result.stderr}")
                return False
        else:
            print("   Script extract_data.py non trovato, uso dati di esempio")
            # Crea dati di esempio se non ci sono dati reali
            crea_dati_esempio()
        
        # 2. Git add, commit, push
        print("2. Commit e push su GitHub...")
        
        # Git commands
        commands = [
            ["git", "add", "."],
            ["git", "status"],
            ["git", "commit", "-m", f"Aggiornamento dati - {datetime.now().strftime('%d/%m/%Y %H:%M')}"],
            ["git", "push", "origin", "main"]
        ]
        
        for cmd in commands:
            print(f"   Eseguo: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                if cmd[1] == "status":
                    print(f"   Status: {result.stdout}")
                else:
                    print(f"   Completato")
            else:
                print(f"   Errore: {result.stderr}")
                if "nothing to commit" in result.stderr.lower():
                    print("   Nessuna modifica da committare")
                    return True
                return False
        
        print("3. Deploy completato!")
        print("   Il sito sarà aggiornato su GitHub Pages in pochi minuti")
        
        return True
        
    except Exception as e:
        print(f"Errore durante deploy: {e}")
        return False

def crea_dati_esempio():
    """Crea dati di esempio se non ci sono dati reali"""
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
            }
        ],
        "attestati": [
            {
                "id": "ATT-001",
                "collaboratore": "Mario Rossi",
                "tipo": "POS",
                "scadenza": "2026-12-31",
                "stato": "valido",
                "cantiere": "CANT-2026-001"
            }
        ],
        "collaboratori": [
            {
                "id": "COL-001",
                "nome": "Mario Rossi",
                "ruolo": "Operaio Specializzato Edile",
                "telefono": "+39 333 1234567",
                "email": "mario.rossi@edilmerc.it",
                "dataAssunzione": "2023-01-15",
                "stato": "attivo"
            }
        ],
        "registro": [
            {
                "data": "2026-01-15",
                "ora": "09:30",
                "cantiere": "CANT-2026-001",
                "tipo": "POS",
                "nomeFile": "POS_CANT-2026-001.docx",
                "operazione": "Creazione Word"
            }
        ]
    }
    
    with open("dati_reali_edilmerc.json", "w", encoding="utf-8") as f:
        json.dump(dati_esempio, f, ensure_ascii=False, indent=2)
    
    print("   Creati dati di esempio")

if __name__ == "__main__":
    deploy_to_github()
