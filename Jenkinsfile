pipeline {
    agent any

    environment {
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Your EC2 instance ID
        S3_BUCKET = 'my-parquetfile-bucket'  // Your S3 bucket name
        SCRIPT_PATH = 'pythonscripts/script.py'  // Path to the script in S3
    }

    stages {
        stage('Upload Script to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        powershell """
                            aws s3 cp .\\script.py s3://${S3_BUCKET}/${SCRIPT_PATH}
                        """
                    }
                }
            }
        }

        stage('Download Script from S3 to EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        echo "Running SSM command to download script from S3 to EC2"
                        def downloadCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["aws s3 cp s3://${S3_BUCKET}/${SCRIPT_PATH} /home/ec2-user/script.py"] --region us-east-1
                        """
                        def downloadResult = powershell(returnStdout: true, script: downloadCommand).trim()
                        echo "Download Command Result: ${downloadResult}"
                    }
                }
            }
        }

        stage('Execute Script on EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        echo "Running SSM command to execute Python script on EC2"
                        def executeCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["python3 /home/ec2-user/script.py"] --region us-east-1
                        """
                        def executeResult = powershell(returnStdout: true, script: executeCommand).trim()
                        echo "Execution Command Result: ${executeResult}"
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