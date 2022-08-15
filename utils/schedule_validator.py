from typing import Dict
from utils.common import read_json, configure_parser


class ValidationError(Exception):
    pass


def check_schedule_events_is_even(schedule: Dict):
    """
    Check if the number of events is even
    """
    accum = []
    for day in schedule:
        accum.extend(schedule[day])
    if not len(accum) % 2 == 0:
        raise ValidationError(
            f"The number of events is not even. Current length: {len(accum)}"
        )
    return True


def check_schedule_events_types_rotates(schedule: Dict):
    """
    Check if the types of events rotate between close and open
    """
    current_event = None
    for day, schedule_events in schedule.items():
        for event in schedule_events:
            if current_event is None:
                current_event = event["type"]
            elif event["type"] == current_event:
                raise ValidationError(
                    f"The types of events are not rotating at {day} {event['value']}"
                )
            else:
                current_event = event["type"]
    return True


def check_schedule_events_value_is_ascending(schedule: Dict):
    """
    Check if the timestamps of events are sorted in ascending order
    """
    for day, schedule_events in schedule.items():
        curr_value = 0
        for event in schedule_events:
            if event["value"] >= curr_value:
                curr_value = event["value"]
            else:
                raise ValidationError(
                    f"The values of events are not ascending at {day} {event['value']}"
                )
    return True


def validate_schedule(filename: str, verbose: bool = False):
    input_schedule = read_json(filename)
    check_schedule_events_is_even(input_schedule)
    check_schedule_events_types_rotates(input_schedule)
    check_schedule_events_value_is_ascending(input_schedule)
    if verbose:
        print(f"The schedule file {filename} is valid")


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    filename = args.file
    validate_schedule(filename=filename, verbose=args.verbose)
