from .plugin_base import Plugin

class Custom(Plugin):
    """Create a fully customised badge"""

    @staticmethod
    def add_arguments(parser):
        """Add argparse arguments for the plugin"""
        # Add plugin arguments below
        parser.add_argument("--subject", default="[subject]",
                    help="Subject text for the badge (default: [subject])")
        parser.add_argument("--status", default="[status]",
                    help="Status text for the badge (default: [status])")
        parser.add_argument("--colour", default="red",
                    help="Colour of the badge (default: [red])")

    def run(self):
        """Run the plugin, returning (subject, status, colour) of the badge"""
        return (self.args.subject, self.args.status, self.args.colour)
