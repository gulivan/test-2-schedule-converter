import unittest
from schedule_converter import *


class TestScheduleConverter(unittest.TestCase):
    def test_parse_timestamp(self):
        # test that input timestamp is parsed correctly
        # given example of 1 day, 1 hour, 1 minute and 10 seconds
        self.assertEqual(tuple(parse_timestamp(86400 + 3600 + 60 + 10)), (1, 1, 1, 10))
        # 0 day, 2 hours, 3 minutes and 30 seconds
        self.assertEqual(tuple(parse_timestamp(7200 + 180 + 30)), (0, 2, 3, 30))

    def test_define_schedule_ranges(self):
        # test output tuples of pairs of time-ranges
        test_case_1 = {
            "monday": [
                {"type": "open", "value": 1800},
                {"type": "close", "value": 3600},
                {"type": "open", "value": 72000},
                {"type": "close", "value": 86399},
            ],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": [],
        }
        self.assertEqual(len(define_schedule_ranges(test_case_1)), 2)

    def test_schedule_rotation(self):
        # test case when the first event at monday is 'close'
        test_case_2 = {
            "monday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 72000},
                {"type": "close", "value": 86399},
            ],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": [
                {"type": "open", "value": 86340}
            ],
        }
        # the very first value must be the first 'open' event
        # at this case it must be 72000
        self.assertEqual(define_schedule_ranges(test_case_2)[0][0], 72000)
        # and the very first 'close' event must be the last
        self.assertEqual(define_schedule_ranges(test_case_2)[-1][-1], 3600)

    def test_form_week_schedule(self):
        test_case_3 = {
            "monday": [
                {"type": "open", "value": 72000},
            ],
            "tuesday": [
                {"type": "close", "value": 3600}
            ],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": [
                {"type": "open", "value": 0},
                {"type": "close", "value": 7200}
            ],
        }
        schedule_ranges = define_schedule_ranges(test_case_3)
        week_schedule = form_week_schedule(schedule_ranges)
        # time ranges distributes correctly
        self.assertEqual(week_schedule["monday"][0], "8 PM — 1 AM")
        self.assertEqual(week_schedule["sunday"][0], "12 AM — 2 AM")

        # and there is no schedule from tuesday to saturday
        days_to_check = ["tuesday", "wednesday", "thursday", "friday", "saturday"]
        for day_to_check in days_to_check:
            self.assertFalse(week_schedule[day_to_check])

    def test_forming_schedule(self):
        test_case_4 = {
            "monday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 36000},
                {"type": "close", "value": 72000},
            ],
            "tuesday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 64800},
            ],
            "wednesday": [],
            "thursday": [
                {"type": "open", "value": 37800},
                {"type": "close", "value": 64800},
                {"type": "open", "value": 68400},
                {"type": "close", "value": 72000},
                {"type": "open", "value": 73800},
                {"type": "close", "value": 75600},
            ],
            "friday": [
                {"type": "open", "value": 36000}
            ],
            "saturday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 36000},
            ],
            "sunday": [
                {"type": "close", "value": 3600},
                {"type": "open", "value": 43200},
                {"type": "close", "value": 75600},
                {"type": "open", "value": 86340},
            ],
        }
        schedule_ranges = define_schedule_ranges(test_case_4)
        week_schedule = form_week_schedule(schedule_ranges)
        result = format_week_schedule(week_schedule).split("\n")
        expected_result = """\
Monday: 10 AM — 8 PM
Tuesday: 10 AM — 6 PM
Wednesday: Closed
Thursday: 10:30 AM — 6 PM, 7 PM — 8 PM, 8:30 PM — 9 PM
Friday: 10 AM — 1 AM
Saturday: 10 AM — 1 AM
Sunday: 12 PM — 9 PM, 11:59 PM — 1 AM
""".split(
            "\n"
        )
        self.assertEqual(len(result), 7)
        for schedule_predefined, schedule_calculated in zip(expected_result, result):
            self.assertEqual(schedule_predefined, schedule_calculated)
