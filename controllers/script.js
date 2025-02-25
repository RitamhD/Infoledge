// Select all the navigation links
const navLinks = document.querySelectorAll('nav a');

// Add event listener to each link
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor link behavior

        // Get the target section's ID
        const targetSection = document.querySelector(link.getAttribute('href'));

        const offset = 70; // Height of the navbar
        const targetPosition = targetSection.offsetTop - offset;
        // Scroll to the target section smoothly
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    });
});
