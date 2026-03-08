pipeline {
  agent any

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
            sh 'docker build -t aceest:jenkins .'
          } else {
            bat 'docker build -t aceest:jenkins .'
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
