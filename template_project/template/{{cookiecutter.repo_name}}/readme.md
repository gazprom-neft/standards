# Welcome to {{cookiecutter.project_name}}!

Add your project description here


### Project structure

```
{% if cookiecutter.include_library != 'no' %}
├── {{ cookiecutter.include_library }}         <- {{ cookiecutter.include_library }} as a git submodule {% endif %}
├── datasets                  <- Keep your datasets here
├── docker_containers
├── .dockerignore
├── extra                     <- extra helper utilities that are not project-specific, ex. cookiecutter template updater
│   ├── .cookiecutter.json
│   ├── src
│   └── update_cookiecutter_template.sh   <- run this script to merge recent changes in cookiecutter template into your project
├── .git
├── .gitattributes
├── .github
│   └── workflows
│       └── status.yml
├── .gitignore
├── notebooks                 <- Development notebooks
├── overview                  <- Notebooks with overview of main results
├── pylintrc
├── readme.md                 <- The top-level README for developers using this project.
├── requirements.txt
├── src                       <- Project-specific models and utilities
└── tests

```
