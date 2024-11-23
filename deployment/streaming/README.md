
### Sending data

```bash
KINESIS_STREAM_INPUT=airbnb_events
aws kinesis put-record \
--stream-name ${KINESIS_STREAM_INPUT} \
--partition-key 1 \
--data "Hello, this is a test."
```

### Decoding base64

```bash
base64.b64decode(data_encoded).decode('utf-8')
```

### Record example

```json
{
   "input_data": {
        "room_type": "Entire home/apt",
        "neighbourhood": "SIXTH WARD",
        "latitude": 42.65222,
        "longitude": -73.76724,
        "minimum_nights": 2,
        "number_of_reviews": 302,
        "reviews_per_month": 2.53,
        "availability_365": 253
    },
    "input_id": 123
}
```

### Encoding base64
```bash
echo -n '{
    "input_data": {
        "room_type": "Entire home/apt",
        "neighbourhood": "SIXTH WARD",
        "latitude": 42.65222,
        "longitude": -73.76724,
        "minimum_nights": 2,
        "number_of_reviews": 302,
        "reviews_per_month": 2.53,
        "availability_365": 253
    },
    "input_id": 123
}' | base64
```

### Encoded records

```string
ewogICAgImlucHV0X2RhdGEiOiB7CiAgICAgICAgInJvb21fdHlwZSI6ICJFbnRpcmUgaG9tZS9h
cHQiLAogICAgICAgICJuZWlnaGJvdXJob29kIjogIlNJWFRIIFdBUkQiLAogICAgICAgICJsYXRp
dHVkZSI6IDQyLjY1MjIyLAogICAgICAgICJsb25naXR1ZGUiOiAtNzMuNzY3MjQsCiAgICAgICAg
Im1pbmltdW1fbmlnaHRzIjogMiwKICAgICAgICAibnVtYmVyX29mX3Jldmlld3MiOiAzMDIsCiAg
ICAgICAgInJldmlld3NfcGVyX21vbnRoIjogMi41MywKICAgICAgICAiYXZhaWxhYmlsaXR5XzM2
NSI6IDI1MwogICAgfSwKICAgICJpbnB1dF9pZCI6IDEyMwp9
```

### Sending records

```bash
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data 'ewogICAgImlucHV0X2RhdGEiOiB7CiAgICAgICAgInJvb21fdHlwZSI6ICJFbnRpcmUgaG9tZS9h
cHQiLAogICAgICAgICJuZWlnaGJvdXJob29kIjogIlNJWFRIIFdBUkQiLAogICAgICAgICJsYXRp
dHVkZSI6IDQyLjY1MjIyLAogICAgICAgICJsb25naXR1ZGUiOiAtNzMuNzY3MjQsCiAgICAgICAg
Im1pbmltdW1fbmlnaHRzIjogMiwKICAgICAgICAibnVtYmVyX29mX3Jldmlld3MiOiAzMDIsCiAg
ICAgICAgInJldmlld3NfcGVyX21vbnRoIjogMi41MywKICAgICAgICAiYXZhaWxhYmlsaXR5XzM2
NSI6IDI1MwogICAgfSwKICAgICJpbnB1dF9pZCI6IDEyMwp9'
```

### Test event

```json
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49657992070253376419733596328969809000942172840170356738",
                "data": "ewogICAgImlucHV0X2RhdGEiOiB7CiAgICAgICAgInJvb21fdHlwZSI6ICJFbnRpcmUgaG9tZS9hcHQiLAogICAgICAgICJuZWlnaGJvdXJob29kIjogIlNJWFRIIFdBUkQiLAogICAgICAgICJsYXRpdHVkZSI6IDQyLjY1MjIyLAogICAgICAgICJsb25naXR1ZGUiOiAtNzMuNzY3MjQsCiAgICAgICAgIm1pbmltdW1fbmlnaHRzIjogMiwKICAgICAgICAibnVtYmVyX29mX3Jldmlld3MiOiAzMDIsCiAgICAgICAgInJldmlld3NfcGVyX21vbnRoIjogMi41MywKICAgICAgICAiYXZhaWxhYmlsaXR5XzM2NSI6IDI1MwogICAgfSwKICAgICJpbnB1dF9pZCI6IDEyMwp9",
                "approximateArrivalTimestamp": 1732384532.966
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49657992070253376419733596328969809000942172840170356738",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::710915581521:role/lambda-kinesis-role",
            "awsRegion": "us-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:710915581521:stream/airbnb_events"
        }
    ]
}
```

### Reading from the stream

```bash
KINESIS_STREAM_OUTPUT='airbnb_predictions'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode
```

### Running the test
```bash
export PREDICTIONS_STREAM_NAME="ride_predictions"
export RUN_ID="e1efc53e9bd149078b0c12aeaa6365df"
export TEST_RUN="True"

python test.py
```

### Putting everythings to Docker
```bash
docker build -t stream-model-airbnb:v1 .

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="airbnb_predictions" \
    -e RUN_ID="7b5744464f544451aee4a9308d1971ad" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    stream-model-airbnb:v1
```

### URL for testing

* http://localhost:8080/2015-03-31/functions/function/invocations

### Configuring AWS CLI to run in Docker

To use AWS CLI, you may need to set the env variables:

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="airbnb_predictions" \
    -e RUN_ID="7b5744464f544451aee4a9308d1971ad" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    -e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    stream-model-duration:v1
```

Alternatively, you can mount the `.aws` folder with your credentials to the `.aws` folder in the container:

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="airbnb_predictions" \
    -e RUN_ID="7b5744464f544451aee4a9308d1971ad" \
    -e TEST_RUN="True" \
    -v c:/Users/alexe/.aws:/root/.aws \
    stream-model-duration:v1
```

### Publishing Docker images

Creating an ECR repo

```bash
aws ecr create-repository --repository-name airbnb-price-model
```

Logging in

```bash
$(aws ecr get-login --no-include-email)
```

Pushing 

```bash
REMOTE_URI="<REOMTE URI>"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}
LOCAL_IMAGE="stream-model-airbnb:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}
```
