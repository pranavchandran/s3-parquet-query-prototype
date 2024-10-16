pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = credentials('AKIAYS2NUES34S77JGCC')  // Replace with the ID of your AWS credentials in Jenkins
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Your EC2 instance ID
    }

    stages {
        stage('Send SSM Command') {
            steps {
                script {
                    // Export AWS credentials for the session
                    powershell """
                        set AWS_ACCESS_KEY_ID=${AWS_CREDENTIALS_USR}
                        set AWS_SECRET_ACCESS_KEY=${AWS_CREDENTIALS_PSW}
                        
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
