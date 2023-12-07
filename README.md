# Ansible-Gendoc

*Inspired by Felix Archambault's* [ansidoc](https://github.com/archf/ansidoc)
project.

An [example](example.md) generated with `ansible-gendoc`.

## Features

* Generate the documentation for a role located in a directory
* Can use a personal template `README.j2` present in folder `templates`

## Quickstart

If you have an existing README.md file in your role, backup it before !

### Run From docker

Clone this project and build the image :

```bash
git clone
export DOCKER_BUILDKIT=1
docker build . -t ansible-gendoc:0.1.0 -t ansible-gendoc:latest
docker run --user $(id -u):$(id -g) -it ansible-gendoc:latest help
```

### Install python package

Install the latest version `ansible-gendoc` with `pip` or `pipx`

```bash
pip install ansible-gendoc
```

### Usage

```bash
ansible-gendoc --help

 Usage: ansible-gendoc [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show the application's version and exit.         │
│ --install-completion            Install completion for the current shell.        │
│ --show-completion               Show completion for the current shell, to copy   │
│                                 it or customize the installation.                │
│ --help                          Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────╮
│ init     Copy templates README.j2 from packages in templates/role folder.        │
│ render   Build the Documentation                                                 │
╰──────────────────────────────────────────────────────────────────────────────────╯
```

#### Build your first documentation of a role

To build the documentation roles, you can run these commands :

* with package installed with pip
  `ansible-gendoc render`.
* with docker images
  `docker run --user $(id -u):$(id -g) -v <path_role>:/role -it ansible-gendoc:latest render`.

#### Use your personal template

To use a personal template, you need to `init` the template in the templates
folder of your role. If `ansible-gendoc` find an existing file
`templates/README.j2`, it will use it to render the README.md file.

* with package installed with pip
  `ansible-gendoc init`.
* with docker images
  `docker run --user $(id -u):$(id -g) -v <path_role>:/role -it ansible-gendoc:latest init`.

```bash
ls templates
README.j2
```

The template use [`jinja`](https://jinja.palletsprojects.com/) as templating
language.

Modify it, for example replace `html` or `Restructuredtext` or another language.
You can remove some variables too.

#### Documentation of vars template

The documentation of vars coming soon.
