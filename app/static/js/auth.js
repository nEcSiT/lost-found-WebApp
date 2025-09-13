// Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Form validation and enhancement
    const authForm = document.querySelector('.auth-form');
    const submitBtn = document.querySelector('.btn-primary');
    const formInputs = document.querySelectorAll('.form-control');
    
    // Real-time validation
    formInputs.forEach(input => {
        input.addEventListener('blur', validateInput);
        input.addEventListener('input', clearValidation);
    });
    
    // Form submission handling
    if (authForm) {
        authForm.addEventListener('submit', handleFormSubmit);
    }
    
    // Password strength indicator (for registration)
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', checkPasswordStrength);
    }
    
    // Auto-dismiss alerts
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

function validateInput(event) {
    const input = event.target;
    const formGroup = input.closest('.form-group');
    
    clearValidationMessages(formGroup);
    
    // Required field validation
    if (input.hasAttribute('required') && !input.value.trim()) {
        showValidationError(input, 'This field is required');
        return false;
    }
    
    // Email validation
    if (input.type === 'email' && input.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            showValidationError(input, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Campus ID validation
    if (input.name === 'campus_id' && input.value) {
        const campusIdRegex = /^[A-Za-z0-9]+$/;
        if (!campusIdRegex.test(input.value)) {
            showValidationError(input, 'Campus ID should contain only letters and numbers');
            return false;
        }
    }
    
    // Phone number validation (optional)
    if (input.name === 'phone' && input.value) {
        const phoneRegex = /^[\+]?[\d\s\-\(\)]+$/;
        if (!phoneRegex.test(input.value)) {
            showValidationError(input, 'Please enter a valid phone number');
            return false;
        }
    }
    
    // Password validation
    if (input.name === 'password' && input.value) {
        if (input.value.length < 8) {
            showValidationError(input, 'Password must be at least 8 characters long');
            return false;
        }
    }
    
    // Show success if validation passes
    showValidationSuccess(input);
    return true;
}

function clearValidation(event) {
    const input = event.target;
    const formGroup = input.closest('.form-group');
    
    input.classList.remove('is-invalid', 'is-valid');
    clearValidationMessages(formGroup);
}

function showValidationError(input, message) {
    const formGroup = input.closest('.form-group');
    
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    
    formGroup.appendChild(feedback);
}

function showValidationSuccess(input) {
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
}

function clearValidationMessages(formGroup) {
    const existingFeedback = formGroup.querySelectorAll('.invalid-feedback, .valid-feedback');
    existingFeedback.forEach(el => el.remove());
}

function handleFormSubmit(event) {
    const form = event.target;
    const submitBtn = form.querySelector('.btn-primary');
    const inputs = form.querySelectorAll('.form-control[required]');
    
    let isValid = true;
    
    // Validate all required inputs
    inputs.forEach(input => {
        if (!validateInput({ target: input })) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        event.preventDefault();
        return false;
    }
    
    // Show loading state
    showLoadingState(submitBtn);
}

function showLoadingState(button) {
    button.disabled = true;
    button.classList.add('loading');
}

function hideLoadingState(button) {
    button.disabled = false;
    button.classList.remove('loading');
}

// Auto-format phone input if present
const phoneInput = document.getElementById('phone');
if (phoneInput) {
    phoneInput.addEventListener('input', function() {
        let value = this.value.replace(/\D/g, '');
        if (value.length >= 10) {
            value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
        } else if (value.length >= 6) {
            value = value.replace(/(\d{3})(\d{3})/, '($1) $2-');
        } else if (value.length >= 3) {
            value = value.replace(/(\d{3})/, '($1) ');
        }
        this.value = value;
    });
}

// Campus ID auto-uppercase
const campusIdInput = document.getElementById('campus_id');
if (campusIdInput) {
    campusIdInput.addEventListener('input', function() {
        this.value = this.value.toUpperCase();
    });
}
