pipeline {
    agent any

    environment {
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Your EC2 instance ID
    }

    stages {
        stage('Send SSM Command') {
            steps {
                script {
                    // Test SSM command to simply echo a message on the EC2 instance
                    powershell """
                        aws ssm send-command `
                        --document-name "AWS-RunShellScript" `
                        --instance-ids ${env.INSTANCE_ID} `
                        --parameters commands=["echo Hello from Jenkins via SSM!"] `
                        --region us-east-1
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'SSM Command Test Completed!'
        }
    }
}
