# spid-django
SPID authentication for Django

## How to develop

### Useful tool

#### pyenv

If you want to isolate your development and manage with different versions of python then [pyenv](https://github.com/pyenv/pyenv) is a great tool to create your virtual environment.

Follow this [link](https://github.com/pyenv/pyenv-installer#pyenv-installer) to install the tool in your preferred operative system. MacOS, Linux and Windows are supported.

#### cookiecutter

A [cookiecutter](https://cookiecutter-django.readthedocs.io/en/latest/) template for Django will be used to bootstrap the package for Spid.

``bash
cookiecutter https://github.com/pydanny/cookiecutter-djangopackage.git
``bash

### Create a virtual environment

#### pyenv

``bash
pyenv virtualenv 2.7.13 spid
``

Enter into the new virtual environment

``bash
pyenv activate spid
``

#### virtualenv

TODO
