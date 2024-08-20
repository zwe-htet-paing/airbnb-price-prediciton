```
KINESIS_STREAM_INPUT=airbnb_events
aws kinesis put-record \
--stream-name ${KINESIS_STREAM_INPUT} \
--partition-key 1 \
--data "Hello, this is a test."
```