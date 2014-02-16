class Plugin(object):
    """Plugin base class"""

    def __init__(self, args):
        self.args = args

    @classmethod
    def add_subparser(cls, subparsers):
        """Add a subparser for the plugin"""
        parser = subparsers.add_parser(cls.__name__.lower(),
                                       help=cls.__doc__,
                                       description=cls.__doc__)
        parser.set_defaults(Plugin=cls)
        cls.add_arguments(parser)

    @staticmethod
    def add_arguments(parser):
        """Add argparse arguments for the plugin"""
        raise NotImplementedError

    def run(self):
        """Run the plugin, returning (subject, status, colour) of the badge"""
        raise NotImplementedError
