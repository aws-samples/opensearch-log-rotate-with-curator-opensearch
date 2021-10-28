# Amazon OpenSearch Service log rotate with curator

This repository is used for running log rotate on OpenSearch.
It uses the [AWS SAM CLI](https://github.com/aws/aws-sam-cli) to build and deploy this project.

## Prerequisites

1. [install](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) AWS SAM CLI
2. Install docker inorder to build the project using `--use-container` option
> You can build the project with python 3.8 installed on your machine, or using virtual environment with python 3.8

## Configuration

Edit `samconfig.toml` with a unique s3 bucket `s3_bucket` and the region `region` you want to install this project.

These are the configuration changes on `template.yaml` required before running this project

1. Update environment variable `OPENSEARCH_HOST` with your OpenSearch domain URL
2. Update environment variable `RETENTION_IN_DAYS` with the number of days you want to keep an index
3. Update `SecurityGroupIds` section with a proper security group that will allow access to OpenSearch domain on port 443
4. Update `SubnetIds` section with a subnet that will allow the Lambda to run in your OpenSearch VPC
5. Optionally update `Resources` section from `'*'` to your specific ARN of OpenSearch Domain, we highly recommend to always grant the least privileges possible for a resource
6. Optionally update `Schedule` from the default once a day to your choosing

## Deploy

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name opensearch-log-rotate-curator
```

### Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

### License

This repository is licensed under the MIT-0 License. See the LICENSE file.