import sys
from lib.constants.regex import UNIQUE_VALUE_CONSTRAINT

def pluck_instance_from_cmd_args() -> str:
    args = __map_args(sys.argv[1:])

    if len(args.keys()) > 1:
        raise NotImplementedError('Resources not supported.')
    return args.get('instance', '4-0')

def __map_args(raw_args: list[str]) -> dict[str, str]:
    filtering = filter(lambda arg: arg.isdigit() is False and '=' in arg, raw_args)
    mapping = list(map(lambda arg: arg.replace('--', '').split('='), filtering))

    return {flag: __to_list(value) for (flag, value) in mapping}

def __to_list(arg: str) -> str:
    if UNIQUE_VALUE_CONSTRAINT.search(arg) is not None:
        return arg
    raise ValueError('More than one value was provided.')
