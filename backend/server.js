const express = require('express');
const cors = require('cors');
const multer = require('multer');
const pdfParse = require('pdf-parse');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const { analyzeWithGemini } = require('./services/geminiService');
const Analysis = require('./models/Analysis');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://mongodb:27017/resume_analyzer';

app.use(cors());
app.use(express.json());

// In-memory fallback if MongoDB is not reachable
let inMemoryHistory = [];
let isMongoConnected = false;

// Connect to MongoDB with graceful fallback
mongoose.connect(MONGO_URI, {
  serverSelectionTimeoutMS: 3000
}).then(() => {
  console.log('Connected successfully to MongoDB');
  isMongoConnected = true;
}).catch(err => {
  console.warn('MongoDB connection failed. Running in resilient in-memory mode:', err.message);
  isMongoConnected = false;
});

// Configure Multer for PDF file uploads (memory storage)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
});

// Health check endpoint (Used by Nagios & Jenkins CI/CD)
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    service: 'AI Resume Analyzer Backend API',
    timestamp: new Date().toISOString(),
    mongoConnected: isMongoConnected,
    version: '1.0.0'
  });
});

// API Root info
app.get('/', (req, res) => {
  res.json({
    message: 'AI Resume Analyzer REST API is active',
    endpoints: {
      health: '/health',
      analyze: 'POST /api/analyze',
      history: 'GET /api/history'
    }
  });
});

// Analyze Resume Endpoint (Accepts file upload OR raw text)
app.post('/api/analyze', upload.single('resume'), async (req, res) => {
  try {
    let resumeText = '';
    const jobDescription = req.body.jobDescription || 'Software Engineer / DevOps Engineer with Cloud, Docker, CI/CD experience';

    if (req.file) {
      const parsedPdf = await pdfParse(req.file.buffer);
      resumeText = parsedPdf.text;
    } else if (req.body.resumeText) {
      resumeText = req.body.resumeText;
    } else {
      return res.status(400).json({ error: 'Please upload a PDF resume or provide resumeText.' });
    }

    if (!resumeText.trim()) {
      return res.status(400).json({ error: 'Extracted resume text is empty.' });
    }

    // Perform AI analysis via Gemini LLM / semantic engine
    const analysisResult = await analyzeWithGemini(resumeText, jobDescription);
    analysisResult.targetJobRole = req.body.targetJobRole || 'DevOps / Cloud Engineer';

    // Persist to MongoDB or in-memory store
    if (isMongoConnected) {
      try {
        const record = new Analysis(analysisResult);
        await record.save();
        analysisResult._id = record._id;
      } catch (dbErr) {
        console.warn('Could not save to DB:', dbErr.message);
      }
    } else {
      analysisResult._id = 'mem_' + Date.now();
      analysisResult.createdAt = new Date();
      inMemoryHistory.unshift(analysisResult);
    }

    return res.status(200).json({
      success: true,
      data: analysisResult
    });
  } catch (err) {
    console.error('Error analyzing resume:', err);
    return res.status(500).json({
      success: false,
      error: 'Failed to process resume analysis: ' + err.message
    });
  }
});

// Get Analysis History Endpoint
app.get('/api/history', async (req, res) => {
  try {
    if (isMongoConnected) {
      const records = await Analysis.find().sort({ createdAt: -1 }).limit(10);
      return res.json({ success: true, count: records.length, data: records });
    } else {
      return res.json({ success: true, count: inMemoryHistory.length, data: inMemoryHistory.slice(0, 10) });
    }
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Start Server if not imported by test
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`AI Resume Analyzer backend listening on port ${PORT}`);
  });
}

module.exports = app;
