// NeuroBridge JavaScript - Enhanced Interactions and Animations

// Smooth scrolling and navigation
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations on scroll
    initScrollAnimations();
    
    // Initialize navbar behavior
    initNavbar();
    
    // Initialize mobile menu
    initMobileMenu();
    
    // Initialize agent card interactions
    initAgentCards();
    
    // Initialize intersection observer for animations
    initIntersectionObserver();
});

// Scroll to agents section
function scrollToAgents() {
    const agentsSection = document.getElementById('agents');
    if (agentsSection) {
        agentsSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Open specific agent file (you'll need to implement the backend routing)
function openAgent(agentFile) {
    // This function should redirect to or load the specific agent
    // For now, it will show an alert and log the agent file name
    console.log(Opening agent: ${agentFile});
    
    // Show a user-friendly message
    showNotification(Loading ${agentFile.replace('_', ' ').replace('.py', '')}..., 'info');
    
    // In a real implementation, you might do:
    // window.location.href = /agent/${agentFile};
    // or use fetch to load the agent interface
    
    // Temporary: simulate loading with a timeout
    setTimeout(() => {
        showNotification(${agentFile.replace('_', ' ').replace('.py', '')} is ready!, 'success');
    }, 1500);
}

// Initialize navbar scroll behavior
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
        
        // Hide/show navbar on scroll
        if (currentScrollY > lastScrollY && currentScrollY > 500) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Initialize mobile menu
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            
            // Animate hamburger menu
            const spans = navToggle.querySelectorAll('span');
            if (navToggle.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
}

// Initialize agent card interactions
function initAgentCards() {
    const agentCards = document.querySelectorAll('.agent-card');
    
    agentCards.forEach(card => {
        // Add hover sound effect (optional)
        card.addEventListener('mouseenter', () => {
            playHoverSound();
        });
        
        // Add click animation
        card.addEventListener('click', function(e) {
            if (!e.target.classList.contains('agent-button')) {
                // If clicked on card but not button, animate the card
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            }
        });
        
        // Add keyboard navigation
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const button = this.querySelector('.agent-button');
                if (button) {
                    button.click();
                }
            }
        });
        
        // Make cards focusable
        card.setAttribute('tabindex', '0');
    });
}

// Initialize intersection observer for scroll animations
function initIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.feature-card, .agent-card, .about-stat');
    animateElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });
}

// Initialize scroll animations
function initScrollAnimations() {
    const elements = document.querySelectorAll('.feature-card, .agent-card');
    
    elements.forEach((element, index) => {
        element.style.animationDelay = ${index * 0.1}s;
    });
}

// Show notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());
    
    const notification = document.createElement('div');
    notification.className = notification notification-${type};
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add styles for notification
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Get notification icon based on type
function getNotificationIcon(type) {
    const icons = {
        info: 'fa-info-circle',
        success: 'fa-check-circle',
        warning: 'fa-exclamation-triangle',
        error: 'fa-times-circle'
    };
    return icons[type] || icons.info;
}

// Get notification color based on type
function getNotificationColor(type) {
    const colors = {
        info: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        success: 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)',
        warning: 'linear-gradient(135deg, #F39C12 0%, #E67E22 100%)',
        error: 'linear-gradient(135deg, #E74C3C 0%, #C0392B 100%)'
    };
    return colors[type] || colors.info;
}

// Play hover sound (optional - requires audio files)
function playHoverSound() {
    // Uncomment and add audio file if you want hover sounds
    // const audio = new Audio('static/sounds/hover.mp3');
    // audio.volume = 0.1;
    // audio.play().catch(e => {}); // Ignore errors
}

// Smooth scroll for navigation links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            const offsetTop = targetElement.offsetTop - 80; // Account for navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Add CSS animations keyframes dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        width: 100%;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0.25rem;
        border-radius: 50%;
        margin-left: auto;
        transition: background-color 0.2s ease;
    }
    
    .notification-close:hover {
        background-color: rgba(255,255,255,0.2);
    }
    
    /* Mobile navigation styles */
    @media (max-width: 768px) {
        .nav-menu {
            position: fixed;
            top: 100%;
            left: 0;
            width: 100%;
            height: calc(100vh - 70px);
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            padding-top: 2rem;
            transform: translateX(-100%);
            transition: transform 0.3s ease;
            z-index: 999;
        }
        
        .nav-menu.active {
            transform: translateX(0);
        }
        
        .nav-link {
            padding: 1rem;
            font-size: 1.1rem;
        }
    }
`;
document.head.appendChild(style);

// Initialize particle background (optional enhancement)
function initParticleBackground() {
    const canvas = document.createElement('canvas');
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
    `;
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    const particles = [];
    const particleCount = 50;
    
    // Set canvas size
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    // Create particles
    function createParticles() {
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1,
                opacity: Math.random() * 0.3 + 0.1
            });
        }
    }
    
    // Animate particles
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around edges
            if (particle.x < 0) particle.x = canvas.width;
            if (particle.x > canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = canvas.height;
            if (particle.y > canvas.height) particle.y = 0;
            
            // Draw particle
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = rgba(102, 126, 234, ${particle.opacity});
            ctx.fill();
        });
        
        requestAnimationFrame(animateParticles);
    }
    
    // Initialize
    resizeCanvas();
    createParticles();
    animateParticles();
    
    window.addEventListener('resize', () => {
        resizeCanvas();
        particles.length = 0;
        createParticles();
    });
}

// Uncomment to enable particle background
// initParticleBackground();

// Add loading animation for page
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in-out';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Enhanced agent button interactions with visual feedback
function enhanceAgentButtons() {
    const agentButtons = document.querySelectorAll('.agent-button');
    
    agentButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.6);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => {
                if (ripple.parentNode) {
                    ripple.parentNode.removeChild(ripple);
                }
            }, 600);
        });
    });
}

// Initialize enhanced interactions
document.addEventListener('DOMContentLoaded', function() {
    enhanceAgentButtons();
});

// Add ripple animation CSS
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Keyboard navigation enhancements
document.addEventListener('keydown', function(e) {
    // Press 'Escape' to close mobile menu
    if (e.key === 'Escape') {
        const navMenu = document.querySelector('.nav-menu');
        const navToggle = document.querySelector('.nav-toggle');
        
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        }
    }
    
    // Quick navigation shortcuts
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case '1':
                e.preventDefault();
                scrollToSection('home');
                break;
            case '2':
                e.preventDefault();
                scrollToSection('features');
                break;
            case '3':
                e.preventDefault();
                scrollToSection('agents');
                break;
            case '4':
                e.preventDefault();
                scrollToSection('about');
                break;
        }
    }
});

// Scroll to section helper
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 80;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// Add accessibility announcements
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    announcement.style.cssText = `
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    `;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Enhanced agent opening with better UX
function openAgent(agentFile) {
    const agentName = agentFile.replace('agent.py', '').replace('', ' ');
    const capitalizedName = agentName.charAt(0).toUpperCase() + agentName.slice(1);
    
    // Show loading state
    showNotification(Loading ${capitalizedName} Agent..., 'info');
    announceToScreenReader(Loading ${capitalizedName} Agent);
    
    // Simulate agent loading (replace with actual implementation)
    setTimeout(() => {
        showNotification(${capitalizedName} Agent is ready!, 'success');
        announceToScreenReader(${capitalizedName} Agent loaded successfully);
        
        // Here you would typically:
        // 1. Make an API call to your Flask backend
        // 2. Navigate to the agent interface
        // 3. Load the agent-specific UI
        
        // Example implementation:
        console.log(Agent file: ${agentFile});
        console.log(Opening ${capitalizedName} Agent interface...);
        
        // For demonstration, we'll show what would happen:
        const agentUrls = {
            'cognition_agent.py': '/cognition',
            'tutor_agent.py': '/tutor',
            'rewriter_agent.py': '/rewriter', 
            'planner_agent.py': '/planner',
            'emotion_agent.py': '/emotion',
            'progress_agent.py': '/progress'
        };
        
        const url = agentUrls[agentFile];
        if (url) {
            // In a real implementation:
            // window.location.href = url;
            console.log(Would navigate to: ${url});
        }
        
    }, 1500);
}

// Theme switching functionality (optional)
function initThemeSwitch() {
    const themeToggle = document.createElement('button');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    themeToggle.className = 'theme-toggle';
    themeToggle.style.cssText = `
        position: fixed;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--gradient-primary);
        color: white;
        border: none;
        cursor: pointer;
        font-size: 1.2rem;
        box-shadow: var(--shadow-lg);
        transition: all var(--duration-normal) ease;
        z-index: 999;
    `;
    
    document.body.appendChild(themeToggle);
    
    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        const isDark = document.body.classList.contains('dark-theme');
        this.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
}

// Performance optimization: Throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Optimized scroll handler
const optimizedScrollHandler = throttle(function() {
    // Update navbar on scroll
    const navbar = document.querySelector('.navbar');
    const scrollY = window.scrollY;
    
    if (scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}, 16); // ~60fps

window.addEventListener('scroll', optimizedScrollHandler);

// Add scrolled class styles
const scrollStyles = document.createElement('style');
scrollStyles.textContent = `
    .navbar.scrolled {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Dark theme styles (optional) */
    .dark-theme {
        --background-primary: #1a1a1a;
        --background-secondary: #2d2d2d;
        --background-card: #3a3a3a;
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
        --text-muted: #999999;
    }
    
    .dark-theme .navbar {
        background: rgba(26, 26, 26, 0.95) !important;
        border-bottom-color: rgba(255, 255, 255, 0.1);
    }
    
    .dark-theme .navbar.scrolled {
        background: rgba(26, 26, 26, 0.98) !important;
        box-shadow: 0 2px 20px rgba(255, 255, 255, 0.1) !important;
    }
`;
document.head.appendChild(scrollStyles);

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Optional: Enable theme switching
    // initThemeSwitch();
    
    console.log('NeuroBridge interface loaded successfully!');
    console.log('Available shortcuts:');
    console.log('- Ctrl/Cmd + 1: Home');
    console.log('- Ctrl/Cmd + 2: Features');
    console.log('- Ctrl/Cmd + 3: Agents');
    console.log('- Ctrl/Cmd + 4: About');
    console.log('- Escape: Close mobile menu');
});

// Error handling for missing elements
function safeQuerySelector(selector) {
    try {
        return document.querySelector(selector);
    } catch (error) {
        console.warn(Element not found: ${selector});
        return null;
    }
}

// Progressive enhancement check
if ('IntersectionObserver' in window) {
    // Modern browser - use intersection observer
    initIntersectionObserver();
} else {
    // Fallback for older browsers
    console.log('Using fallback animations for older browsers');
    const elements = document.querySelectorAll('.feature-card, .agent-card');
    elements.forEach(el => el.classList.add('animate-in'));
}