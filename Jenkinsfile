pipeline {
  agent any
  environment { PYTHONUNBUFFERED = '1' }
  options { timestamps() }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Setup Python') {
      steps {
        sh '''#!/usr/bin/env bash
          set -euo pipefail
          python3 --version
          python3 -m venv .venv
          . .venv/bin/activate
          .venv/bin/python -m pip install --upgrade pip
        '''
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''#!/usr/bin/env bash
          set -euo pipefail
          . .venv/bin/activate
          .venv/bin/pip install -r requirements.txt
        '''
      }
    }

    stage('Lint') {
      steps {
        sh '''#!/usr/bin/env bash
          . .venv/bin/activate
          .venv/bin/flake8 app || true
        '''
      }
    }

    stage('Tests') {
      steps {
        sh '''#!/usr/bin/env bash
          . .venv/bin/activate
          if [ -d tests ]; then
            .venv/bin/pytest -q
          fi
        '''
      }
    }
  }

  post {
    always {
      sh 'echo "Build finished."'
      archiveArtifacts artifacts: 'requirements.txt, **/*.log', allowEmptyArchive: true
    }
    failure { echo "Build failed" }
  }
}
