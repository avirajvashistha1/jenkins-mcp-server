pipeline {
    agent any
    environment {
        // If you use a virtualenv or want to specify python version
        PYTHON = 'python3'
    }
    stages {
        stage('Checkout') {
            steps {
                // Check the code out from SCM (GitHub)
                checkout scm
            }
        }
        stage('Set up Python') {
            steps {
                // Install dependencies
                bat '''
                $PYTHON -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                if [ -f requirements.txt ]; then
                  pip install -r requirements.txt
                fi
                '''
            }
        }
        stage('Run Tests') {
            steps {
                // Run your test suite, for example with pytest
                bat '''
                . venv/bin/activate
                if [ -f pytest.ini ] || [ -d tests ]; then
                  pytest
                else
                  echo "No tests found, skipping."
                fi
                '''
            }
        }
    }

    
    post {
        always {
            // Clean up virtualenv after job finishes
            bat 'rm -rf venv'
        }
    }
}
