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
                        sh """
                            aws s3 cp script.py s3://$BUCKET_NAME/script.py --region us-east-1
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
                        // Download the script from S3 to EC2
                        sh """
                            aws ssm send-command \
                            --document-name "AWS-RunShellScript" \
                            --instance-ids $INSTANCE_ID \
                            --parameters commands=["aws s3 cp s3://$BUCKET_NAME/script.py /home/ec2-user/script.py"] \
                            --region us-east-1
                        """

                        // Execute the Python script on EC2
                        sh """
                            aws ssm send-command \
                            --document-name "AWS-RunShellScript" \
                            --instance-ids $INSTANCE_ID \
                            --parameters commands=["python3 /home/ec2-user/script.py"] \
                            --region us-east-1
                        """
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
