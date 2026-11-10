const request = require('supertest');
const app = require('../server');

describe('AI Resume Analyzer API Tests', () => {
  it('GET /health should return 200 and status UP', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toEqual(200);
    expect(res.body.status).toEqual('UP');
    expect(res.body.service).toBeDefined();
  });

  it('GET / should return 200 with API info', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toEqual(200);
    expect(res.body.endpoints).toBeDefined();
  });

  it('POST /api/analyze should return 400 when no input is provided', async () => {
    const res = await request(app).post('/api/analyze').send({});
    expect(res.statusCode).toEqual(400);
  });

  it('POST /api/analyze with resumeText should return match score and extracted data', async () => {
    const payload = {
      resumeText: 'Experienced Software Engineer skilled in React, Node.js, Docker, AWS, Jenkins and Git.',
      jobDescription: 'Looking for a DevOps Engineer with Docker, Node.js, AWS and CI/CD experience.'
    };
    const res = await request(app).post('/api/analyze').send(payload);
    expect(res.statusCode).toEqual(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.matchScore).toBeGreaterThanOrEqual(0);
    expect(Array.isArray(res.body.data.extractedSkills)).toBe(true);
  });
});
