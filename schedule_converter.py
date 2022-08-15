"""Converts input json weekly schedule to the human readable schedule format"""
from datetime import datetime
from typing import Dict, List, Tuple, NamedTuple
from itertools import islice
from collections import deque, namedtuple
from utils.common import read_json, configure_parser
from utils.schedule_validator import validate_schedule

DAY_NAMES = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def define_schedule_ranges(
    schedule: Dict[str, List[Dict[str, int]]]
) -> List[Tuple[int]]:
    """
    Defines schedule ranges from the input schedule and returns pair of open and close times
    :param schedule: Dict
    :return: List
    """
    schedule_ranges = deque()
    first_event_type = None
    for day, schedule_events in schedule.items():
        if schedule_events:  # if schedule events is not empty
            for event in schedule_events:
                if not first_event_type:
                    first_event_type = event["type"]
                adjusted_timestamp = event["value"] + (86400 * DAY_NAMES.index(day))
                schedule_ranges.append(adjusted_timestamp)

    # if the type of the first event == 'close' then we should move
    # first element to the end of the list
    if first_event_type == "close":
        schedule_ranges.rotate(-1)

    # making a list of time-schedules in timestamp format
    schedule_ranges = list(
        zip(islice(schedule_ranges, None, None, 2), islice(schedule_ranges, 1, None, 2))
    )
    return schedule_ranges


def parse_timestamp(timestamp: int) -> NamedTuple:
    """
    Parses timestamp and returns a named tuple with days, hours, minutes and seconds as elements
    :param timestamp: int
    :return: NamedTuple(days, hours, minutes, seconds)
    """
    _tuple = namedtuple("time", "day hours minutes seconds")
    days, seconds = divmod(timestamp, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    result = _tuple(days, hours, minutes, seconds)
    return result


def time_tuple_to_12h(time_tuple: NamedTuple) -> str:
    """
    Converts time tuple to 12h format
    :param time_tuple: NamedTuple(days, hours, minutes, seconds)
    :return: str
    """
    time_format = "%-I"
    if time_tuple.minutes:
        time_format += ":%-M"
    if time_tuple.seconds:
        time_format += ":%-S"
    time_format += " %p"
    time_str = f"{time_tuple.hours}:{time_tuple.minutes}:{time_tuple.seconds}"
    time_12h = datetime.strptime(time_str, "%H:%M:%S").strftime(time_format)
    return time_12h


def form_week_schedule(schedule_ranges: List[Tuple[int]]) -> Dict[str, List[str]]:
    """
    Converts schedule ranges to a week schedule and returns is as a Dict of weekdays and time ranges
    :param schedule_ranges:
    :return: Dict
    """
    week_schedule = {day: [] for day in DAY_NAMES}

    for schedule_pair in schedule_ranges:
        open_time = parse_timestamp(schedule_pair[0])
        close_time = parse_timestamp(schedule_pair[1])

        # even if the closing time is at tomorrow we should still bind it to the day it is opened
        # the following line gets the day name
        day = DAY_NAMES[open_time.day]
        open_time_str = time_tuple_to_12h(open_time)
        close_time_str = time_tuple_to_12h(close_time)
        week_schedule[day].append(f"{open_time_str} — {close_time_str}")
    return week_schedule


def format_week_schedule(week_schedule: Dict[str, List[str]]) -> str:
    """
    Formats week schedule to a string
    :param week_schedule:
    :return:
    """
    output = ""
    for day, time_ranges in week_schedule.items():
        if time_ranges:
            output += f"{day.capitalize()}: {', '.join(time_ranges)}\n"
        else:
            output += f"{day.capitalize()}: Closed\n"
    return output.rstrip("\n")


def main(schedule: Dict[str, List[Dict[str, int]]]):
    """
    :param schedule:
    :return:
    """
    schedule_ranges = define_schedule_ranges(schedule)
    week_schedule = form_week_schedule(schedule_ranges)
    result = format_week_schedule(week_schedule)
    return result


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    validate_schedule(filename=args.file, verbose=args.verbose)
    print(args)
    input_schedule = read_json(args.file)
    print(main(input_schedule))
