import logging
import os
import sys
import googkit.lib.path
import googkit.lib.plugin
from googkit.lib.argument_parser import ArgumentParser
from googkit.lib.command_tree import CommandTree
from googkit.lib.config import Config
from googkit.lib.environment import Environment
from googkit.lib.error import GoogkitError


VERSION = '0.0.0'


def print_help(tree, commands=[]):
    right_commands = tree.right_commands(commands)
    if len(right_commands) == 0:
        print('Usage: googkit <command>')
    else:
        print('Usage: googkit {cmd} <command>'.format(cmd=' '.join(right_commands)))

    print('')
    print('Available commands:')

    available_commands = tree.available_commands(right_commands)
    for name in available_commands:
        print('    ' + name)


def print_version():
    print('googkit ' + VERSION)


def find_config(cwd):
    default_config = googkit.lib.path.default_config()
    user_config = googkit.lib.path.user_config()
    project_config = googkit.lib.path.project_config(cwd)
    config = Config()
    config.load(project_config, user_config, default_config)
    return config


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    tree = CommandTree()
    googkit.lib.plugin.load(tree)

    cwd = os.getcwd()

    parser = ArgumentParser()
    parser.parse(sys.argv)
    commands = parser.commands

    if len(commands) == 0 and parser.option('--version'):
        print_version()
        sys.exit()

    classes = tree.command_classes(commands)
    if classes is None:
        print_help(tree, commands)
        sys.exit()

    try:
        config = None
        for cls in classes:
            if config is None and cls.needs_config():
                os.chdir(googkit.lib.path.project_root(cwd))
                config = find_config(cwd)

            env = Environment(cwd, parser, tree, config)
            command = cls(env)
            command.run()
    except GoogkitError as e:
        logging.error('[Error] ' + str(e))
        sys.exit(1)
