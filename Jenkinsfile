pipeline {
    agent any

    environment {
        SSH_KEY = credentials('e6662271-9b92-4b6d-a85a-682052c16d94') // Replace with your actual credentials ID
        EC2_HOST = "ec2-user@52.205.11.86"  // Your EC2 instance's public DNS or IP
        FILE_TO_COPY = "script.py" // The file you want to copy
        REMOTE_PATH = "/home/ec2-user/" // The destination directory on EC2
    }

    stages {
        stage('Transfer Python Script to EC2') {
            steps {
                script {
                    // Write the private key file for SCP
                    writeFile file: 'private_key.pem', text: "${SSH_KEY}"

                    // Adjust SCP command for Windows
                    bat """
                    chmod 400 private_key.pem
                    scp -i private_key.pem -o StrictHostKeyChecking=no ${FILE_TO_COPY} ${EC2_HOST}:${REMOTE_PATH}
                    """
                }
            }
        }
    }

    post {
        always {
            // Clean up the private key file after execution
            bat 'del private_key.pem'
        }
    }
}
