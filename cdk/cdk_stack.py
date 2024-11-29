from aws_cdk import (
    App, Stack, 
    aws_ec2 as ec2,
    aws_s3 as s3,
    CfnOutput,
    RemovalPolicy
)


class CdkStack(Stack):

    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Step 1: Create a VPC
        vpc = ec2.Vpc(self, "MyVpc",
                      cidr="10.0.0.0/16",
                      max_azs=1,
                      enable_dns_support=True,
                      enable_dns_hostnames=True
                      )
        CfnOutput(self, "VpcId", value=vpc.vpc_id)

        # Step 2: Create a public subnet
        subnet = ec2.Subnet(self, "MyPublicSubnet",
                            cidr_block="10.0.1.0/24",
                            availability_zone="eu-north-1b",
                            vpc_id=vpc.vpc_id,
                            map_public_ip_on_launch=True
                            )
        CfnOutput(self, "SubnetId", value=subnet.subnet_id)

        # Step 3: Launch an EC2 instance in the public subnet
        instance = ec2.Instance(self, "MyInstance",
                                instance_type=ec2.InstanceType("t3.micro"),
                                machine_image=ec2.MachineImage.
                                latest_amazon_linux(),
                                vpc=vpc,
                                vpc_subnets=ec2.SubnetSelection(
                                    subnets=[subnet]),
                                key_name="TestUserKeyPair"
                                )
        CfnOutput(self, "InstanceId", value=instance.instance_id)

        # Step 4: Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket",
                           bucket_name="test-user-todo-app-bucket",
                           removal_policy=RemovalPolicy.DESTROY
                           )
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
