pipeline {
    agent any

    environment {
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Your EC2 instance ID
    }

    stages {
        stage('Send SSM Command') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                 credentialsId: 'AWS Jenkins credentials', 
                                 accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        // Use AWS credentials for SSM command
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
    }

    post {
        always {
            echo 'SSM Command Test Completed!'
        }
    }
}
