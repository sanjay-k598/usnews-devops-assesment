# import Packages
import boto3
import sys


# Variables
region= 'us-east-1'
ecs_ami= '/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id'
name= 'sanjay'

#establishing session with aws systems manager
client = boto3.client('ssm', region=region)

#Fetching latest ECS AMI
try:
    response = client.get_parameter(Name=ecs_ami)
    ami_id = response['Parameter']['Value']
    print("Successfully fetched latest ECS AMI")
except Exception as e:
    print("Error fetching ECS AMI ID:", str(e))
    sys.exit(1)

#EC2 creation involving AMI Id, instance type, min-max count, keypair, n/w interface, EBS, NSG, Subnet, Tags
ec2_ids = []
for i in range(10):
    instance_name = f'myinstance{i+1}'
    instance = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType='t3.micro',
        MaxCount=1,
        MinCount=1,
        KeyName=sanjay_keypair,
        NetworkInterfaces=[{
            'NetworkInterfaceId': eni.id,
            'DeviceIndex': 0,
        }],
      BlockDeviceMappings=[{
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 8,
                'VolumeType': 'gp2',
            }
        }],
      SecurityGroupIds=[security_group.id],
      SubnetId=subnet.id,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': instance_name}]
            }
        ]
    )
    instance_id = instance['Instances'][0]['InstanceId']
    ec2_ids.append(instance_id)

# S3 bucket creation and file upload.
for i, id in enumerate(ec2_ids, start=1):
    bucket_name = f'{name}-mys3bucket{i}'
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
  
    #creating file with instance id
    file_name = f'instance{i}_id.txt'
    with open(filename, 'w') as file:
        file.write(id)
    # S3 Upload
    s3_client.upload_file(file_name, bucket_name, file_name)

  

####Assumptions
#1. The lambda function runs on python 3.9 version
#2. To run use the below command
#    python3 Lambda_function.py
#3. While ec2 instance creation few parameters are hard coded and needs to be addressed for successfull running.
# lambda is assigned with proper IAM role for creation of the resources.
