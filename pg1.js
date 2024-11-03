function handleLogin(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the values from the form fields
    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Placeholder for valid credentials - you can replace this with actual validation
    const validEmail = "user@example.com"; // Replace with your actual valid email
    const validPassword = "password123"; // Replace with your actual valid password

    // Get the error message element
    const errorMessage = document.getElementById('error-message');
    
    // Check if the credentials are valid
    if (email === validEmail && password === validPassword) {
        // Redirect to index2.html if valid
        window.location.href = "index2.html";
    } else {
        // Display an error message for invalid credentials
        errorMessage.textContent = "Invalid credentials. Please try again.";
        errorMessage.style.display = "block";
    }
}
