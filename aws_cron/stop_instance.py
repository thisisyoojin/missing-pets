import boto3

def invoke_lambda(region, access_key, secret_key):
    client = boto3.client('lambda', 
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
            )
    response = client.invoke(FunctionName='stop-the-ec2')
    print(response)