pipeline {
    agent any

    environment {
        SSH_KEY = credentials('e6662271-9b92-4b6d-a85a-682052c16d94') // Update with your SSH credentials ID
    }

    stages {
        stage('Transfer Python Script to EC2') {
            steps {
                script {
                    // Write the SSH key to a temporary file for SCP
                    writeFile file: 'private_key.pem', text: "${env.SSH_KEY}"

                    // Use SCP to copy the Python script to the EC2 instance
                    sh '''
                    chmod 400 private_key.pem
                    scp -i private_key.pem -o StrictHostKeyChecking=no script.py ec2-user@52.205.11.86:/home/ec2-user/
                    '''
                }
            }
        }
    }

    post {
        always {
            // Clean up the private key file after completion
            sh 'rm private_key.pem'
        }
    }
}
