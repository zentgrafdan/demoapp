# GitHub Actions Lambda Deployment Setup

This guide explains how to set up automatic deployment of your three Lambda functions using GitHub Actions.

## Overview

The workflow automatically deploys updates to three AWS Lambda functions:
- **Frontend Service** (`demofrontend/demofrontend.py`)
- **Transaction Service** (`demotxnsvc/demotxnsvc.py`)
- **User Service** (`demousersvc/demousersvc.py`)

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **IAM User** with Lambda update permissions
3. **Lambda Functions** already created in AWS

## Required AWS Permissions

Your IAM user needs the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "lambda:GetFunction"
            ],
            "Resource": "arn:aws:lambda:*:*:function:*"
        }
    ]
}
```

## GitHub Repository Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

### Required Secrets:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `FRONTEND_LAMBDA_FUNCTION_NAME` - Name of your frontend Lambda function
- `TXNSVC_LAMBDA_FUNCTION_NAME` - Name of your transaction service Lambda function
- `USERSVC_LAMBDA_FUNCTION_NAME` - Name of your user service Lambda function

### Optional Configuration:
- Update `AWS_REGION` in the workflow file if not using `us-east-1`

## How It Works

1. **Trigger**: Workflow runs on push to main/master branch or pull requests
2. **Dependencies**: Installs any requirements from `requirements.txt` files
3. **Packaging**: Creates ZIP files for each service
4. **Deployment**: Updates Lambda function code and configuration
5. **Parallel Execution**: All three services deploy simultaneously

## Workflow Features

- **Automatic Dependency Management**: Installs packages from requirements.txt
- **Clean Packaging**: Excludes unnecessary files (pyc, cache, git)
- **Runtime Configuration**: Sets Python 3.9 runtime for all functions
- **Error Handling**: Each service deploys independently

## Customization

### Adding Dependencies
If you need external packages, add them to the respective `requirements.txt` file:
```
requests==2.28.1
boto3==1.26.0
```

### Changing Python Version
Update the `python-version` in the workflow file:
```yaml
python-version: '3.10'  # or '3.11', '3.12'
```

### Adding Environment Variables
To set Lambda environment variables, add this step after deployment:
```yaml
- name: Set Environment Variables
  run: |
    aws lambda update-function-configuration \
      --function-name ${{ secrets.FUNCTION_NAME }} \
      --environment Variables='{"KEY":"VALUE"}' \
      --region ${{ env.AWS_REGION }}
```

## Troubleshooting

### Common Issues:

1. **Permission Denied**: Check IAM permissions
2. **Function Not Found**: Verify function names in secrets
3. **Deployment Package Too Large**: Check for unnecessary files
4. **Runtime Mismatch**: Ensure Python version compatibility

### Debug Steps:

1. Check workflow logs in GitHub Actions
2. Verify AWS credentials are correct
3. Confirm Lambda function names exist
4. Check AWS region configuration

## Security Notes

- Never commit AWS credentials to the repository
- Use IAM roles with minimal required permissions
- Regularly rotate access keys
- Monitor deployment logs for security issues

## Support

For issues or questions:
1. Check GitHub Actions logs
2. Verify AWS CloudWatch logs
3. Review IAM permissions
4. Test AWS CLI commands locally
