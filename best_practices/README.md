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
    -e AWS_DEFAULT_REGION="eu-west-1" \
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
