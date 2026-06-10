pipeline {
  agent any
  environment {
    DOCKER_HOST = 'unix:///var/run/docker.sock'
    COMPOSE_DOCKER_CLI_BUILD = '1'
    DOCKER_BUILDKIT = '1'
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Verify environment') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && pwd && ls -la && docker compose version && docker version'
      }
    }
    stage('Build images') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose build'
      }
    }
    stage('Unit tests') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose run --rm cpp-tests'
      }
    }
    stage('Static analysis') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose run --rm static-analysis'
      }
    }
    stage('Clang-Tidy') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose run --rm clang-tidy'
      }
    }
    stage('Valgrind') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose run --rm valgrind'
      }
    }
    stage('Coverage') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose run --rm coverage'
      }
    }
    stage('Sanitizers') {
      steps {
        sh 'cd /host_mnt/c/projets/docker-googletest-cpp-project && docker compose run --rm sanitizers'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'reports/**/*.html, reports/**/*.xml', allowEmptyArchive: true
    }
  }
}
