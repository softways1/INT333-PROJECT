const mongoose = require('mongoose');

const AnalysisSchema = new mongoose.Schema({
  candidateName: { type: String, default: 'Anonymous Candidate' },
  email: { type: String, default: 'Not specified' },
  extractedSkills: [String],
  targetJobRole: { type: String, default: 'General Application' },
  matchScore: { type: Number, required: true },
  strengths: [String],
  missingSkills: [String],
  recommendations: { type: String },
  rawSummary: { type: String },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Analysis', AnalysisSchema);
