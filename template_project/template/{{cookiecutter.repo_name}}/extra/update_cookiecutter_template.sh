#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
echo "$BASEDIR"
python $BASEDIR/src/cupper.py $BASEDIR/.cookiecutter.json template
git merge template --no-commit --no-ff
echo "Recent changes from template have been merged into current branch"
echo "Review them, resolve conflicts if needed"
echo "REVIEW SUBMODULES CAREFULLY!!!"
