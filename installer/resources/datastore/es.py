from core.terraform.resources.aws.elasticsearch import ElasticsearchDomainResource, ElasticsearchDomainPolicyResource
from core.terraform.resources.aws.cloudwatch import CloudWatchLogGroupResource, CloudWatchLogResourcePolicy
from core.providers.aws.boto3.iam import create_iam_service_linked_role
from resources.vpc.security_group import InfraSecurityGroupResource
from core.config import Settings
from core.log import SysLog
import json


class ESCloudWatchLogGroup(CloudWatchLogGroupResource):
    name = "elasticsearch"
    retention_in_days = 7


class ESCloudWatchLogResourcePolicy(CloudWatchLogResourcePolicy):
    policy_name = "elasticSearch"
    policy_document = '''{
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "es.amazonaws.com"
            },
            "Action": [
              "logs:PutLogEvents",
              "logs:PutLogEventsBatch",
              "logs:CreateLogStream"
            ],
            "Resource": "''' + ESCloudWatchLogGroup.get_output_attr('arn') + '''*"
          }
        ]
    }'''


class ESDomain(ElasticsearchDomainResource):
    domain_name = "data"
    elasticsearch_version = "5.5"
    instance_type = Settings.get('ES_INSTANCE_TYPE', "m4.large.elasticsearch")
    instance_count = 1
    dedicated_master_enabled = False
    zone_awareness_enabled = False
    ebs_enabled = True
    volume_type = "gp2"
    volume_size = 20
    automated_snapshot_start_hour = 23
    security_group_ids = [InfraSecurityGroupResource.get_output_attr('id')]
    subnet_ids = [Settings.get('VPC')['SUBNETS'][0]]
    cloudwatch_log_group_arn = ESCloudWatchLogGroup.get_output_attr('arn')
    log_type = "ES_APPLICATION_LOGS"

    @classmethod
    def get_http_url_with_port(cls):
        return f"{cls.get_http_url()}:80"

    @classmethod
    def get_http_url(cls):
        return f"http://{cls.get_output_attr('endpoint')}"

    @classmethod
    def get_es_port(cls):
        return 80

    def pre_terraform_apply(self):
        status, msg = create_iam_service_linked_role(
            Settings.AWS_ACCESS_KEY,
            Settings.AWS_SECRET_KEY,
            "es.amazonaws.com",
            Settings.RESOURCE_DESCRIPTION)

        SysLog().write_debug_log(
            f"ElasticSearch IAM Service Linked role creation: Status:{str(status)}, Message: {msg}"
        )

    def render_output(self, outputs):
        if self.resource_in_tf_output(outputs):
            resource_id = self.get_resource_id()
            return {
              'ES Host': outputs[resource_id]['endpoint'],
              'Kibana Host': outputs[resource_id]['kibana_endpoint']
            }


class ESDomainPolicy(ElasticsearchDomainPolicyResource):
    resource_id = "elasticsearch_domain_policy"
    domain_name = ESDomain.get_input_attr('domain_name')
    access_policies = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": [
              "*"
            ]
          },
          "Action": [
            "es:*"
          ],
          "Resource": ESDomain.get_output_attr('arn') + "/*"
        }
      ]
    }
