from __future__ import print_function
import subprocess

from .plugin_base import Plugin

MATCH_STRING = "Your code has been rated at "

class Pylint(Plugin):
    """Create a Pylint badge"""

    @staticmethod
    def add_arguments(parser):
        # Add plugin arguments below
        parser.add_argument("pylint_args",
            help="Arguments to use when running pylint "+
                 "(enclosed in \"quotes\" if necessary)")
        parser.add_argument("--pylint-patcher", action="store_true",
            help="Use the pylint-patcher tool in place of pylint")
        parser.add_argument("--green-threshold", default=9.0,
            help="Badge will be green above this threshold (default:9.0)")
        parser.add_argument("--red-threshold", default=5.0,
            help="Badge will be red below this threshold (default:5.0)")
        parser.add_argument("--quiet", action="store_true",
            help="Supress the Pylint output")

    def run(self):
        """Run the plugin, returning (subject, status, colour) of the badge"""
        if self.args.pylint_patcher:
            cmd = ["pylint-patcher"] + self.args.pylint_args.split(" ")
        else:
            cmd = ["pylint"] + self.args.pylint_args.split(" ")

        print(" ".join(cmd))

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        stdout, _ = proc.communicate()
        if not self.args.quiet:
            print(stdout)

        score = self.parse_score(stdout)
        colour = self.get_colour(score)
        return ("pylint", score, colour)

    @staticmethod
    def parse_score(pylint_output):
        """
        Given a string containing Pylint output, return the overall score
        (eg. "9.8/10")
        """
        for line in pylint_output.split("\n"):
            if line.startswith(MATCH_STRING):
                score = line[len(MATCH_STRING):]
                return score.split()[0]
        print("Could not parse Pylint score")
        return "unknown"

    def get_colour(self, score):
        """
        Given a string containing the Pylint score, use the
        red_threshold/green_threshold arguments to return a badge colour
        """
        try:
            score = float(score.split("/")[0])
        except Exception:
            print("Could not decode Pylint colour")
            return "red"
        if score < float(self.args.red_threshold):
            return "red"
        elif score > float(self.args.green_threshold):
            return "green"
        else:
            return "orange"
