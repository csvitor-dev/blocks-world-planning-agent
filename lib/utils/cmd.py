import sys
from typing import Any
from lib.constants.regex import UNIQUE_VALUE_CONSTRAINT


def pluck_flags_from_cmd_args(search_for: list[str]) -> dict[str, Any]:
    args = __map_args(sys.argv[1:])
    return {target: args[target] for target in search_for if target in args}


def __map_args(raw_args: list[str]) -> dict[str, Any]:
    filtering = filter(lambda arg: arg.isdigit()
                       is False and '=' in arg, raw_args)
    mapping = list(map(lambda arg: arg.replace(
        '--', '').split('='), filtering))

    return {flag: value if flag != 'instance' else __to_list(value) for (flag, value) in mapping}


def __to_list(arg: str) -> list[str]:
    if UNIQUE_VALUE_CONSTRAINT.search(arg) is not None:
        return [arg]
    return arg[1:len(arg)-1].split(',')
