pipeline {
    agent any

    environment {
        BUCKET_NAME = 'my-parquetfile-bucket'
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'
    }

    stages {
        stage('Upload Script to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                 credentialsId: 'AWS Jenkins credentials', 
                                 accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        // Upload script to S3
                        powershell """
                            aws s3 cp script.py s3://$BUCKET_NAME/pythonscripts/script.py --region us-east-1
                        """
                    }
                }
            }
        }

        stage('Test SSM Command') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                 credentialsId: 'AWS Jenkins credentials', 
                                 accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        // Test command execution via SSM
                        def testSSMCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids $INSTANCE_ID --parameters commands=["echo Hello from SSM"] --region us-east-1
                        """
                        echo "Running test SSM command"
                        def testResult = powershell testSSMCommand
                        echo "Test Command Result: ${testResult}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed!'
        }
    }
}
