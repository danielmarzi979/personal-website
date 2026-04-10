// Script di debug per il sito EDILMERC
// Aggiungi temporaneamente all'HTML per diagnosticare problemi

console.log("=== DEBUG EDILMERC SITE ===");

// Verifica caricamento DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM caricato");
    
    // Verifica elementi principali
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    console.log("Tab buttons trovati:", tabButtons.length);
    console.log("Tab contents trovati:", tabContents.length);
    
    // Verifica se il JSON è caricabile
    fetch('dati_reali_edilmerc.json')
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("JSON caricato con successo:", data);
            console.log("Cantieri:", data.cantieri?.length || 0);
            console.log("Attestati:", data.attestati?.length || 0);
            console.log("Collaboratori:", data.collaboratori?.length || 0);
            console.log("Registro:", data.registro?.length || 0);
        })
        .catch(error => {
            console.error("Errore caricamento JSON:", error);
        });
    
    // Test funzioni principali
    if (typeof caricaDatiReali === 'function') {
        console.log("Funzione caricaDatiReali trovata");
    } else {
        console.error("Funzione caricaDatiReali NON trovata");
    }
    
    if (typeof aggiornaInterfaccia === 'function') {
        console.log("Funzione aggiornaInterfaccia trovata");
    } else {
        console.error("Funzione aggiornaInterfaccia NON trovata");
    }
    
    // Forza caricamento dati
    setTimeout(() => {
        console.log("Forzo caricamento dati...");
        if (typeof caricaDatiReali === 'function') {
            caricaDatiReali();
        }
    }, 1000);
});

// Mostra notifica di debug
function mostraNotificaDebug(messaggio) {
    const notifica = document.createElement('div');
    notifica.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: #ff6b6b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        z-index: 10000;
        font-size: 12px;
    `;
    notifica.textContent = messaggio;
    document.body.appendChild(notifica);
    
    setTimeout(() => {
        if (document.body.contains(notifica)) {
            notifica.remove();
        }
    }, 5000);
}
