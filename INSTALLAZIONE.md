# 🚀 Installazione ed Esecuzione EDILMERC 2026

## 📋 Prerequisiti
- Python 3.8+ installato
- Accesso a internet per l'installazione

---

## 🔧 Installazione Dipendenze

### 1. Apri il terminale (Prompt dei comandi)
**Windows:** `Win + R` → scrivi `cmd` → Invio

### 2. Naviga alla cartella del progetto
```cmd
cd "c:\Users\danie\OneDrive\Desktop\CascadeProjects\personal-website"
```

### 3. Installa Streamlit e le dipendenze
```cmd
pip install streamlit
pip install docxtpl
pip install docx2pdf
pip install python-docx
```

---

## 🏃 Esecuzione dell'Applicazione

### Metodo 1: Esecuzione diretta
```cmd
streamlit run modified_edilmerc.py
```

### Metodo 2: Esecuzione su porta specifica
```cmd
streamlit run modified_edilmerc.py --server.port 8501
```

---

## 🌐 Apri l'Applicazione

Dopo l'esecuzione:
1. Il terminale mostrerà un URL locale (solitamente: `http://localhost:8501`)
2. Apri il tuo browser (Chrome, Edge, Firefox)
3. Naviga all'URL mostrato nel terminale
4. L'applicazione si aprirà con il nuovo tema grigio chiaro!

---

## ⚠️ Note Importanti

- **G:Drive**: L'app cerca automaticamente `G:\Il mio Drive\EdilMerc`
- **Documenti Word**: Assicurati di avere i modelli POS e PiMUS nella cartella
- **Conversione PDF**: Richiede Word installato o libreria docx2pdf
- **Backup**: I backup vengono salvati in `G:\Il mio Drive\EdilMerc\_Backup`

---

## 🔧 Risoluzione Problemi

### Se Streamlit non è installato:
```cmd
pip install --upgrade pip
pip install streamlit
```

### Se ci sono errori di dipendenze:
```cmd
pip install -r requirements.txt
```

### Se la porta 8501 è occupata:
```cmd
streamlit run modified_edilmerc.py --server.port 8502
```

---

## 🎨 Modifiche Applicate

✅ **Background cambiato da nero (#111111) a grigio chiaro (#D3D3D3)**
✅ **Testo adattato per migliore leggibilità su sfondo chiaro**
✅ **Colori sidebar e componenti aggiornati**
✅ **Tema professionale mantenuto con accento arancione**
