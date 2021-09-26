import sys
import os

from textwrap import dedent

from traitlets import default
from traitlets.config import Application
from traitlets.config.application import catch_config_error

import dscreate
from .BaseApp import dscreate_aliases, dscreate_flags
from . import (
    DsCreate,
    CreateApp,
    GenerateApp,
    ShareApp
)
from traitlets.traitlets import MetaHasTraits
from typing import List

aliases = {}
aliases.update(dscreate_aliases)
aliases.update({
})

flags = {}
flags.update(dscreate_flags)
flags.update({
})


class DsCreateApp(DsCreate):

    name = u'ds'
    description = u'''
    The command line launch application for dscreate.

    This application parses the command line arguments via a traitlets ``Application`` object
    and uses the arguments to determine which sub application should be activated.
    '''
    version = '0.1.87'

    aliases = aliases
    flags = flags

    subcommands = dict(
        create=(
            CreateApp,
            dedent(
                """
                Split a notebook into student facing and instructor facing materials
                and generate readme markdown files for each split.
                """
            ).strip()
        ),
        generate=(
            GenerateApp,
            dedent(
                """
                Split an nbgrader assignment into student and teacher facing materials
                and generate readme markdown files for each split.
                """
            ).strip()
        ),
        share=(
            ShareApp,
            dedent(
                """
                Add a url to your clipboard that opens a github hosted jupyter notebook
                in illumidesk.
                """
            )
        )
    )


    @default("classes")
    def _classes_default(self) -> List[MetaHasTraits]:
        return self.all_configurable_classes()

    @catch_config_error
    def initialize(self, argv: List[str] = None) -> None:
        super(DsCreateApp, self).initialize(argv)

    def start(self) -> None:
        # check: is there a subapp given?
        if self.subapp is None:
            print("No command given (run with --help for options). List of subcommands:\n")
            self.print_subcommands()

        # This starts subapps
        super(DsCreateApp, self).start()

    def print_version(self):
        print("Python version {}".format(sys.version))
        print("dscreate version {}".format(dscreate.__version__))


def main():
    DsCreateApp.launch_instance()