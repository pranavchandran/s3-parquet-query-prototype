pipeline {
    agent any

    parameters {
        string(name: 'BUCKET_NAME', defaultValue: 'my-parquetfile-bucket', description: 'S3 Bucket Name')
        string(name: 'ASSET_ID', defaultValue: 'A001', description: 'Asset ID')
        string(name: 'YEAR', defaultValue: '2024', description: 'Year')
        string(name: 'MONTH', defaultValue: '2', description: 'Month')
        string(name: 'START_DAY', defaultValue: '1', description: 'Start Day')
        string(name: 'END_DAY', defaultValue: '3', description: 'End Day')
        string(name: 'TAG_NAME', defaultValue: 'Temperature', description: 'Tag Name')
    }

    environment {
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Your EC2 instance ID
        SCRIPT_PATH = 'pythonscripts/script.py'  // Path to the script in S3
        OUTPUT_FILE = '/home/ec2-user/output.csv'  // Path to the CSV file on EC2
        LOCAL_OUTPUT_PATH = 'output.csv'  // Path to save the output locally in Jenkins
        S3_OUTPUT_PATH = 's3://my-parquetfile-bucket/output.csv'  // Path in S3 to store the CSV
    }

    stages {
        stage('Upload Script to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        powershell """
                            aws s3 cp .\\script.py s3://${params.BUCKET_NAME}/${SCRIPT_PATH}
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
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["sudo yum install -y aws-cli python3-pip && python3 -m venv /home/ec2-user/myenv && source /home/ec2-user/myenv/bin/activate && pip install --upgrade awscli boto3 python-dateutil pandas pyarrow"] --region us-east-1
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
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["source /home/ec2-user/myenv/bin/activate && aws --version"] --region us-east-1
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
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["source /home/ec2-user/myenv/bin/activate && aws s3 cp s3://${params.BUCKET_NAME}/${SCRIPT_PATH} /home/ec2-user/script.py"] --region us-east-1
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
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["source /home/ec2-user/myenv/bin/activate && python3 /home/ec2-user/script.py ${params.BUCKET_NAME} ${params.ASSET_ID} ${params.YEAR} ${params.MONTH} ${params.START_DAY} ${params.END_DAY} ${params.TAG_NAME} | tee /home/ec2-user/script_output.log"] --region us-east-1
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

                            // Fetch the script output log
                            def fetchLogCommand = """
                                aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["cat /home/ec2-user/script_output.log"] --region us-east-1
                            """
                            def fetchLogResult = powershell(returnStdout: true, script: fetchLogCommand).trim()
                            echo "Fetch Log Command Result: ${fetchLogResult}"

                            def logCommandId = fetchLogResult =~ /"CommandId":\s*"([^"]+)"/
                            if (logCommandId) {
                                logCommandId = logCommandId[0][1]
                                echo "Checking status of SSM command with CommandId: ${logCommandId}"
                                sleep(time: 30, unit: 'SECONDS')  // Wait for the command to complete
                                def logStatusCommand = """
                                    aws ssm list-command-invocations --command-id ${logCommandId} --details --region us-east-1
                                """
                                def logStatusResult = powershell(returnStdout: true, script: logStatusCommand).trim()
                                echo "SSM Command Log Status: ${logStatusResult}"
                            } else {
                                error "Failed to retrieve CommandId from fetch log command result"
                            }
                        } else {
                            error "Failed to retrieve CommandId from execute command result"
                        }
                    }
                }
            }
        }
        stage('Upload Output to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                       echo "Running SSM command to upload output.csv from EC2 to S3"
                       def uploadCommand = """
                            aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids ${INSTANCE_ID} --parameters commands=["aws s3 cp ${OUTPUT_FILE} ${S3_OUTPUT_PATH}"] --region us-east-1
                       """
                       def uploadResult = powershell(returnStdout: true, script: uploadCommand).trim()
                       echo "Upload Command Result: ${uploadResult}"

                       def commandId = uploadResult =~ /"CommandId":\s*"([^"]+)"/
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
                            error "Failed to retrieve CommandId from upload command result"
                       }
                    }
                }
            }
        }
        stage ('Download Output from s3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        echo "Downloading output.csv from S3 to Jenkins Workspace"
                        powershell """
                        aws s3 cp ${S3_OUTPUT_PATH} ${LOCAL_OUTPUT_PATH}
                        """
                    }
                }
            }
        }
        stage ('Save Output as Artifact') {
            steps {
                echo "Saving output.csv as artifact"
                archiveArtifacts artifacts: "${LOCAL_OUTPUT_PATH}"
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed!'
        }
    }
}
