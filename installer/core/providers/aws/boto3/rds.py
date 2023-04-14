import boto3


def get_rds_client(access_key, secret_key, region):
    """
    Returns the client object for AWS RDS

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        obj: AWS RDS Object
    """
    return boto3.client(
        'rds',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key)


def check_rds_instance_exists(instance_identifier, access_key, secret_key, region):
    """
    Check wheter the given RDS Instance already exists in the AWS Account

    Args:
        instance_identifier (str): RDS instance identifier
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        Boolean: True if env exists else False
    """
    client = get_rds_client(access_key, secret_key, region)
    try:
        response = client.describe_db_instances(
            DBInstanceIdentifier=instance_identifier
        )
        return bool(len(response['DBInstances']))
    except:
        return False


def check_rds_option_group_exists(name, access_key, secret_key, region):
    """
    Check wheter the given RDS Option Group already exists in the AWS Account

    Args:
        name (str): RDS Option Group name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        Boolean: True if env exists else False
    """
    client = get_rds_client(access_key, secret_key, region)
    try:
        response = client.describe_option_groups(
            OptionGroupName=name
        )
        return bool(len(response['OptionGroupsList']))
    except:
        return False


def check_rds_parameter_group_exists(name, access_key, secret_key, region):
    """
    Check wheter the given RDS Parameter Group already exists in the AWS Account

    Args:
        name (str): RDS Parameter Group name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        Boolean: True if env exists else False
    """
    client = get_rds_client(access_key, secret_key, region)
    try:
        response = client.describe_db_parameter_groups(
            DBParameterGroupName=name
        )
        return bool(len(response['DBParameterGroups']))
    except:
        return False


def check_rds_subnet_group_exists(name, access_key, secret_key, region):
    """
    Check wheter the given RDS SUbnet Group already exists in the AWS Account

    Args:
        name (str): RDS Subnet Group name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        Boolean: True if env exists else False
    """
    client = get_rds_client(access_key, secret_key, region)
    try:
        response = client.describe_db_subnet_groups(
            DBSubnetGroupName=name
        )
        return bool(len(response['DBSubnetGroups']))
    except:
        return False
