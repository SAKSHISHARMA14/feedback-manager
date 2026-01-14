pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        DOCKER_IMAGE = "feedback-manager"
        CONTAINER_NAME = "feedback-app"
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

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

        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    flake8 app || true
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    if [ -d tests ]; then
                        pytest -q
                    else
                        echo "No tests found - skipping"
                    fi
                '''
            }
        }

        // === NEW: Docker stages ===
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                    # Remove old container if exists
                    if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
                        docker rm -f $CONTAINER_NAME
                    fi
                    # Run container detached
                    docker run -d -p 5000:5000 --name $CONTAINER_NAME $DOCKER_IMAGE
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        failure {
            echo "Pipeline failed. Check Jenkins logs."
        }
    }
}
