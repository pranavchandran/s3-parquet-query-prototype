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

        stage('Install AWS CLI and Dependencies on EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        echo "Running SSM command to install AWS CLI and dependencies on EC2"
                        def installCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["sudo yum install -y aws-cli python3-pip && python3 -m venv myenv && source myenv/bin/activate && pip install boto3 python-dateutil"] --region us-east-1
                        """
                        def installResult = powershell(returnStdout: true, script: installCommand).trim()
                        echo "Install Command Result: ${installResult}"

                        // Check the status of the SSM command
                        def commandId = installResult =~ /"CommandId":\s*"([^"]+)"/
                        if (commandId) {
                            commandId = commandId[0][1]
                            echo "Checking status of SSM command with CommandId: ${commandId}"
                            sleep(time: 30, unit: 'SECONDS')  // Wait for the command to complete
                            def statusCommand = """
                                aws ssm list-command-invocations --command-id ${commandId} --details --region us-east-1
                            """
                            def statusResult = powershell(returnStdout: true, script: statusCommand).trim()
                            echo "SSM Command Status: ${statusResult}"
                        } else {
                            error "Failed to retrieve CommandId from install command result"
                        }
                    }
                }
            }
        }

        stage('Verify AWS CLI Installation on EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        echo "Running SSM command to verify AWS CLI installation on EC2"
                        def verifyCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["source myenv/bin/activate && aws --version"] --region us-east-1
                        """
                        def verifyResult = powershell(returnStdout: true, script: verifyCommand).trim()
                        echo "Verify Command Result: ${verifyResult}"

                        // Check the status of the SSM command
                        def commandId = verifyResult =~ /"CommandId":\s*"([^"]+)"/
                        if (commandId) {
                            commandId = commandId[0][1]
                            echo "Checking status of SSM command with CommandId: ${commandId}"
                            sleep(time: 30, unit: 'SECONDS')  // Wait for the command to complete
                            def statusCommand = """
                                aws ssm list-command-invocations --command-id ${commandId} --details --region us-east-1
                            """
                            def statusResult = powershell(returnStdout: true, script: statusCommand).trim()
                            echo "SSM Command Status: ${statusResult}"
                        } else {
                            error "Failed to retrieve CommandId from verify command result"
                        }
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
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["source myenv/bin/activate && aws s3 cp s3://${S3_BUCKET}/${SCRIPT_PATH} /home/ec2-user/script.py"] --region us-east-1
                        """
                        def downloadResult = powershell(returnStdout: true, script: downloadCommand).trim()
                        echo "Download Command Result: ${downloadResult}"

                        // Check the status of the SSM command
                        def commandId = downloadResult =~ /"CommandId":\s*"([^"]+)"/
                        if (commandId) {
                            commandId = commandId[0][1]
                            echo "Checking status of SSM command with CommandId: ${commandId}"
                            sleep(time: 30, unit: 'SECONDS')  // Wait for the command to complete
                            def statusCommand = """
                                aws ssm list-command-invocations --command-id ${commandId} --details --region us-east-1
                            """
                            def statusResult = powershell(returnStdout: true, script: statusCommand).trim()
                            echo "SSM Command Status: ${statusResult}"
                        } else {
                            error "Failed to retrieve CommandId from download command result"
                        }
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
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["source myenv/bin/activate && python3 /home/ec2-user/script.py"] --region us-east-1
                        """
                        def executeResult = powershell(returnStdout: true, script: executeCommand).trim()
                        echo "Execution Command Result: ${executeResult}"

                        // Check the status of the SSM command
                        def commandId = executeResult =~ /"CommandId":\s*"([^"]+)"/
                        if (commandId) {
                            commandId = commandId[0][1]
                            echo "Checking status of SSM command with CommandId: ${commandId}"
                            sleep(time: 30, unit: 'SECONDS')  // Wait for the command to complete
                            def statusCommand = """
                                aws ssm list-command-invocations --command-id ${commandId} --details --region us-east-1
                            """
                            def statusResult = powershell(returnStdout: true, script: statusCommand).trim()
                            echo "SSM Command Status: ${statusResult}"
                        } else {
                            error "Failed to retrieve CommandId from execute command result"
                        }
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