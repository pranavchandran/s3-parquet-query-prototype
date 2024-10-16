pipeline {
    agent any

    environment {
        // Define SSH key for Jenkins to access EC2 (though not needed for SSM, this is still stored for SSH steps)
        SSH_KEY = credentials('e6662271-9b92-4b6d-a85a-682052c16d94')
        INSTANCE_ID = 'i-0a7aa679b6c66fb59'  // Update with your EC2 instance ID
    }

    parameters {
        string(name: 'BUCKET_NAME', defaultValue: 'my-parquetfile-bucket', description: 'Name of the S3 bucket')
        string(name: 'ASSET_ID', defaultValue: 'A001', description: 'ASSET ID to query')
        string(name: 'YEAR', defaultValue: '2024', description: 'Year folder in S3')
        string(name: 'MONTH', defaultValue: '10', description: 'Month folder in S3')
        string(name: 'START_DAY', defaultValue: 'day1', description: 'Start day of the date range')
        string(name: 'END_DAY', defaultValue: 'day1', description: 'End day of the date range')
        string(name: 'TAG_NAME', defaultValue: 'Temperature', description: 'Tag name to filter data')
    }

    stages {
        stage('Initialize') {
            steps {
                echo "Initializing S3 query with the following parameters:"
                echo "Bucket: ${params.BUCKET_NAME}"
                echo "Asset: ${params.ASSET_ID}"
                echo "Year: ${params.YEAR}"
                echo "Month: ${params.MONTH}"
                echo "Date Range: ${params.START_DAY} to ${params.END_DAY}"
                echo "Tag Name: ${params.TAG_NAME}"
                echo "EC2 Instance ID: ${env.INSTANCE_ID}"
            }
        }

        stage('Upload Python Script to EC2 using SSM') {
            steps {
                script {
                    // Using AWS SSM to upload the script to EC2 instance
                    powershell """
                        aws ssm send-command `
                        --document-name "AWS-RunShellScript" `
                        --instance-ids ${env.INSTANCE_ID} `
                        --parameters commands=["echo '${env.SSH_KEY}' > /home/ec2-user/private_key.pem", "chmod 400 /home/ec2-user/private_key.pem", "echo 'print(\"Hello, S3!\")' > /home/ec2-user/script.py"] `
                        --region us-east-1
                    """
                }
            }
        }

        stage('Run Python Script on EC2 using SSM') {
            steps {
                script {
                    // Use AWS SSM to execute the Python script on the EC2 instance
                    powershell """
                        aws ssm send-command `
                        --document-name "AWS-RunShellScript" `
                        --instance-ids ${env.INSTANCE_ID} `
                        --parameters commands=["python3 /home/ec2-user/script.py ${params.BUCKET_NAME} ${params.ASSET_ID} ${params.YEAR} ${params.MONTH} ${params.START_DAY} ${params.END_DAY} ${params.TAG_NAME}"] `
                        --region us-east-1
                    """
                }
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'output_*.csv', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            // Clean up if necessary, though SSM takes care of managing command sessions
            echo 'Finished the Jenkins pipeline.'
        }
    }
}
