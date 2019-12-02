from django.test import TestCase
from app.utils import get_ordered_data, get_count_per_month

# Create your tests here.


class UtilsTest(TestCase):
    def setUp(self):
        self.test_dict = {3: 5, 4: 6, 5: 2, 10: 1}
        self.test_tuples = [(2019, 10, 6), (2019, 10, 4),
                            (2019, 9, 9), (2018, 10, 10)]

    def test_ordered_data(self):
        vid_count = get_ordered_data(self.test_dict)
        expected_result = [0, 0, 5, 6, 2, 0, 0, 0, 0, 1, 0, 0]
        self.assertListEqual(vid_count, expected_result)

    def test_count_per_month(self):
        count_per_month = get_count_per_month(self.test_tuples)
        expected_result = {2019: [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0], 2018: [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]}
        self.assertDictEqual(count_per_month, expected_result)
