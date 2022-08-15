from typing import Dict
import json
from argparse import ArgumentParser


def configure_parser() -> ArgumentParser:
    """
    Configures parser from sys.argv
    :return: ArgumentParser
    """
    _parser = ArgumentParser()
    _parser.add_argument(
        "--file", type=str, required=True, help="Input json file with a schedule"
    )
    _parser.add_argument(
        "--verbose", type=str, required=False, help="Verbose output", default=False
    )
    return _parser


def read_json(file_name: str) -> Dict:
    """
    Reads json file and returns a dict
    :param file_name: str
    :return: Dict
    """
    with open(file_name, "r", encoding="utf-8") as fp:
        return json.load(fp)
