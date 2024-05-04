document.addEventListener('DOMContentLoaded', function() {
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });

    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('nav ul');
    menuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('show');
    });

    const contactForm = document.getElementById('contact-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    const submitButton = document.getElementById('submit-button');

    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateForm()) {
            console.log('Submitted!');
            contactForm.reset();
        }
    });

    function validateForm() {
        let isValid = true;
        if (nameInput.value.trim() === '') {
            isValid = false;
            setErrorFor(nameInput, 'Name is required');
        } else {
            setSuccessFor(nameInput);
        }
        if (emailInput.value.trim() === '') {
            isValid = false;
            setErrorFor(emailInput, 'Email is required');
        } else if (!isEmailValid(emailInput.value.trim())) {
            isValid = false;
            setErrorFor(emailInput, 'Email is not valid');
        } else {
            setSuccessFor(emailInput);
        }
        if (messageInput.value.trim() === '') {
            isValid = false;
            setErrorFor(messageInput, 'Message is required');
        } else {
            setSuccessFor(messageInput);
        }
        return isValid;
    }

    function setErrorFor(input, message) {
        const formControl = input.parentElement;
        const errorMessage = formControl.querySelector('.error-message');
        errorMessage.innerText = message;
        formControl.classList.add('error');
    }

    function setSuccessFor(input) {
        const formControl = input.parentElement;
        formControl.classList.remove('error');
        const errorMessage = formControl.querySelector('.error-message');
        errorMessage.innerText = '';
    }

    function isEmailValid(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});
