import os
from mock import patch, Mock, ANY, call
import nose.tools as nt
import datetime
from dateutil.tz import tzlocal

import aws
import boto3
import ecs_taskbalancer


class TestTaskBalancer(object):


    def setup(self):
        self.region = "eu-west-1"
        self.cluster = "test"
        self.sleep_time = 1
        self.drain_timeout = 1
        self.drain_max_instances = 2
        self.max_retries = 3
        self.cov_percent = 20

    @patch('aws.update_container_instance_draining')
    @patch('aws.get_container_instances')
    def test_cluster_is_rebalanced_when_distribution_is_uneven(self, get_instances_mock, drain_mock):
        test_dataset = [11, 8, 5, 11, 4]
        test_dataset_2 = [10, 9, 5, 8, 7]
        get_instances_mock.side_effect = [[
            {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }], [{
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset_2[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset_2[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset_2[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset_2[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset_2[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }],
            [
            {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }], [{
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset_2[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset_2[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset_2[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset_2[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset_2[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }],
            [
            {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }], [{
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset_2[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset_2[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset_2[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset_2[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset_2[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }], 
            [{
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset_2[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset_2[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset_2[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset_2[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset_2[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }]]

        get_instances_mock.return_value = [
            {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }
        ]

        drain_mock.return_value = [
            {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset_2[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset_2[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset_2[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset_2[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset_2[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }
        ]


        
        ecs_taskbalancer.try_rebalancing_cluster(
            self.region, self.cluster, self.sleep_time, self.drain_timeout,
            self.drain_max_instances, self.max_retries, self.cov_percent
        )
        # Assert that the call was first made to drain the instance
        # and then to activate the instance back so that
        # rebalancing can occur.
        drain_mock.assert_has_calls(
            [
                call(self.region, self.cluster, ANY, status=aws.STATUS_DRAINING),
                call(self.region, self.cluster, ANY, status=aws.STATUS_ACTIVE)
            ]
        )

    @patch('aws.update_container_instance_draining')
    @patch('aws.get_container_instances')
    def test_cluster_is_not_rebalanced_when_distribution_is_even(self, get_instances_mock, drain_mock):
        test_dataset = [10, 9, 5, 8, 8]
        get_instances_mock.return_value = [
            {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }
        ]
        ecs_taskbalancer.try_rebalancing_cluster(
            self.region, self.cluster, self.sleep_time, self.drain_timeout,
            self.drain_max_instances, self.max_retries, self.cov_percent
        )

        # A call to get the distribution
        get_instances_mock.assert_called_once_with(self.region, cluster_name=self.cluster, status=aws.STATUS_ACTIVE)

        # Because the distribution is good, rebalancing should not occur
        drain_mock.assert_not_called()

    @patch('aws.update_container_instance_draining')
    @patch('aws.get_container_instances')
    def test_cluster_is_not_rebalanced_for_zero_or_single_tasks(self, get_instances_mock, drain_mock):
        for test_dataset in [[0, 0, 0, 0 ,0 ], [1, 0, 0, 1, 1]]:
            get_instances_mock.return_value = [
                {
                "ec2InstanceId": "i-aaaaa",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/xxx",
                "runningTasksCount": test_dataset[0],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-bbbbb",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/yyy",
                "runningTasksCount": test_dataset[1],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1a'}]
            },
            {
                "ec2InstanceId": "i-ccccc",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/zzz",
                "runningTasksCount": test_dataset[2],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1b'}]
            },
            {
                "ec2InstanceId": "i-ddddd",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/hhh",
                "runningTasksCount": test_dataset[3],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            },
            {
                "ec2InstanceId": "i-eeeee",
                "containerInstanceArn": "arn:aws:ecs:eu-west-1:000:container-instance/ggg",
                "runningTasksCount": test_dataset[4],
                "pendingTasksCount": 0,
                "attributes": [{'name': 'ecs.availability-zone', 'value': 'us-east-1d'}]
            }
            ]
            ecs_taskbalancer.try_rebalancing_cluster(
                self.region, self.cluster, self.sleep_time, self.drain_timeout,
                self.drain_max_instances, self.max_retries, self.cov_percent
            )

        # A call to get the distribution
        get_instances_mock.assert_has_calls(
            [
                call(self.region, cluster_name=self.cluster, status=aws.STATUS_ACTIVE),
                call(self.region, cluster_name=self.cluster, status=aws.STATUS_ACTIVE)
            ]
        )

        # No rebalancing required, so no  calls to drain the instance
        drain_mock.assert_not_called()
