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

        stage('Download Script from S3 to EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                 credentialsId: 'AWS Jenkins credentials', 
                                 accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        // Download the script from S3 to EC2
                        def downloadCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids $INSTANCE_ID --parameters commands=["aws s3 cp s3://$BUCKET_NAME/pythonscripts/script.py /home/ec2-user/script.py"] --region us-east-1
                        """
                        echo "Running SSM command to download script from S3 to EC2"
                        def downloadResult = powershell downloadCommand
                        echo "Download Command Result: ${downloadResult}"

                        // Extract CommandId for further checking
                        def commandId = (downloadResult =~ /"CommandId":\s*"(.*?)"/)[0][1]
                        sleep(time: 20, unit: "SECONDS")

                        // Check command output
                        def commandOutput = powershell """
                            aws ssm list-command-invocations --command-id $commandId --details --region us-east-1
                        """
                        echo "Download Command Output: ${commandOutput}"
                    }
                }
            }
        }

        stage('Execute Script on EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                 credentialsId: 'AWS Jenkins credentials', 
                                 accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        // Execute the script on EC2
                        def executeCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids $INSTANCE_ID --parameters commands=["python3 /home/ec2-user/script.py"] --region us-east-1
                        """
                        echo "Running SSM command to execute Python script on EC2"
                        def executeResult = powershell executeCommand
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
