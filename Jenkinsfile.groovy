pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
        STACK_NAME = 'lamda-event-bridge'
        TEMPLATE_FILE = 'Lambda_CFT.yaml'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/sanjay-k598/usnews-devops-assesment.git'
            }
        }
        stage('Deploy Lambda') {
            steps {
                script {
                    // Zip the Lambda function code
                    sh 'zip -r sanjay-lambda-code.zip .'

                    // Upload to S3
                    sh '''
                    aws s3 cp sanjay-lambda-code.zip s3://sanjay-lambda-python-code/sanjay-lambda-code.zip
                    '''

                    // Deployment of CFT
                    sh '''
                    aws cloudformation deploy \
                        --region $AWS_REGION \
                        --stack-name $STACK_NAME \
                        --template-file $TEMPLATE_FILE
                    '''
                }
            }
        }
    }
    post {
        success {
            echo 'CFT deployed successfully.'
        }
        failure {
            echo 'CFT Deployment failed.'
        }
    }
}
