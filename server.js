const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname))); // Serve static files from the current directory

// Endpoint to handle form submission
app.post('/submit', (req, res) => {
    const { email, location, message } = req.body;

    // Validate input
    if (!email || !location || !message) {
        return res.status(400).send('Invalid input');
    }

    // Prepare data to be saved
    const data = `Email: ${email}, Location: ${location}, Message: ${message}\n`;

    // Write data to data1.txt
    fs.appendFile('data1.txt', data, (err) => {
        if (err) {
            console.error('Error writing to file', err);
            return res.status(500).send('Internal Server Error');
        }
        // Respond with success message
        res.status(200).send('Success');
    });
});

// Endpoint to get email data
app.get('/emails', (req, res) => {
    fs.readFile('data1.txt', 'utf-8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading data file');
        }

        // Split the file contents into lines and filter out empty lines
        const emails = data.split('\n').filter(line => line.trim() !== '').map(line => {
            // Extracting values from the line
            const parts = line.split(', ');

            // Extract the email, location, and message while checking for undefined
            const email = parts[0] ? parts[0].split(': ')[1] : undefined; // Ensure parts[0] exists
            const location = parts[1] ? parts[1].split(': ')[1] : undefined; // Ensure parts[1] exists
            const message = parts[2] ? parts[2].split(': ')[1] : undefined; // Ensure parts[2] exists

            // Log extracted values to debug
            console.log(`Extracted - Email: ${email}, Location: ${location}, Message: ${message}`);

            return {
                to_email: email,
                location: location,
                message: message,
                deleted: false // Placeholder for deletion status if needed
            };
        });

        res.json(emails);
    });
});




// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
