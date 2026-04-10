// Dati EDILMERC
let edilmercData = {
    cantieri: [],
    attestati: [],
    collaboratori: [],
    registro: []
};

// Inizializzazione quando il DOM è caricato
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM caricato - inizio caricamento dati');
    caricaDati();
    setupTabNavigation();
});

// Funzione principale per caricare i dati
async function caricaDati() {
    try {
        // Prova a caricare dati reali
        const response = await fetch('dati_reali_edilmerc.json');
        
        if (response.ok) {
            edilmercData = await response.json();
            console.log('Dati reali caricati:', edilmercData);
        } else {
            console.log('File JSON non trovato, uso dati di esempio');
            caricaDatiEsempio();
        }
    } catch (error) {
        console.log('Errore caricamento JSON, uso dati di esempio:', error);
        caricaDatiEsempio();
    }
    
    // Aggiorna l'interfaccia
    aggiornaInterfaccia();
}

// Dati di esempio come fallback
function caricaDatiEsempio() {
    edilmercData = {
        cantieri: [
            {
                id: 'CANT-001',
                nome: 'Ristrutturazione Edificio Residenziale',
                committente: 'Mario Rossi',
                indirizzo: 'Via G. Venturi 43, Bibbiano (RE)',
                direttoreLavori: 'Ing. Bianchi',
                nLavoratori: 8,
                dataInizio: '2026-01-15',
                dataFine: '2026-04-30',
                stato: 'in_corso'
            },
            {
                id: 'CANT-002',
                nome: 'Ristrutturazione Ufficio Commerciale',
                committente: 'SRL Costruzioni',
                indirizzo: 'Via Roma 123, Reggio Emilia',
                direttoreLavori: 'Ing. Verdi',
                nLavoratori: 12,
                dataInizio: '2026-02-01',
                dataFine: '2026-07-15',
                stato: 'in_corso'
            }
        ],
        attestati: [
            {
                id: 'ATT-001',
                collaboratore: 'Mario Rossi',
                tipo: 'POS',
                scadenza: '2026-12-31',
                stato: 'valido'
            },
            {
                id: 'ATT-002',
                collaboratore: 'Luca Bianchi',
                tipo: 'PiMUS',
                scadenza: '2026-08-15',
                stato: 'in_scadenza'
            },
            {
                id: 'ATT-003',
                collaboratore: 'Giuseppe Verdi',
                tipo: 'DUVRI',
                scadenza: '2026-05-01',
                stato: 'scaduto'
            }
        ],
        collaboratori: [
            {
                id: 'COL-001',
                nome: 'Mario Rossi',
                ruolo: 'Operaio Specializzato',
                telefono: '+39 333 1234567',
                email: 'mario.rossi@edilmerc.it',
                dataAssunzione: '2023-01-15',
                stato: 'attivo'
            },
            {
                id: 'COL-002',
                nome: 'Luca Bianchi',
                ruolo: 'Capo Cantiere',
                telefono: '+39 333 9876543',
                email: 'luca.bianchi@edilmerc.it',
                dataAssunzione: '2022-06-01',
                stato: 'attivo'
            }
        ],
        registro: [
            {
                data: '2026-04-10',
                ora: '14:30',
                cantiere: 'CANT-001',
                tipo: 'POS',
                nomeFile: 'POS_CANT-001_20260410.docx',
                operazione: 'Creazione Word'
            },
            {
                data: '2026-04-10',
                ora: '14:45',
                cantiere: 'CANT-002',
                tipo: 'PiMUS',
                nomeFile: 'PiMUS_CANT-002_20260410.docx',
                operazione: 'Creazione Word'
            }
        ]
    };
}

// Aggiorna tutta l'interfaccia
function aggiornaInterfaccia() {
    console.log('Aggiornamento interfaccia');
    aggiornaKPI();
    aggiornaCantieri();
    aggiornaAttestati();
    aggiornaCollaboratori();
    aggiornaRegistro();
}

// Aggiorna KPI
function aggiornaKPI() {
    // Cantieri attivi
    const cantieriAttivi = edilmercData.cantieri.filter(c => c.stato === 'in_corso').length;
    document.getElementById('cantieri-count').textContent = cantieriAttivi;
    
    // Attestati per stato
    const attestatiValidi = edilmercData.attestati.filter(a => a.stato === 'valido').length;
    const attestatiScadenza = edilmercData.attestati.filter(a => a.stato === 'in_scadenza').length;
    const attestatiScaduti = edilmercData.attestati.filter(a => a.stato === 'scaduto').length;
    
    document.getElementById('attestati-validi').textContent = attestatiValidi;
    document.getElementById('attestati-scadenza').textContent = attestatiScadenza;
    document.getElementById('attestati-scaduti').textContent = attestatiScaduti;
}

// Aggiorna cantieri
function aggiornaCantieri() {
    const container = document.getElementById('cantieri-list');
    
    if (!edilmercData.cantieri || edilmercData.cantieri.length === 0) {
        container.innerHTML = '<p>Nessun cantiere trovato</p>';
        return;
    }
    
    let html = '<div class="cantieri-list">';
    edilmercData.cantieri.forEach(cantiere => {
        html += `
            <div class="card">
                <h4>${cantiere.nome}</h4>
                <p><strong>Comune:</strong> ${cantiere.committente}</p>
                <p><strong>Indirizzo:</strong> ${cantiere.indirizzo}</p>
                <p><strong>Lavoratori:</strong> ${cantiere.nLavoratori}</p>
                <p><strong>Periodo:</strong> ${cantiere.dataInizio} - ${cantiere.dataFine}</p>
                <p><strong>Stato:</strong> ${cantiere.stato}</p>
            </div>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

// Aggiorna attestati
function aggiornaAttestati() {
    const container = document.getElementById('attestati-list');
    
    if (!edilmercData.attestati || edilmercData.attestati.length === 0) {
        container.innerHTML = '<p>Nessun attestato trovato</p>';
        return;
    }
    
    let html = '<div class="attestati-list">';
    edilmercData.attestati.forEach(attestato => {
        html += `
            <div class="card stato-${attestato.stato}">
                <h4>${attestato.collaboratore}</h4>
                <p><strong>Tipo:</strong> ${attestato.tipo}</p>
                <p><strong>Scadenza:</strong> ${attestato.scadenza}</p>
                <p><strong>Stato:</strong> ${attestato.stato}</p>
            </div>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

// Aggiorna collaboratori
function aggiornaCollaboratori() {
    const container = document.getElementById('collaboratori-list');
    
    if (!edilmercData.collaboratori || edilmercData.collaboratori.length === 0) {
        container.innerHTML = '<p>Nessun collaboratore trovato</p>';
        return;
    }
    
    let html = '<div class="collaboratori-list">';
    edilmercData.collaboratori.forEach(collaboratore => {
        html += `
            <div class="card">
                <h4>${collaboratore.nome}</h4>
                <p><strong>Ruolo:</strong> ${collaboratore.ruolo}</p>
                <p><strong>Telefono:</strong> ${collaboratore.telefono}</p>
                <p><strong>Email:</strong> ${collaboratore.email}</p>
                <p><strong>Assunzione:</strong> ${collaboratore.dataAssunzione}</p>
                <p><strong>Stato:</strong> ${collaboratore.stato}</p>
            </div>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

// Aggiorna registro
function aggiornaRegistro() {
    const container = document.getElementById('registro-list');
    
    if (!edilmercData.registro || edilmercData.registro.length === 0) {
        container.innerHTML = '<p>Nessun documento nel registro</p>';
        return;
    }
    
    let html = '<table class="registro-table"><thead><tr><th>Data</th><th>Ora</th><th>Cantiere</th><th>Tipo</th><th>File</th><th>Operazione</th></tr></thead><tbody>';
    
    edilmercData.registro.slice().reverse().forEach(doc => {
        html += `
            <tr>
                <td>${doc.data}</td>
                <td>${doc.ora}</td>
                <td>${doc.cantiere}</td>
                <td>${doc.tipo}</td>
                <td>${doc.nomeFile}</td>
                <td>${doc.operazione}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    
    container.innerHTML = html;
}

// Setup tab navigation
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Rimuovi active da tutti i bottoni e contenuti
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Aggiungi active al bottone cliccato e al contenuto corrispondente
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}
