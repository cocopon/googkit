class Environment(object):
    def __init__(self, cwd, arg_parser, tree, config):
        self.cwd = cwd
        self.arg_parser = arg_parser
        self.tree = tree
        self.config = config
