stage('Test SSM Command') {
    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                         credentialsId: 'AWS Jenkins credentials', 
                         accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                         secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
            script {
                def testSSMCommand = """
                    aws ssm send-command --document-name "AWS-RunShellScript" --instance-ids $INSTANCE_ID --parameters commands=["echo Hello from SSM"] --region us-east-1
                """
                echo "Running test SSM command"
                def testResult = powershell testSSMCommand
                echo "Test Command Result: ${testResult}"
            }
        }
    }
}
