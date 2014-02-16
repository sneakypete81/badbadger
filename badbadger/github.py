from __future__ import print_function
import os
import tempfile
import shutil
import git

class GitException(Exception):
    """Generic Git exception"""
    pass

def publish_badge(args, image):
    """Publish the supplied badge image to GitHub"""
    if "GH_TOKEN" not in os.environ:
        raise ValueError(
              "Please set $GH_TOKEN to a GitHub personal access token.")
    if "GH_REPO_SLUG" not in os.environ:
        raise ValueError(
              "Please set $GH_REPO_SLUG (eg: github.com/user/repo.git)")

    tempdir = tempfile.mkdtemp()
    try:
        # Clone into a temporary location
        url = "https://%s@%s" % (os.environ["GH_TOKEN"],
                                 os.environ["GH_REPO_SLUG"])
        repo = git.Repo.clone_from(url, tempdir)

        # Switch branches, creating a new one if necessary
        try:
            repo.git.checkout("origin/%s" % args.branch, track=True)
        except git.exc.GitCommandError:
            # Create an empty orphan branch, since we don't want past history
            repo.git.checkout(args.branch, orphan=True)
            repo.git.reset()

        # Add the badge image
        filepath = os.path.join(tempdir, args.filename)
        file(filepath, "wb").write(image.read())

        # Git add
        repo.git.add([filepath])
        if repo.head.is_valid() and not repo.is_dirty():
            print("Badge is unchanged")
            return

        # Git commit
        repo.git.commit(m=args.commit_message, author=args.author)

        # Git push
        repo.remotes.origin.push(args.branch)

    except Exception:
        if args.debug:
            raise
        else: # Hide the error, in case it contains sensitive information
            raise GitException("Git command failed, use --debug for more info")

    finally:
        shutil.rmtree(tempdir, ignore_errors=True)
