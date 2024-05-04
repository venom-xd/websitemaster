// Import required modules
const express = require('express');
const path = require('path');

// Create an Express application
const app = express();

// Serve static files from the project directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the homepage
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Route to serve the internships page
app.get('/internships', (req, res) => {
    res.sendFile(path.join(__dirname, 'internships.html'));
});
// Route to serve the LeetCode solutions page
app.get('/leetcode', (req, res) => {
    res.sendFile(path.join(__dirname, 'leetcode.html'));
});
// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
