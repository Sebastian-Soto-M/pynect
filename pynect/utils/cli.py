import argparse
from attrs import field, define
from functools import partialmethod
from typing import Any, Dict, Optional


@define
class CLIArgument:
    detail: str
    help: str
    flag: Optional[str] = field(default=None)
    choices: Optional[set[str]] = field(default=None)


class CLI:
    """
    CLI class that handles the arguments groups, parsers and values based
    on the argparse library.
    """

    def __init__(self, name: str):
        self.__groups: Dict[str, argparse._ArgumentGroup] = dict()
        self.__parser = argparse.ArgumentParser(prog=name)
        self.__values: argparse.Namespace = None

    def add_group(self, name: str):
        self.__groups[name] = self.__parser.add_argument_group(
            name.capitalize())

    def add_argument(
        self, arg: CLIArgument, group: Optional[str] = None,
            default: Optional[Any] = None, action: Optional[str] = None,
            required: bool = False
    ):
        """
        Adds a new argument to the specified group or parser if no group is
        specified.

        Args:
            arg (CLIArgument): A CLIArgument object
            group (Optional[str], optional): The group where the argument will
                be stored or None. [None]

            default (Optional[Any], optional): Default value for the argument.
                [None]

            action (Optional[str], optional): If actions from argsparse
                library are needed. [None]

            required (bool, optional): If the argument is required or not.
                [False]
        """
        opts = {
            'help': arg.help,
            'default': default,
            'action': action,
            'required': required,
        }
        if action != 'store_true':
            opts['choices'] = arg.choices
        arg_parser = self.__parser if group is None else self.__groups[group]
        if arg.flag is not None:
            arg_parser.add_argument(
                f'-{arg.flag}',
                f'--{arg.detail}',
                **opts
            )
        else:
            arg_parser.add_argument(
                f'--{arg.detail}',
                **opts
            )

    add_flag = partialmethod(add_argument, action='store_true')

    def __call__(self) -> argparse.Namespace:
        return self.__parser.parse_args() if self.__values else self.__values
