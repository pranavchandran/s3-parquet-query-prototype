pipeline {
    agent any

    parameters {
        string(name: 'BUCKET_NAME', defaultValue: '', description: 'Name of the S3 bucket')
        string(name: 'ASSET_ID', defaultValue: '', description: 'ASSET ID to query')
        string(name: 'YEAR', defaultValue: '', description: 'Year folder in S3')
        string(name: 'MONTH', defaultValue: '', description: 'Month folder in S3')
        string(name: 'START_DAY', defaultValue: '', description: 'Start day of the date range')
        string(name: 'END_DAY', defaultValue: '', description: 'End day of the date range')
        string(name: 'TAG_NAME', defaultValue: '', description: 'Tag name to filter data')
        string(name: 'INSTANCE_ID', defaultValue: 'i-05aa5523aa341d722', description: 'ID of the EC2 instance')
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
                echo "INSTANCE_ID: ${params.INSTANCE_ID}"
            }
        }

        stage('Read Python Script') {
            steps {
                script {
                    // Read the python script from the Jenkins workspace after checkout
                    def scriptContent = readFile('script.py')
                    // Store the script content as a variable for use in the next stage
                    env.PYTHON_SCRIPT = scriptContent
                }
            }
        }

        stage('Install Dependencies and Upload Script to EC2') {
            steps {
                script {
                    // Use SSM to install dependencies and upload the script
                    sh """
                        aws ssm send-command \
                        --document-name "AWS-RunShellScript" \
                        --targets "Key=instanceIds,Values=${params.INSTANCE_ID}" \
                        --parameters 'commands=["sudo yum install -y python3-pip", "pip3 install pandas pyarrow boto3", "echo \\"${env.PYTHON_SCRIPT}\\" > /home/ec2-user/script.py", "chmod +x /home/ec2-user/script.py"]' \
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
                        --targets "Key=instanceIds,Values=${params.INSTANCE_ID}" \
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
}
