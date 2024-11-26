### Building and runing Docker images

```bash
docker build -t stream-model-airbnb:v2 .
```

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="airbnb_predictions" \
    -e RUN_ID="1936d050006746eeaa60c76db167d18c" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    stream-model-airbnb:v2
```

### Mount the model folder:
```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="airbnb_predictions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    -v $(pwd)/model:/app/model \
    stream-model-airbnb:v2
```

## Specifying endpoint URL

```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis list-streams
```

```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name airbnb_predictions \
    --shard-count 1
```

```bash
aws  --endpoint-url=http://localhost:4566 \
    kinesis     get-shard-iterator \
    --shard-id ${SHARD} \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --query 'ShardIterator'
```

### Unable to locate credentials

If you get 'Unable to locate credentials' error, add these env variables to the docker-compose.yaml file:

- AWS_ACCESS_KEY_ID=abc
- AWS_SECRET_ACCESS_KEY=xyz


### Make

Without make:

```bash
isort .
black .
pylint --recursive=y .
pytest tests/
```

With make:

```bash
make quality_checks
make test
```

To prepare the project, run

```bash
make setup
```

## Infrastructure as Code (IaC) with Terraform

### Setup

This guide explains how to set up and configure Terraform and AWS CLI for managing AWS infrastructure as code.

### Installation
1. Install AWS CLI
Both AWS CLI v1 and v2 are supported. You can download and install it from [AWS CLI official documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

2. Install Terraform
Download and install the Terraform CLI from the [Terraform documentation](https://developer.hashicorp.com/terraform/install).

### Configuration

1. **Generate AWS Access Keys**
    * Log in to your AWS Management Console.
    * Go to the IAM section.
    * Create an access key and secret key for your user.
    * Download and store the keys securely.
    * Configure AWS CLI Use the AWS CLI to configure your credentials.

    ```bash
    $ aws configure
    AWS Access Key ID [None]: <Your Access Key ID>
    AWS Secret Access Key [None]: <Your Secret Access Key>
    Default region name [None]: us-east-1
    Default output format [None]: json
    ```

2. **Verify AWS Configuration** Run the following command to ensure your AWS credentials are set up correctly:

    ```bash
    $ aws sts get-caller-identity
    ```

    This command should return your AWS account information, confirming the configuration is correct.

3. **(Optional) Configure AWS Profiles** If you need multiple configurations for different environments, you can set up named profiles. Refer to:

    * [AWS CLI named profiles documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html).
    * Additional details [here](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#using-an-external-credentials-process).