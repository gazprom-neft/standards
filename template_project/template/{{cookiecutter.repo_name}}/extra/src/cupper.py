# -*- coding: utf-8 -*-
"""
script from https://github.com/senseyeio/cupper,
as a stand-alone script with minor changes

MIT License

Copyright (c) 2018 Senseye

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import json
import shutil
import subprocess
import json
from cookiecutter.main import cookiecutter


class TemporaryWorkdir():
    """Context Manager for a temporary working directory of a branch in a git repo"""

    def __init__(self, path, repo, branch='master'):
        self.repo = repo
        self.path = path
        self.branch = branch

    def __enter__(self):
        if not os.path.exists(os.path.join(self.repo, ".git")):
            raise Exception("Not a git repository: %s" % self.repo)

        if os.path.exists(self.path):
            raise Exception("Temporary directory already exists: %s" % self.path)

        os.makedirs(self.path)
        subprocess.run(["git", "worktree",  "add", "--no-checkout", self.path, self.branch],
                       cwd=self.repo)

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.path)
        subprocess.run(["git", "worktree", "prune"], cwd=self.repo)


def update_template(context, root, branch):
    """Update template branch from a template url"""
    template_url = context['_template']
    tmpdir       = os.path.join(root, ".git", "cookiecutter")
    project_slug = os.path.basename(root)
    tmp_workdir  = os.path.join(tmpdir, project_slug)

    context['project_slug'] = project_slug
    # create a template branch if necessary
    if subprocess.run(["git", "rev-parse", "-q", "--verify", branch], cwd=root).returncode != 0:
        firstref = subprocess.run(["git", "rev-list", "--max-parents=0", "--max-count=1", "HEAD"],
                                  cwd=root,
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True).stdout.strip()
        subprocess.run(["git", "branch", branch, firstref])

    with TemporaryWorkdir(tmp_workdir, repo=root, branch=branch):
        # update the template
        cookiecutter(template_url,
                     no_input=True,
                     extra_context=context,
                     overwrite_if_exists=True,
                     output_dir=tmpdir)

        # commit to template branch
        subprocess.run(["git", "add", "-A", "."], cwd=tmp_workdir)
        subprocess.run(["git", "commit", "-m", "Update template"],
                       cwd=tmp_workdir)

def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: cupper <context filename> <branch>")
        sys.exit(1)
    context_file, branch = sys.argv[1], sys.argv[2]
    with open(context_file, 'r') as fd:
        context = json.load(fd)

    update_template(context, os.getcwd(), branch=branch)

if __name__ == "__main__":
    main()
