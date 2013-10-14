import distutils.core
import os
import googkit.lib.path
from googkit.commands.command import Command
from googkit.lib.error import GoogkitError


class InitCommand(Command):
    def __init__(self, env):
        super(InitCommand, self).__init__(env)

    def copy_template(self, dst_dir):
        template_dir = googkit.lib.path.template()

        conflicted = set(os.listdir(dst_dir)) & set(os.listdir(template_dir))
        if conflicted:
            raise GoogkitError('Conflicted files: ' + ', '.join(conflicted))

        distutils.dir_util.copy_tree(template_dir, dst_dir)

    def run_internal(self):
        self.copy_template(os.getcwd())