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
                    // Use WinSCP for file transfer
                    powershell """
                        winscp.com /command "open scp://ec2-user:private_key.pem@52.205.11.86" "put script.py /home/ec2-user/" "exit"
                    """
                }
            }
        }

        // Remaining stages...
    }

    post {
        always {
            // Clean up the private key file after completion
            powershell 'Remove-Item private_key.pem'
        }
    }
}
