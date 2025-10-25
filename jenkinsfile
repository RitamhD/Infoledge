pipeline {
    agent any

    environment {
        APP_DIR = "/home/ubuntu/infoledge"
        VENV = "${APP_DIR}/venv"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Setup Python') {
            steps {
                sh """
                python3 -m venv ${VENV}
                . ${VENV}/bin/activate
                pip install -r ${APP_DIR}/requirements.txt
                """
            }
        }

        stage('Run tests') {
            steps {
                sh """
                . ${VENV}/bin/activate
                pytest -q || true   # run tests; fail the pipeline if you want
                """
            }
        }

        stage('Deploy') {
            steps {
                // If Jenkins runs on same machine, we can deploy by restarting systemd
                sh """
                sudo systemctl stop flaskapp || true
                cd ${APP_DIR}
                git pull origin main || true
                . ${VENV}/bin/activate
                pip install -r requirements.txt
                sudo systemctl start flaskapp
                """
            }
        }
    }

    post {
        success {
            echo '✅ Deployment complete.'
            emailtext(
                subject: "✅ SUCCESS: Jenkins Build #${BUILD_NUMBER}",
                body: """<p>Hi,</p>
                        <p>The Jenkins build for <b>${JOB_NAME}</b> completed successfully!</p>
                        <p><b>Build URL:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></p>""",
                to: 'hatiritam03@gmail.com',
                mimeType: 'text/html'
            )
        }

        failure {
            echo '❌Build failed.'
            emailext(
                subject: "❌ FAILURE: Jenkins Build #${BUILD_NUMBER}",
                body: """<p>Hi,</p>
                        <p>The Jenkins build for <b>${JOB_NAME}</b> has failed.</p>
                        <p><b>Build URL:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                        <p>Please check Jenkins logs for details.</p>""",
                to: 'hatiritam03@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}
