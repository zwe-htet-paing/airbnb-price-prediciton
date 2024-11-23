import requests 

event = {
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


url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(url, json=event)
print(response.json())