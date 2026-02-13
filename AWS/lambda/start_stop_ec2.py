import boto3
import json

'''
event → contains input data (like { "action": "start" })

context → runtime info about the Lambda execution
'''
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:12345678:alb-sns-demo'
    
    tag_key = 'AutoStartStop'
    tag_value = 'True'

    # Get EC2 instances with tag AutoStartStop=True
    instances = ec2.describe_instances(
        Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
    )

    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    if not instance_ids:
        message = "No EC2 instances found with AutoStartStop=True"
        print(message)
        return {"statusCode": 200, "body": message}

    action = event.get('action', 'stop').lower()

    if action == 'start':
        ec2.start_instances(InstanceIds=instance_ids)
        subject = "EC2 Auto-Start Notification"
        message = f"Started EC2 instances:\n{instance_ids}"

    elif action == 'stop':
        ec2.stop_instances(InstanceIds=instance_ids)
        subject = "EC2 Auto-Stop Notification"
        message = f"Stopped EC2 instances:\n{instance_ids}"

    else:
        return {
            "statusCode": 400,
            "body": "Invalid action. Use 'start' or 'stop'."
        }

    # 🔔 Send SNS Notification
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )

    return {
        "statusCode": 200,
        "body": message
    }
