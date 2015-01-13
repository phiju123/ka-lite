import glob
import os

from django.conf import settings

from .base import UpdatesTestCase
from kalite.topic_tools import get_content_cache, get_node_cache

class TestTopicAvailability(UpdatesTestCase):
    """
    Test that topics with exercises are available, others are not.
    """

    def setUp(self):
        super(TestTopicAvailability, self).setUp()
        self.n_content = len(glob.glob(os.path.join(settings.CONTENT_ROOT, "*.mp4")))

    def test_video_availability(self):
        ncontent_local = sum([node["languages"] for node in get_content_cache().values()])
        self.assertEqual(self.n_content, ncontent_local, "# videos actually on disk should match # videos in topic tree")

    def test_topic_availability(self):
        for topic in get_node_cache("Topic").values():
            if "Exercise" in topic["contains"]:
                self.assertTrue(topic["available"], "Make sure all topics containing exercises are shown as available.")
            if topic["children"] and len(topic["contains"]) == 1 and "Video" in topic["contains"]:
                any_on_disk = bool(sum([v["on_disk"] for v in topic["children"]]))
                self.assertEqual(topic["available"], any_on_disk, "Make sure topic availability matches video availability when only videos are available.")
