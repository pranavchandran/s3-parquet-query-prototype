pipeline {
    agent any

    environment {
        SSH_KEY = credentials('e6662271-9b92-4b6d-a85a-682052c16d94') // SSH key stored in Jenkins credentials
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
                echo "Using EC2 Public IP: 52.205.11.86"
            }
        }

        stage('Upload Python Script to EC2') {
            steps {
                script {
                    // Write the SSH key to a temporary file
                    writeFile file: 'private_key.pem', text: "${env.SSH_KEY}"
                    
                    // Ensure the permissions on the key file are correct for use in SSH
                    sh 'chmod 600 private_key.pem'
                    
                    // Upload the Python script to the EC2 instance using SCP
                    sh """
                        scp -i private_key.pem script.py ec2-user@52.205.11.86:/home/ec2-user/script.py
                    """
                }
            }
        }

        stage('Install Dependencies on EC2') {
            steps {
                script {
                    // Use AWS SSM to install Python dependencies on the EC2 instance
                    sh """
                        aws ssm send-command \
                        --document-name "AWS-RunShellScript" \
                        --targets "Key=instanceIds,Values=i-0a7aa679b6c66fb59" \
                        --parameters 'commands=["sudo yum install -y python3-pip", "pip3 install pandas pyarrow boto3"]' \
                        --region us-east-1
                    """
                }
            }
        }

        stage('Run Python Script on EC2') {
            steps {
                script {
                    // Execute the Python script on the EC2 instance
                    sh """
                        aws ssm send-command \
                        --document-name "AWS-RunShellScript" \
                        --targets "Key=instanceIds,Values=i-0a7aa679b6c66fb59" \
                        --parameters 'commands=["python3 /home/ec2-user/script.py ${params.BUCKET_NAME} ${params.ASSET_ID} ${params.YEAR} ${params.MONTH} ${params.START_DAY} ${params.END_DAY} ${params.TAG_NAME}"]' \
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
            // Clean up the private key file after completion
            sh 'rm private_key.pem'
        }
    }
}
