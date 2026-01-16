pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        VERSIONED_IMAGE = "14sakshi/feedback-app:1.0.${BUILD_NUMBER}"
        LATEST_IMAGE = "14sakshi/feedback-app:latest"
        CONTAINER_NAME = "feedback-app"
    }

    options {
        timestamps()
    }

    stages {

        // 1️⃣ Checkout code from GitHub
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

        // 3️⃣ Lint your Python code
        stage('Lint') {
            steps {
                sh '''
                    . .venv/bin/activate
                    flake8 app || true
                '''
            }
        }

        // 4️⃣ Run Tests (if tests folder exists)
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

        // 5️⃣ Build Docker Images (versioned + latest)
        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t $VERSIONED_IMAGE -t $LATEST_IMAGE .
                '''
            }
        }

        // 6️⃣ Docker Login & Push
        stage('Docker Login & Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',   // Set your Docker Hub credentials in Jenkins
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $VERSIONED_IMAGE
                        docker push $LATEST_IMAGE
                    '''
                }
            }
        }

        // 7️⃣ Deploy Docker Container
        stage('Deploy Container') {
            steps {
                sh '''
                    if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
                        docker rm -f $CONTAINER_NAME
                    fi

                    docker run -d -p 5000:5000 --name $CONTAINER_NAME $VERSIONED_IMAGE
                '''
            }
        }
    }

    post {
        success {
            echo "Build, Push & Deploy SUCCESS 🎉 Version: $VERSIONED_IMAGE / Latest: $LATEST_IMAGE"
        }
        failure {
            echo "Pipeline FAILED ❌ Check logs"
        }
    }
}
