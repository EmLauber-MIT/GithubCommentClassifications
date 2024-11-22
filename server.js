const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// Middleware to parse JSON requests
app.use(bodyParser.json());
app.use(express.static('public')); // Serve static files

// Endpoint to handle form submission
app.post('/submit-analysis-request', (req, res) => {
  const { repoUrl, contactEmail, dateRequestedBy, otherNotes } = req.body;

  // Prepare data for saving
  const requestData = {
    repoUrl,
    contactEmail,
    dateRequestedBy,
    otherNotes,
    submittedAt: new Date().toISOString()
  };

  // Define the path for the Analysis_Request file
  const filePath = path.join(__dirname, 'Analysis_Request.json');

  // Read the existing data from the file (if any)
  fs.readFile(filePath, 'utf8', (err, data) => {
    let requests = [];

    if (!err && data) {
      // If the file exists, parse the existing requests
      requests = JSON.parse(data);
    }

    // Add the new request to the list
    requests.push(requestData);

    // Write the updated data to the file
    fs.writeFile(filePath, JSON.stringify(requests, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ error: 'Error saving the analysis request' });
      }
      res.status(200).json({ message: 'Request submitted successfully' });
    });
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
