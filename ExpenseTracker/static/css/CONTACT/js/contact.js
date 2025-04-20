// Enable submit button only when consent checkbox is checked
document.addEventListener("DOMContentLoaded", function () {
    const consentCheckbox = document.querySelector('input[name="consent"]');
    const submitButton = document.getElementById("submitBtn");
  
    if (consentCheckbox && submitButton) {
      submitButton.disabled = !consentCheckbox.checked;
  
      consentCheckbox.addEventListener("change", function () {
        submitButton.disabled = !this.checked;
      });
    }
  });
  