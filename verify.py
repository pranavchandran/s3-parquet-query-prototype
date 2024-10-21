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
        OUTPUT_FILE = '/home/ec2-user/output.csv'  // Path to the CSV file on EC2
        S3_OUTPUT_PATH = 's3://my-parquetfile-bucket/output.csv'  // Path in S3 to store the CSV
        LOCAL_OUTPUT_PATH = 'output.csv'  // Path to save the output locally in Jenkins
    }

    stages {
        // Upload script and execute steps remain the same

        // NEW STAGE to upload the output CSV from EC2 to S3
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
                    }
                }
            }
        }

        // NEW STAGE to download the output CSV from S3 to Jenkins
        stage('Download Output from S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'AWS Jenkins credentials']]) {
                    script {
                        echo "Downloading output.csv from S3 to Jenkins workspace"
                        sh """
                        aws s3 cp ${S3_OUTPUT_PATH} ${LOCAL_OUTPUT_PATH}
                        """
                    }
                }
            }
        }

        // Save the output CSV as a Jenkins artifact
        stage('Save Output as Artifact') {
            steps {
                echo "Saving output.csv as artifact"
                archiveArtifacts artifacts: "${LOCAL_OUTPUT_PATH}", allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed!'
        }
    }
}
