import express from 'express';
import fs from 'fs';
import path from 'path';
import bodyParser from 'body-parser';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3000;

// Middleware to parse JSON requests
app.use(bodyParser.json());
app.use(express.static('public')); // Serve static files

// Serve the index.html file for the root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

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

  // Save the request data to a file (for example purposes)
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err && err.code !== 'ENOENT') {
      return res.status(500).json({ error: 'Failed to read existing requests' });
    }

    const requests = data ? JSON.parse(data) : [];
    requests.push(requestData);

    fs.writeFile(filePath, JSON.stringify(requests, null, 2), (err) => {
      if (err) {
        return res.status(500).json({ error: 'Failed to save request' });
      }

      res.status(200).json({ message: 'Request submitted successfully' });
    });
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});