// Navigation JavaScript for dropdown functionality

document.addEventListener('DOMContentLoaded', function() {
    // Handle dropdown menu interactions
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('.dropdown-btn');
        const content = dropdown.querySelector('.dropdown-content');
        
        // Toggle dropdown on click
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Close all other dropdowns
            dropdowns.forEach(otherDropdown => {
                if (otherDropdown !== dropdown) {
                    otherDropdown.querySelector('.dropdown-content').style.display = 'none';
                    otherDropdown.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            const isOpen = content.style.display === 'block';
            content.style.display = isOpen ? 'none' : 'block';
            dropdown.classList.toggle('active', !isOpen);
        });
        
        // Show dropdown on hover for better UX
        dropdown.addEventListener('mouseenter', function() {
            content.style.display = 'block';
            dropdown.classList.add('active');
        });
        
        dropdown.addEventListener('mouseleave', function() {
            content.style.display = 'none';
            dropdown.classList.remove('active');
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function() {
        dropdowns.forEach(dropdown => {
            const content = dropdown.querySelector('.dropdown-content');
            content.style.display = 'none';
            dropdown.classList.remove('active');
        });
    });
    
    // Prevent dropdown from closing when clicking inside it
    dropdowns.forEach(dropdown => {
        const content = dropdown.querySelector('.dropdown-content');
        content.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
});

// Add smooth animations for better UX
function addSmoothAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        .dropdown-content {
            opacity: 0;
            transform: translateY(-10px);
            transition: opacity 0.2s ease, transform 0.2s ease;
        }
        
        .dropdown.active .dropdown-content {
            opacity: 1;
            transform: translateY(0);
        }
        
        .dropdown-btn {
            transition: all 0.2s ease;
        }
        
        .dropdown.active .dropdown-btn {
            background-color: #94DEA5;
            color: #023D54;
        }
    `;
    document.head.appendChild(style);
}

// Initialize smooth animations
addSmoothAnimations();
