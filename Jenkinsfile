pipeline {
    agent any

//     passing the parameters to the pipeline
    parameters {
        string(name: 'BUCKET_NAME', defaultValue: '', description: 'Name of the S3 bucket')
        string(name: 'ASSET_ID', defaultValue: '', description: 'ASSET ID to query')
        string(name: 'YEAR', defaultValue: '', description: 'Year folder in S3')
        string(name: 'MONTH', defaultValue: '', description: 'Month folder in S3')
        string(name: 'START_DAY', defaultValue: '', description: 'Start day of the date range')
        string(name: 'END_DAY', defaultValue: '', description: 'End day of the date range')
        string(name: 'TAG_NAME', defaultValue: '', description: 'Tag name to filter data')
    }

//  stages
    stages {
        stage('Initialize') {
            steps {
                echo "Initializing s3 query with the following parameters:"
                echo "Bucket: ${params.BUCKET_NAME}"
                echo "Asset: ${params.ASSET_ID}"
                echo "Year: ${params.YEAR}"
                echo "Month: ${params.MONTH}"
                echo "Date Range: ${params.START_DAY} to ${params.END_DAY}"
                echo "Tag Name: ${params.TAG_NAME}"
            }
        }

        stage('Run S3 Query') {
            steps {
                echo "Executing query on S3"
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'output_*.csv', allowEmptyArchive: true
            }
        }
    }
}
