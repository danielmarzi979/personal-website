// EDILMERC Sito Pubblicizzario - JavaScript Semplice

// Funzione per scroll alla sezione contatti
function scrollToContact() {
    const contactSection = document.getElementById('contatti');
    if (contactSection) {
        const headerHeight = document.querySelector('.header').offsetHeight;
        const sectionTop = contactSection.offsetTop - headerHeight - 20;
        
        window.scrollTo({
            top: sectionTop,
            behavior: 'smooth'
        });
    }
}

// Setup form contatti
function setupForm() {
    const form = document.getElementById('contact-form');
    
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
        
        // Validazione in tempo reale
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => validateField(input));
            input.addEventListener('input', () => {
                if (input.classList.contains('error')) {
                    validateField(input);
                }
            });
        });
    }
}

// Validazione campo
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Rimuovi errori precedenti
    field.classList.remove('error');
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Validazione base
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'Questo campo è obbligatorio';
    } else if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Inserisci un\'email valida';
        }
    } else if (field.type === 'tel' && value) {
        const phoneRegex = /^[\d\s\+\-\(\)]+$/;
        if (!phoneRegex.test(value) || value.length < 8) {
            isValid = false;
            errorMessage = 'Inserisci un numero di telefono valido';
        }
    }
    
    // Mostra errore se necessario
    if (!isValid) {
        field.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = errorMessage;
        field.parentNode.appendChild(errorDiv);
    }
    
    return isValid;
}

// Gestione submit form
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    // Disabilita bottone e mostra caricamento
    submitButton.disabled = true;
    submitButton.textContent = 'Invio in corso...';
    
    // Valida tutti i campi
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isFormValid = true;
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isFormValid = false;
        }
    });
    
    if (!isFormValid) {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
        showNotification('Per favore, correggi gli errori nel form', 'error');
        return;
    }
    
    // Simula invio form
    try {
        // Raccogli dati
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        console.log('Dati form:', data);
        
        // Simula invio API
        await simulateFormSubmission(data);
        
        // Successo
        showNotification('Richiesta inviata con successo! Ti contatteremo presto.', 'success');
        form.reset();
        
    } catch (error) {
        console.error('Errore invio form:', error);
        showNotification('Errore durante l\'invio. Riprova più tardi.', 'error');
    } finally {
        // Ripristina bottone
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }
}

// Simula invio form (sostituire con API reale)
async function simulateFormSubmission(data) {
    // Simula delay rete
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Qui andrebbe la chiamata API reale
    // const response = await fetch('/api/contact', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(data)
    // });
    
    return { success: true };
}

// Sistema notifiche
function showNotification(message, type = 'info') {
    // Rimuovi notifiche esistenti
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Crea nuova notifica
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Aggiungi al DOM
    document.body.appendChild(notification);
    
    // Animazione ingresso
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Rimuovi automaticamente
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (document.body.contains(notification)) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

// Inizializzazione quando il DOM è caricato
document.addEventListener('DOMContentLoaded', function() {
    console.log('EDILMERC Sito Pubblicizzario caricato');
    setupForm();
});

// Stili CSS dinamici per notifiche e errori
const dynamicStyles = document.createElement('style');
dynamicStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        color: var(--testo-principale);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: var(--ombra-forte);
        z-index: 10000;
        transform: translateX(400px);
        transition: all 0.3s ease;
        max-width: 300px;
        border-left: 4px solid var(--rosso-em);
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left-color: var(--verde-em);
        background: linear-gradient(135deg, #f8fff8, white);
    }
    
    .notification-error {
        border-left-color: var(--rosso-em);
        background: linear-gradient(135deg, #fff8f8, white);
    }
    
    .form-group .error {
        border-color: var(--rosso-em) !important;
        box-shadow: 0 0 0 3px rgba(224, 43, 43, 0.1);
    }
    
    .error-message {
        color: var(--rosso-em);
        font-size: 0.875rem;
        margin-top: 0.5rem;
        display: block;
    }
    
    @media (max-width: 768px) {
        .notification {
            right: 10px;
            left: 10px;
            max-width: none;
            transform: translateY(-100px);
        }
        
        .notification.show {
            transform: translateY(0);
        }
    }
`;

document.head.appendChild(dynamicStyles);
