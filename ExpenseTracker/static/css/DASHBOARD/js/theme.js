// Immediately apply the theme when the page loads
document.addEventListener("DOMContentLoaded", function() {
    const savedTheme = localStorage.getItem("theme");
    const body = document.body;
    const button = document.getElementById("themeToggle");

    // Apply the theme based on saved preference
    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
        button.textContent = "🌞"; // Change button text to Sun (light mode)
    } else {
        body.classList.remove("dark-mode");
        button.textContent = "🌙"; // Change button text to Moon (dark mode)
    }
});

// Toggle the theme between light and dark mode
function toggleTheme() {
    const body = document.body;
    const button = document.getElementById("themeToggle");

    // Toggle the dark mode class
    body.classList.toggle("dark-mode");

    // Save the current theme mode (dark or light) in localStorage
    if (body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
        button.textContent = "🌞"; // Change button text to Sun (light mode)
    } else {
        localStorage.setItem("theme", "light");
        button.textContent = "🌙"; // Change button text to Moon (dark mode)
    }
}