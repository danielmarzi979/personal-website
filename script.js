// Dati EDILMERC - verranno caricati dal file JSON
let edilmercData = {
    cantieri: [],
    attestati: [],
    collaboratori: [],
    registro: []
};

// Funzione per caricare dati reali dal file JSON
async function caricaDatiReali() {
    try {
        console.log('Tentativo caricamento dati reali...');
        const response = await fetch('dati_reali_edilmerc.json');
        
        if (response.ok) {
            edilmercData = await response.json();
            console.log('✅ Dati reali caricati con successo:', edilmercData);
            aggiornaInterfaccia();
            mostraNotifica('Dati reali caricati con successo', 'successo');
        } else {
            // Se il file non esiste, mostra errore specifico
            console.warn('⚠️ File dati_reali_edilmerc.json non trovato (status:', response.status);
            mostraNotifica('File dati non trovato. Esegui extract_data.py nell\'applicazione Streamlit per generare i dati reali.', 'errore');
            caricaDatiEsempio();
        }
    } catch (error) {
        console.error('❌ Errore caricamento dati:', error);
        mostraNotifica('Errore nel caricamento dei dati: ' + error.message, 'errore');
        caricaDatiEsempio();
    }
}

// Dati di esempio come fallback
function caricaDatiEsempio() {
    edilmercData = {
        cantieri: [
            {
                id: 'CANT-2026-001',
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
                id: 'CANT-2026-002',
                nome: 'Ristrutturazione Ufficio Commerciale',
                committente: 'SRL Costruzioni Modenesi',
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
                stato: 'valido',
                cantiere: 'CANT-2026-001'
            },
            {
                id: 'ATT-002',
                collaboratore: 'Luca Bianchi',
                tipo: 'PiMUS',
                scadenza: '2026-08-15',
                stato: 'in_scadenza',
                cantiere: 'CANT-2026-002'
            },
            {
                id: 'ATT-003',
                collaboratore: 'Giuseppe Verdi',
                tipo: 'DUVRI',
                scadenza: '2026-05-01',
                stato: 'scaduto',
                cantiere: 'CANT-2026-001'
            }
        ],
        collaboratori: [
            {
                id: 'COL-001',
                nome: 'Mario Rossi',
                ruolo: 'Operaio Specializzato Edile',
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
            },
            {
                id: 'COL-003',
                nome: 'Giuseppe Verdi',
                ruolo: 'Tecnico della Sicurezza',
                telefono: '+39 333 5558889',
                email: 'giuseppe.verdi@edilmerc.it',
                dataAssunzione: '2021-03-10',
                stato: 'attivo'
            }
        ],
        registro: [
            {
                data: '2026-01-15',
                ora: '09:30',
                cantiere: 'CANT-2026-001',
                tipo: 'POS',
                nomeFile: 'POS_CANT-2026-001.docx',
                operazione: 'Creazione Word'
            },
            {
                data: '2026-01-15',
                ora: '10:15',
                cantiere: 'CANT-2026-001',
                tipo: 'POS',
                nomeFile: 'POS_CANT-2026-001.pdf',
                operazione: 'Creazione PDF'
            },
            {
                data: '2026-01-16',
                ora: '14:20',
                cantiere: 'CANT-2026-002',
                tipo: 'PiMUS',
                nomeFile: 'PiMUS_CANT-2026-002.docx',
                operazione: 'Creazione Word'
            },
            {
                data: '2026-01-17',
                ora: '11:45',
                cantiere: 'CANT-2026-001',
                tipo: 'DUVRI',
                nomeFile: 'DUVRI_CANT-2026-001.pdf',
                operazione: 'Creazione PDF'
            },
            {
                data: '2026-01-18',
                ora: '16:00',
                cantiere: 'CANT-2026-002',
                tipo: 'Backup',
                nomeFile: 'backup_20260118_160000.zip',
                operazione: 'Backup Automatico'
            }
        ]
    };
    aggiornaInterfaccia();
}

// Funzione per aggiornare l'interfaccia con i dati caricati
function aggiornaInterfaccia() {
    // Nascondi messaggi di caricamento
    nascondiMessaggiCaricamento();
    
    // Aggiorna KPI
    aggiornaKPI();
    
    // Aggiorna sezioni
    caricaCantieri();
    caricaAttestati();
    caricaCollaboratori();
    caricaRegistro();
    
    console.log('Interfaccia aggiornata con dati reali');
}

// Funzione per nascondere i messaggi di caricamento
function nascondiMessaggiCaricamento() {
    const loadingMessages = document.querySelectorAll('.loading-message');
    loadingMessages.forEach(msg => {
        if (msg && msg.parentNode) {
            msg.style.display = 'none';
        }
    });
}

// Funzione per aggiornare i KPI
function aggiornaKPI() {
    const cantieriAttivi = edilmercData.cantieri.filter(c => c.stato === 'in_corso').length;
    const attestatiValidi = edilmercData.attestati.filter(a => a.stato === 'valido').length;
    const attestatiInScadenza = edilmercData.attestati.filter(a => a.stato === 'in_scadenza').length;
    const attestatiScaduti = edilmercData.attestati.filter(a => a.stato === 'scaduto').length;
    
    // Aggiorna i valori KPI nell'HTML
    const kpiCantieri = document.querySelector('.kpi-cantieri .kpi-value');
    const kpiValidi = document.querySelector('.kpi-validi .kpi-value');
    const kpiScadenza = document.querySelector('.kpi-scadenza .kpi-value');
    const kpiScaduti = document.querySelector('.kpi-scaduti .kpi-value');
    
    if (kpiCantieri) kpiCantieri.textContent = cantieriAttivi;
    if (kpiValidi) kpiValidi.textContent = attestatiValidi;
    if (kpiScadenza) kpiScadenza.textContent = attestatiInScadenza;
    if (kpiScaduti) kpiScaduti.textContent = attestatiScaduti;
}

// Funzione per caricare i cantieri
function caricaCantieri() {
    const container = document.querySelector('.cantieri-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (edilmercData.cantieri.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--testo-s); padding: 2rem;">Nessun cantiere trovato</p>';
        return;
    }
    
    edilmercData.cantieri.forEach(cantiere => {
        const card = document.createElement('div');
        card.className = 'cantiere-card';
        card.innerHTML = `
            <div class="cantiere-header">
                <h3>${cantiere.nome}</h3>
                <span class="stato-badge stato-${cantiere.stato}">${cantiere.stato.replace('_', ' ').toUpperCase()}</span>
            </div>
            <div class="cantiere-details">
                <p><strong>Committente:</strong> ${cantiere.committente || 'Non specificato'}</p>
                <p><strong>Indirizzo:</strong> ${cantiere.indirizzo || 'Non specificato'}</p>
                <p><strong>Direttore Lavori:</strong> ${cantiere.direttoreLavori || 'Non specificato'}</p>
                <p><strong>Lavoratori:</strong> ${cantiere.nLavoratori || 0}</p>
                <p><strong>Periodo:</strong> ${cantiere.dataInizio || 'Non specificato'} - ${cantiere.dataFine || 'Non specificato'}</p>
            </div>
            <div class="cantiere-actions">
                <button class="btn btn-primary" onclick="visualizzaDocumenti('${cantiere.id}')">Visualizza Documenti</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Funzione per caricare gli attestati
function caricaAttestati() {
    const container = document.querySelector('.attestati-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (edilmercData.attestati.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--testo-s); padding: 2rem;">Nessun attestato trovato</p>';
        return;
    }
    
    edilmercData.attestati.forEach(attestato => {
        const card = document.createElement('div');
        card.className = 'attestato-card';
        card.innerHTML = `
            <div class="attestato-header">
                <h3>${attestato.collaboratore}</h3>
                <span class="tipo-badge tipo-${attestato.tipo.toLowerCase()}">${attestato.tipo}</span>
            </div>
            <div class="attestato-details">
                <p><strong>Scadenza:</strong> ${attestato.scadenza}</p>
                <p><strong>Stato:</strong> <span class="stato-badge stato-${attestato.stato}">${attestato.stato.replace('_', ' ').toUpperCase()}</span></p>
                <p><strong>Cantiere:</strong> ${attestato.cantiere}</p>
            </div>
            <div class="attestato-actions">
                <button class="btn btn-secondary" onclick="anteprimaDocumento('${attestato.file}')">Anteprima</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Funzione per caricare i collaboratori
function caricaCollaboratori() {
    const container = document.querySelector('.collaboratori-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (edilmercData.collaboratori.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--testo-s); padding: 2rem;">Nessun collaboratore trovato</p>';
        return;
    }
    
    edilmercData.collaboratori.forEach(collaboratore => {
        const card = document.createElement('div');
        card.className = 'collaboratore-card';
        card.innerHTML = `
            <div class="collaboratore-header">
                <h3>${collaboratore.nome}</h3>
                <span class="ruolo-badge">${collaboratore.ruolo}</span>
            </div>
            <div class="collaboratore-details">
                <p><strong>Telefono:</strong> ${collaboratore.telefono}</p>
                <p><strong>Email:</strong> ${collaboratore.email}</p>
                <p><strong>Data Assunzione:</strong> ${collaboratore.dataAssunzione}</p>
                <p><strong>Stato:</strong> <span class="stato-badge stato-${collaboratore.stato}">${collaboratore.stato.toUpperCase()}</span></p>
            </div>
            <div class="collaboratore-actions">
                <button class="btn btn-secondary" onclick="anteprimaDocumento('${collaboratore.file}')">Anteprima Documento</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// Funzione per caricare il registro documenti
function caricaRegistro() {
    const container = document.querySelector('.registro-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (edilmercData.registro.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--testo-s); padding: 2rem;">Nessun documento nel registro</p>';
        return;
    }
    
    // Crea tabella
    const table = document.createElement('table');
    table.className = 'registro-table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Data</th>
                <th>Ora</th>
                <th>Cantiere</th>
                <th>Tipo</th>
                <th>Nome File</th>
                <th>Operazione</th>
                <th>Azioni</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;
    
    const tbody = table.querySelector('tbody');
    edilmercData.registro.forEach(doc => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${doc.data}</td>
            <td>${doc.ora}</td>
            <td>${doc.cantiere}</td>
            <td><span class="tipo-badge tipo-${doc.tipo.toLowerCase()}">${doc.tipo}</span></td>
            <td>${doc.nomeFile}</td>
            <td>${doc.operazione}</td>
            <td>
                <button class="btn btn-sm btn-secondary" onclick="anteprimaDocumento('${doc.nomeFile}')">Anteprima</button>
            </td>
        `;
        tbody.appendChild(row);
    });
    
    container.appendChild(table);
}

// Funzione per visualizzare l'anteprima di un documento
function anteprimaDocumento(nomeFile) {
    // Mostra un modal con l'anteprima del documento
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Anteprima Documento</h2>
                <button class="modal-close" onclick="chiudiModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                <h3>${nomeFile}</h3>
                <p>Anteprima del documento non disponibile in questa demo.</p>
                <p>In una versione completa, qui verrebbe mostrato il contenuto del documento.</p>
                <div style="text-align: center; margin-top: 1rem;">
                    <button class="btn btn-primary" onclick="chiudiModal(this)">Chiudi</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

// Funzione per visualizzare i documenti di un cantiere
function visualizzaDocumenti(cantiereId) {
    const cantiere = edilmercData.cantieri.find(c => c.id === cantiereId);
    if (!cantiere || !cantiere.documenti) {
        alert('Nessun documento trovato per questo cantiere');
        return;
    }
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Documenti - ${cantiere.nome}</h2>
                <button class="modal-close" onclick="chiudiModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                <div class="documenti-list">
                    ${cantiere.documenti.map(doc => `
                        <div class="documento-item">
                            <span class="documento-nome">${doc.nome}</span>
                            <span class="documento-tipo tipo-${doc.tipo.toLowerCase()}">${doc.tipo}</span>
                            <button class="btn btn-sm btn-secondary" onclick="anteprimaDocumento('${doc.nome}')">Anteprima</button>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

// Funzione per chiudere i modal
function chiudiModal(button) {
    const modal = button.closest('.modal');
    if (modal) {
        modal.remove();
    }
}

// Funzione per mostrare notifiche all'utente
function mostraNotifica(messaggio, tipo = 'info') {
    // Rimuovi notifiche esistenti
    const notificaEsistente = document.querySelector('.notifica-fluttuante');
    if (notificaEsistente) {
        notificaEsistente.remove();
    }
    
    // Crea nuova notifica
    const notifica = document.createElement('div');
    notifica.className = `notifica-fluttuante notifica-${tipo}`;
    notifica.innerHTML = `
        <div class="notifica-contenuto">
            <span class="notifica-icona">${tipo === 'successo' ? '✅' : tipo === 'errore' ? '❌' : 'ℹ️'}</span>
            <span class="notifica-testo">${messaggio}</span>
            <button class="notifica-chiudi" onclick="chiudiNotifica(this)">&times;</button>
        </div>
    `;
    
    // Stile CSS per la notifica
    notifica.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${tipo === 'successo' ? 'var(--verde-em)' : tipo === 'errore' ? 'var(--rosso-em)' : 'var(--arancio-em)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        animation: scivolaDestra 0.3s ease-out;
    `;
    
    document.body.appendChild(notifica);
    
    // Auto-rimozione dopo 5 secondi
    setTimeout(() => {
        if (document.body.contains(notifica)) {
            notifica.remove();
        }
    }, 5000);
}

// Funzione per chiudere notifica
function chiudiNotifica(button) {
    const notifica = button.closest('.notifica-fluttuante');
    if (notifica) {
        notifica.style.animation = 'scivolaDestra 0.3s ease-in reverse';
        setTimeout(() => notifica.remove(), 300);
    }
}

// Inizializzazione quando il DOM è caricato
document.addEventListener('DOMContentLoaded', function() {
    // Carica i dati reali
    caricaDatiReali();
    
    // Gestione tab
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            
            // Rimuovi la classe active da tutti i pulsanti e contenuti
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Aggiungi la classe active al pulsante e contenuto correnti
            button.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        });
    });
    
    // Gestione modal backdrop click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.remove();
        }
    });
});

// Funzione per simulare il backup
function simulaBackup() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Backup in Corso</h2>
                <button class="modal-close" onclick="chiudiModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                <div class="backup-progress">
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                    <p>Backup dei dati in corso...</p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    // Simula il progresso del backup
    const progressFill = modal.querySelector('.progress-fill');
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += 10;
        progressFill.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            modal.querySelector('p').textContent = 'Backup completato con successo!';
            setTimeout(() => {
                chiudiModal(modal.querySelector('.modal-close'));
            }, 2000);
        }
    }, 200);
}

// Funzione per aggiornare l'interfaccia con i dati caricati
function aggiornaInterfaccia() {
    console.log('Aggiornamento interfaccia con dati:', edilmercData);
    
    // Aggiorna KPI
    aggiornaKPI();
    
    // Aggiorna sezioni
    aggiornaCantieri();
    aggiornaAttestati();
    aggiornaCollaboratori();
    aggiornaRegistro();
}

// Funzione per aggiornare i KPI
function aggiornaKPI() {
    const dati = edilmercData;
    
    // Cantieri attivi
    const cantieriAttivi = dati.cantieri.filter(c => c.stato === 'in_corso').length;
    document.querySelector('.kpi-cantieri').textContent = cantieriAttivi;
    
    // Attestati validi
    const attestatiValidi = dati.attestati.filter(a => a.stato === 'valido').length;
    document.querySelector('.kpi-validi').textContent = attestatiValidi;
    
    // In scadenza
    const inScadenza = dati.attestati.filter(a => a.stato === 'in_scadenza').length;
    document.querySelector('.kpi-scadenza').textContent = inScadenza;
    
    // Scaduti
    const scaduti = dati.attestati.filter(a => a.stato === 'scaduto').length;
    document.querySelector('.kpi-scaduti').textContent = scaduti;
}

// Funzione per aggiornare cantieri
function aggiornaCantieri() {
    const container = document.querySelector('.cantieri-container');
    
    if (!edilmercData.cantieri || edilmercData.cantieri.length === 0) {
        container.innerHTML = '<p>Nessun cantiere trovato</p>';
        return;
    }
    
    let html = '';
    edilmercData.cantieri.forEach(cantiere => {
        const statoIcon = cantiere.stato === 'in_corso' ? 'construction' : 'check_circle';
        const statoColor = cantiere.stato === 'in_corso' ? '#FF8C00' : '#28a745';
        
        html += `
            <div class="cantieri-card">
                <div class="cantieri-header">
                    <h3>${cantiere.nome || cantiere.id}</h3>
                    <span style="color: ${statoColor}">${cantiere.stato || 'sconosciuto'}</span>
                </div>
                <div class="cantieri-details">
                    <p><strong>Comune:</strong> ${cantiere.committente || 'N/A'}</p>
                    <p><strong>Indirizzo:</strong> ${cantiere.indirizzo || 'N/A'}</p>
                    <p><strong>Lavoratori:</strong> ${cantiere.nLavoratori || 0}</p>
                    <p><strong>Periodo:</strong> ${cantiere.dataInizio || 'N/A'} - ${cantiere.dataFine || 'N/A'}</p>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Funzione per aggiornare attestati
function aggiornaAttestati() {
    const container = document.querySelector('.attestati-container');
    
    if (!edilmercData.attestati || edilmercData.attestati.length === 0) {
        container.innerHTML = '<p>Nessun attestato trovato</p>';
        return;
    }
    
    let html = '';
    edilmercData.attestati.forEach(attestato => {
        const statoColor = attestato.stato === 'valido' ? '#28a745' : 
                          attestato.stato === 'in_scadenza' ? '#ffc107' : '#dc3545';
        
        html += `
            <div class="attestati-card">
                <div class="attestati-header">
                    <h3>${attestato.collaboratore}</h3>
                    <span style="color: ${statoColor}">${attestato.stato}</span>
                </div>
                <div class="attestati-details">
                    <p><strong>Tipo:</strong> ${attestato.tipo}</p>
                    <p><strong>Scadenza:</strong> ${attestato.scadenza || 'N/A'}</p>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Funzione per aggiornare collaboratori
function aggiornaCollaboratori() {
    const container = document.querySelector('.collaboratori-container');
    
    if (!edilmercData.collaboratori || edilmercData.collaboratori.length === 0) {
        container.innerHTML = '<p>Nessun collaboratore trovato</p>';
        return;
    }
    
    let html = '';
    edilmercData.collaboratori.forEach(collaboratore => {
        html += `
            <div class="collaboratori-card">
                <div class="collaboratori-header">
                    <h3>${collaboratore.nome}</h3>
                    <span>${collaboratore.ruolo || 'Collaboratore'}</span>
                </div>
                <div class="collaboratori-details">
                    <p><strong>Telefono:</strong> ${collaboratore.telefono || 'N/A'}</p>
                    <p><strong>Email:</strong> ${collaboratore.email || 'N/A'}</p>
                    <p><strong>Assunzione:</strong> ${collaboratore.dataAssunzione || 'N/A'}</p>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Funzione per aggiornare registro
function aggiornaRegistro() {
    const container = document.querySelector('.registro-container');
    
    if (!edilmercData.registro || edilmercData.registro.length === 0) {
        container.innerHTML = '<p>Nessun documento nel registro</p>';
        return;
    }
    
    let html = '<div class="registro-table"><table><thead><tr><th>Data</th><th>Ora</th><th>Cantiere</th><th>Tipo</th><th>File</th><th>Operazione</th></tr></thead><tbody>';
    
    edilmercData.registro.slice().reverse().forEach(doc => {
        html += `
            <tr>
                <td>${doc.data || 'N/A'}</td>
                <td>${doc.ora || 'N/A'}</td>
                <td>${doc.cantiere || 'N/A'}</td>
                <td>${doc.tipo || 'N/A'}</td>
                <td>${doc.nomeFile || 'N/A'}</td>
                <td>${doc.operazione || 'N/A'}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

// Funzione per mostrare notifiche
function mostraNotifica(messaggio, tipo = 'info') {
    const notifica = document.createElement('div');
    notifica.className = `notifica notifica-${tipo}`;
    notifica.textContent = messaggio;
    
    document.body.appendChild(notifica);
    
    setTimeout(() => {
        if (document.body.contains(notifica)) {
            notifica.remove();
        }
    }, 5000);
}

// Funzione per chiudere modal
function chiudiModal(element) {
    const modal = element.closest('.modal');
    if (modal) {
        modal.remove();
    }
}
