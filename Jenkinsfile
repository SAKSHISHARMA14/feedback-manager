pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE_NAME = "14sakshi/feedback-app"
        VERSION = "1.0.${env.BUILD_NUMBER}"   // versioned image based on Jenkins build number
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {
        // 1️⃣ Checkout code from Git
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2️⃣ Setup Python & Install Dependencies
        stage('Setup Python & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // 3️⃣ Lint Python Code
        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    flake8 app || true
                '''
            }
        }

        // 4️⃣ Run Python Tests
        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    if [ -d tests ]; then pytest tests; else echo "No tests found - skipping"; fi
                '''
            }
        }

        // 5️⃣ Build Docker Images
        stage('Build Docker Images') {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE_NAME}:${VERSION} -t ${DOCKER_IMAGE_NAME}:latest .
                """
            }
        }

        // 6️⃣ Docker Login & Push
        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword
                (credentialsId: 'dockerhub-creds', 
                usernameVariable: 'DOCKER_USER', 
                passwordVariable: 'DOCKER_PASS')
                ]) 
                {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE_NAME}:${VERSION}
                        docker push ${DOCKER_IMAGE_NAME}:latest
                    '''
                }
            }
        }

        // 7️⃣ Deploy Docker Container
        stage('Deploy Container') {
            steps {
                sh """
                    docker stop feedback-app || true
                    docker rm feedback-app || true
                    docker run -d --name feedback-app -p 5000:5000 ${DOCKER_IMAGE_NAME}:latest
                """
            }
        }
    }

    post {de
        success {
            echo "Pipeline finished successfully. Docker image deployed: ${DOCKER_IMAGE_NAME}:latest"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
