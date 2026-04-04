pipeline {
  agent any

  environment {
    // Optional (default empty): for environments with TLS interception.
    // Example: pypi.org files.pythonhosted.org
    PIP_TRUSTED_HOSTS = "${env.PIP_TRUSTED_HOSTS ?: ''}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          if (isUnix()) {
            sh 'DOCKER_BUILDKIT=1 docker build -t aceest:jenkins --build-arg PIP_TRUSTED_HOSTS="$PIP_TRUSTED_HOSTS" .'
          } else {
            bat 'set DOCKER_BUILDKIT=1\r\ndocker build -t aceest:jenkins --build-arg PIP_TRUSTED_HOSTS=%PIP_TRUSTED_HOSTS% .'
          }
        }
      }
    }

    stage('Quality Gate - Lint') {
      steps {
        script {
          if (isUnix()) {
            sh 'docker run --rm aceest:jenkins python -m compileall app.py'
            sh 'docker run --rm aceest:jenkins ruff check .'
          } else {
            bat 'docker run --rm aceest:jenkins python -m compileall app.py'
            bat 'docker run --rm aceest:jenkins ruff check .'
          }
        }
      }
    }

    stage('Test') {
      steps {
        script {
          if (isUnix()) {
            sh 'docker run --rm aceest:jenkins python -m pytest'
          } else {
            bat 'docker run --rm aceest:jenkins python -m pytest'
          }
        }
      }
    }
  }

  post {
    always {
      deleteDir()
    }
  }
}
