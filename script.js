document.getElementById('myForm').addEventListener('submit', function(event) {
    console.log('Form submitted'); // Debugging line
    event.preventDefault(); // Prevent default form submission

    const email = document.getElementById('email').value;
    const location = document.getElementById('location').value;
    const message = document.getElementById('composeMessage').value;

    const data = { email, location, message };

    // Show loading message
    showPopup('Submitting, please wait...', 'loading');
    
    fetch('http://localhost:3000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.text();
    })
    .then(result => {
        showPopup('Successfully submitted: ' + result, 'success');
        document.getElementById('myForm').reset();
        
        // Redirect to index2.html after successful submission
        setTimeout(() => {
            window.location.href = 'index2.html';
        }, 3000); // Wait for 3 seconds before redirecting
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        showPopup('Submission failed. Please try again.', 'error');
    });
});

function showPopup(message, type) {
    const popup = document.getElementById('popup');
    popup.textContent = message;

    // Remove existing classes and add the appropriate one
    popup.className = 'popup';
    if (type === 'success') {
        popup.classList.add('success');
    } else if (type === 'error') {
        popup.classList.add('error');
    } else {
        popup.classList.add('loading');
    }

    popup.classList.add('show'); // Show popup

    // Hide the popup after 3 seconds
    setTimeout(() => {
        popup.classList.remove('show');
    }, 3000);
}