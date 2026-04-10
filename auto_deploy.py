#!/usr/bin/env python3
"""
Script di deploy automatico per il sito EDILMERC
Estrae i dati e carica tutto su GitHub automaticamente
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def deploy_automatico():
    """Deploy automatico completo su GitHub"""
    try:
        print("=== DEPLOY AUTOMATICO EDILMERC ===")
        print(f"Orario: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        # 1. Esegui estrazione dati
        print("1. Estrazione dati reali...")
        extract_script = "extract_data.py"
        
        if os.path.exists(extract_script):
            result = subprocess.run([sys.executable, extract_script], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("   Dati estratti con successo")
                print(f"   {result.stdout}")
            else:
                print(f"   Errore estrazione: {result.stderr}")
                return False
        else:
            print("   Script extract_data.py non trovato")
            return False
        
        # 2. Controlla se ci sono modifiche
        print("2. Controllo modifiche...")
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        
        if not result.stdout.strip():
            print("   Nessuna modifica da committare")
            print("   Sito già aggiornato!")
            return True
        
        print(f"   Modifiche trovate: {len(result.stdout.splitlines())} file")
        
        # 3. Git add
        print("3. Aggiunta file al repository...")
        result = subprocess.run(["git", "add", "."], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   Errore git add: {result.stderr}")
            return False
        print("   File aggiunti con successo")
        
        # 4. Git commit
        print("4. Creazione commit...")
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        commit_msg = f"Auto-deploy - {timestamp}"
        
        result = subprocess.run(["git", "commit", "-m", commit_msg], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            if "nothing to commit" in result.stderr.lower():
                print("   Nessuna modifica da committare")
                return True
            print(f"   Errore git commit: {result.stderr}")
            return False
        print(f"   Commit creato: {commit_msg}")
        
        # 5. Git push
        print("5. Caricamento su GitHub...")
        result = subprocess.run(["git", "push", "origin", "main"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   Errore git push: {result.stderr}")
            return False
        print("   Push completato con successo!")
        
        # 6. Mostra statistiche
        print()
        print("=== RIEPILOGO ===")
        
        # Leggi il JSON per statistiche
        if os.path.exists("dati_reali_edilmerc.json"):
            with open("dati_reali_edilmerc.json", "r", encoding="utf-8") as f:
                dati = json.load(f)
            
            print(f"   Cantieri: {len(dati.get('cantieri', []))}")
            print(f"   Attestati: {len(dati.get('attestati', []))}")
            print(f"   Collaboratori: {len(dati.get('collaboratori', []))}")
            print(f"   Documenti registro: {len(dati.get('registro', []))}")
        
        print()
        print("=== SITO AGGIORNATO! ===")
        print("URL: https://danielmarzi979.github.io/personal-website")
        print("Il sito sarà online in 1-2 minuti")
        
        return True
        
    except Exception as e:
        print(f"Errore durante deploy automatico: {e}")
        return False

def deploy_senza_estrazione():
    """Deploy solo se ci sono già dati estratti"""
    try:
        print("=== DEPLOY RAPIDO EDILMERC ===")
        
        # Controlla se esiste il JSON
        if not os.path.exists("dati_reali_edilmerc.json"):
            print("File dati_reali_edilmerc.json non trovato")
            print("Esegui prima l'estrazione completa")
            return False
        
        # Git add, commit, push
        subprocess.run(["git", "add", "."], check=True)
        
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        commit_msg = f"Quick deploy - {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("Deploy rapido completato!")
        return True
        
    except Exception as e:
        print(f"Errore deploy rapido: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        deploy_senza_estrazione()
    else:
        deploy_automatico()
