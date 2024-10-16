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
                        powershell """
                            aws s3 cp script.py s3://$BUCKET_NAME/pythonscripts/script.py --region us-east-1
                        """
                    }
                }
            }
        }

        stage('Download and Execute Script on EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                 credentialsId: 'AWS Jenkins credentials', 
                                 accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                 secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    script {
                        // First SSM command: download the script from S3
                        // Capture the command ID from the send-command output
                        def downloadCommandResult = powershell """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids $INSTANCE_ID --parameters commands=["aws s3 cp s3://$BUCKET_NAME/pythonscripts/script.py /home/ec2-user/script.py"] --region us-east-1
                        """
                        
                        // Assuming downloadCommandResult returns a JSON string; extract the command ID
                        def commandId = readJSON(text: downloadCommandResult).Command.CommandId  // Adjusted to correctly extract the command ID

                        // Delay to allow the copy to complete
                        sleep(time: 20, unit: "SECONDS")

                        // Retrieve command output
                        def commandOutput = powershell """
                            aws ssm list-command-invocations --command-id $commandId --details --region us-east-1
                        """
                        echo "SSM Command Output: ${commandOutput}"

                        // Second SSM command: execute the Python script on EC2
                        def ssmExecuteCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids $INSTANCE_ID --parameters commands=["python3 /home/ec2-user/script.py"] --region us-east-1
                        """
                        echo "Running SSM command to execute Python script on EC2"
                        powershell ssmExecuteCommand
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Script execution completed!'
        }
    }
}
