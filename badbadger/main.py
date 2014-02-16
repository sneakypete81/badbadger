from __future__ import print_function
import sys
import argparse

from . import plugins
from . import badge
from . import github

def main(sysargs=sys.argv[1:]):
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="BadBadger creates custom GitHub badges")
    parser.add_argument("--ext", default="png",
        help="File extension of the badge image (default: png)")
    parser.add_argument("--filename",
        help="Filename for the badge image")
    parser.add_argument("--branch", default="badges",
        help="Git branch to push (default: badges)")
    parser.add_argument("--commit-message", default="Updated badge",
        help="Message to use for the Git commit (default: 'Updated badge')")
    parser.add_argument("--author", default="BadBadger <>",
        help="Author string to use for the Git commit (default: 'BadBadger <>'")
    parser.add_argument("--no-push", action="store_true",
        help="Don't push to GitHib, just save the badge to a local file")
    parser.add_argument("--debug", action="store_true",
        help="Print full debugging error messages " +
             "(WARNING: contains sensitive information)")

    # Create plugin subparsers
    subparsers = parser.add_subparsers(metavar="<command>", title="Commands",
                 description="Use \"%(prog)s <command> --help\" for more info")
    for plugin in plugins.ALL:
        plugin.add_subparser(subparsers)

    # Parse commandline arguments
    args = parser.parse_args(sysargs)
    if args.filename is None:
        args.filename = "badge-%s.%s" % (args.Plugin.__name__.lower(),
                                         args.ext)

    # Run the plugin
    plugin = args.Plugin(args)
    subject, status, colour = plugin.run()

    # Create the badge
    print("Creating badge %s:%s:%s" % (subject, status, colour))
    image = badge.open_badge(subject, status, colour, args.ext)

    # Publish to GitHub
    if args.no_push:
        # Just create the file in the current directory
        print("Saving badge to %s" % args.filename)
        open(args.filename, "wb").write(image.read())
    else:
        print("Publishing badge to GitHub")
        github.publish_badge(args, image)
