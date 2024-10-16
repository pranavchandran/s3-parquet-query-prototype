pipeline {
    agent any

    environment {
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Your EC2 instance ID
    }

    stages {
        stage('Send SSM Command') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        // Use the AWS credentials correctly
                        powershell """
                            $env:AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
                            $env:AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
                            aws ssm send-command `
                            --document-name "AWS-RunShellScript" `
                            --instance-ids ${env.INSTANCE_ID} `
                            --parameters commands=["echo 'print(\\\"Hello, S3!\\\")' > /home/ec2-user/script.py"] `
                            --region us-east-1
                        """
                    }
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
