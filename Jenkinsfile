pipeline {
    agent any

    environment {
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

        stage('Upload Python Script using SSM') {
            steps {
                script {
                    // Run an SSM command to create the Python script directly on the EC2 instance
                    def command = 'echo "print(\\"Hello, S3!\\")" > /home/ec2-user/script.py'
                    powershell """
                        aws ssm send-command `
                        --document-name "AWS-RunShellScript" `
                        --instance-ids ${env.INSTANCE_ID} `
                        --parameters commands=["${command}"] `
                        --region us-east-1
                    """
                }
            }
        }

        // stage('Run Python Script using SSM') {
        //     steps {
        //         script {
        //             // Run an SSM command to execute the Python script
        //             powershell """
        //                 aws ssm send-command `
        //                 --document-name "AWS-RunShellScript" `
        //                 --instance-ids ${env.INSTANCE_ID} `
        //                 --parameters commands=["python3 /home/ec2-user/script.py"] `
        //                 --region us-east-1
        //             """
        //         }
        //     }
        // }
    }

    post {
        always {
            echo 'Pipeline completed!'
        }
    }
}
