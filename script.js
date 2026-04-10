// EDILMERC Sito Pubblico - JavaScript Professionale

// Inizializzazione quando il DOM è caricato
document.addEventListener('DOMContentLoaded', function() {
    console.log('EDILMERC Sito Pubblico caricato');
    setupNavigation();
    setupForm();
    setupAnimations();
    setupScrollEffects();
});

// Setup navigazione principale
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetSection = button.getAttribute('data-section');
            
            // Rimuovi active da tutti i bottoni
            navButtons.forEach(btn => btn.classList.remove('active'));
            
            // Aggiungi active al bottone cliccato
            button.classList.add('active');
            
            // Scroll smooth alla sezione
            const section = document.getElementById(targetSection);
            if (section) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const sectionTop = section.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: sectionTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Aggiorna active state durante lo scroll
    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav();
}

// Aggiorna stato attivo della navigazione durante lo scroll
function updateActiveNav() {
    const sections = document.querySelectorAll('.section');
    const navButtons = document.querySelectorAll('.nav-btn');
    const scrollPosition = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            navButtons.forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.querySelector(`[data-section="${sectionId}"]`);
            if (activeBtn) {
                activeBtn.classList.add('active');
            }
        }
    });
}

// Setup form contatti
function setupForm() {
    const form = document.querySelector('.form');
    
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
        // Raccolta dati
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

// Setup animazioni
function setupAnimations() {
    // Animazione numeri stats
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumbers(entry.target);
                statsObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
    
    // Animazione cards
    const cardsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.service-card, .work-card, .stat-item').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        cardsObserver.observe(card);
    });
}

// Animazione numeri
function animateNumbers(container) {
    const numbers = container.querySelectorAll('.stat-number');
    
    numbers.forEach(numberElement => {
        const finalNumber = numberElement.textContent;
        const hasPlus = finalNumber.includes('+');
        const hasPercent = finalNumber.includes('%');
        
        let numericValue = parseInt(finalNumber.replace(/\D/g, ''));
        let currentValue = 0;
        const increment = numericValue / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                currentValue = numericValue;
                clearInterval(timer);
            }
            
            let displayValue = Math.floor(currentValue);
            if (hasPlus) displayValue += '+';
            if (hasPercent) displayValue += '%';
            
            numberElement.textContent = displayValue;
        }, 30);
    });
}

// Setup effetti scroll
function setupScrollEffects() {
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        const header = document.querySelector('.header');
        
        // Header scroll effect
        if (currentScrollY > 100) {
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.boxShadow = 'var(--ombra-leggera)';
        }
        
        lastScrollY = currentScrollY;
    });
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

// Gestione pulsanti hero
document.addEventListener('DOMContentLoaded', function() {
    const primaryBtn = document.querySelector('.hero-buttons .btn-primary');
    const secondaryBtn = document.querySelector('.hero-buttons .btn-secondary');
    
    if (primaryBtn) {
        primaryBtn.addEventListener('click', () => {
            const contactSection = document.getElementById('contatti');
            if (contactSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const sectionTop = contactSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: sectionTop,
                    behavior: 'smooth'
                });
            }
        });
    }
    
    if (secondaryBtn) {
        secondaryBtn.addEventListener('click', () => {
            const worksSection = document.getElementById('lavori');
            if (worksSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const sectionTop = worksSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: sectionTop,
                    behavior: 'smooth'
                });
            }
        });
    }
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
    
    .nav-btn.active {
        background-color: var(--rosso-em);
        color: white;
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
