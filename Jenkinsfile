pipeline {
    agent any

    environment {
        PROJECT_NAME = 'ai-resume-analyzer'
        DEPLOY_DIR   = '/opt/ai-resume-analyzer'
    }

    stages {
        stage('1. Code Verification & Checkout') {
            steps {
                echo "======================================================"
                echo "Starting CI/CD Pipeline for: ${PROJECT_NAME}"
                echo "Student: AMAN KUMAR SINGH | INT333 DevOps Project"
                echo "======================================================"
                sh 'git --version'
                sh 'pwd && ls -la'
            }
        }

        stage('2. Automated Unit Testing') {
            steps {
                dir('backend') {
                    echo "Running backend unit tests with Jest..."
                    sh 'npm install --include=dev'
                    sh 'npm test'
                }
            }
        }

        stage('3. Build Docker Microservices') {
            steps {
                echo "Building Docker images for Frontend, Backend, and MongoDB..."
                sh 'docker compose build'
            }
        }

        stage('4. Automated Container Deployment') {
            steps {
                echo "Deploying microservices using Docker Compose..."
                sh 'docker compose down || true'
                sh 'docker compose up -d'
            }
        }

        stage('5. Production Health Verification') {
            steps {
                echo "Verifying application endpoint health..."
                sleep 5
                sh 'curl -f http://localhost:5000/health || curl -f http://localhost/health'
                echo "Deployment successfully verified and operational!"
            }
        }
    }

    post {
        success {
            echo "SUCCESS: AI Resume Analyzer Pipeline executed successfully!"
        }
        failure {
            echo "FAILURE: Pipeline execution encountered an error. Check logs."
        }
    }
}
