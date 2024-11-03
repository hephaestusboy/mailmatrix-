const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path'); // Import path to serve static files

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname))); // Serve static files from the current directory

// Endpoint to handle form submission
app.post('/submit', (req, res) => {
    const {email, location, message } = req.body;

    // Validate input
    if (!email || !location || !message) {
        return res.status(400).send('Invalid input');
    }

    // Prepare data to be saved
    const data = Email: ${email}, Location: ${location}, Message: ${message}\n;

    // Write data to data.txt
    fs.appendFile('data.txt', data, (err) => {
        if (err) {
            console.error('Error writing to file', err);
            return res.status(500).send('Internal Server Error');
        }
        // Respond with success message
        res.status(200).send('Success');
    });
});

// Start server
app.listen(PORT, () =>) {
    console.log(Server is running on http://localhost:${PORT});
});