import sys
from pathlib import Path
from typing import Final

PROJECT_PATH: Final = str(Path(__file__).parent.parent.parent)
sys.path.append(PROJECT_PATH)

import unittest  # NOQA
from src import utils  # NOQA


class TestGeneralUtils(unittest.TestCase):

    def setUp(self):
        self.downloads_string_dir = "/home/eastern-skill7173/Downloads"
        self.downloads_path_obj = Path(self.downloads_string_dir)
        self.number_list = [0, 1, 2, 3, 4, 5]

    def test_convert_file_path_to_string(self):
        self.assertEqual(
            utils.convert_file_path_to_string(self.downloads_path_obj),
            self.downloads_string_dir
        )

    def test_convert_string_to_file_path(self):
        self.assertEqual(
            utils.convert_string_to_file_path(self.downloads_string_dir),
            self.downloads_path_obj
        )

    def test_is_plural(self):
        self.assertTrue(utils.is_plural(2))
        self.assertFalse(utils.is_plural(1))
        self.assertTrue(utils.is_plural(0))
        self.assertFalse(utils.is_plural(-1))
        self.assertFalse(utils.is_plural(-2))

    def test_move_index(self):
        copied_number_list = self.number_list.copy()
        utils.move_index(copied_number_list, 0, 5)
        self.assertListEqual(copied_number_list, [1, 2, 3, 4, 5, 0])

    def test_replace_index(self):
        copied_number_list = self.number_list.copy()
        utils.replace_index(copied_number_list, 5, 6)
        self.assertListEqual(copied_number_list, [0, 1, 2, 3, 4, 6])

    def test_matched_prefix(self):
        string = "Florida"
        prefixes = ("Alaska", "Flow",  "Floor", "Flo", "Florida")
        self.assertEqual(utils.matched_prefix(string, prefixes), "Flo")

    def test_matched_prefix_dict(self):
        pass

    def test_human_readable_size(self):
        one_kilobyte = 10 ** 3
        one_megabyte = 10 ** 6
        one_gigabyte = 10 ** 9
        self.assertEqual(
            utils.human_readable_size(one_kilobyte),
            "1 KB"
        )
        self.assertEqual(
            utils.human_readable_size(one_megabyte),
            "1 MB"
        )
        self.assertEqual(
            utils.human_readable_size(one_gigabyte),
            "1 GB"
        )

    def test_human_readable_duration(self):
        one_second = 1
        one_minute = 60 * one_second
        one_hour = 60 * one_minute
        self.assertEqual(
            utils.human_readable_duration(one_second),
            "0:01"
        )
        self.assertEqual(
            utils.human_readable_duration(one_minute),
            "1:00"
        )
        self.assertEqual(
            utils.human_readable_duration(one_hour),
            "1:00:00"
        )


if __name__ == "__main__":
    unittest.main()
