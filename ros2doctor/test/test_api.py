# Copyright 2020 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from launch import LaunchDescription
from launch.actions import ExecuteProcess

import launch_testing.actions
import launch_testing.markers

import pytest

from ros2doctor.api import Report
from ros2doctor.api.topic import TopicCheck
from ros2doctor.api.topic import TopicReport


@pytest.mark.rostest
@launch_testing.markers.keep_alive
def generate_test_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'daemon', 'stop'],
            name='daemon-stop',
            on_exit=[
                ExecuteProcess(
                    cmd=['ros2', 'daemon', 'start'],
                    name='daemon-start',
                    on_exit=[
                        launch_testing.actions.ReadyToTest()
                    ]
                )
            ]
        )
    ])


def _generate_expected_report(topic, pub_count, sub_count):
    expected_report = Report('TOPIC LIST')
    expected_report.add_to_report('topic', topic)
    expected_report.add_to_report('publisher count', pub_count)
    expected_report.add_to_report('subscriber count', sub_count)
    return expected_report


class TestROS2DoctorAPI(unittest.TestCase):

    def test_topic_check(self):
        """Assume no topics are publishing or subscribing other than whitelisted ones."""
        topic_check = TopicCheck()
        check_result = topic_check.check()
        self.assertEqual(check_result.error, 0)
        self.assertEqual(check_result.warning, 0)

    def test_topic_report(self):
        """Assume no topics are publishing or subscribing other than whitelisted ones."""
        report = TopicReport().report()
        expected_report = _generate_expected_report('none', 0, 0)
        self.assertEqual(report.name, expected_report.name)
        self.assertEqual(report.items, expected_report.items)
