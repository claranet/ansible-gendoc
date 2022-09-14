# ansible-role-sshd

[![Maintainer](https://img.shields.io/badge/maintained%20by-claranet-e00000?style=flat-square)](https://www.claranet.fr/)
[![License](https://img.shields.io/github/license/claranet/ansible-role-sshd?style=flat-square)](https://github.com/claranet/ansible-role-sshd/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/claranet/ansible-role-sshd?style=flat-square)](https://github.com/claranet/ansible-role-sshd/releases)
[![Status](https://img.shields.io/github/workflow/status/claranet/ansible-role-sshd/Ansible%20Molecule?style=flat-square&label=tests)](https://github.com/claranet/ansible-role-sshd/actions?query=workflow%3A%22Ansible+Molecule%22)
[![Ansible Galaxy](https://img.shields.io/badge/ansible-galaxy-black.svg?style=flat-square&logo=ansible)](https://galaxy.ansible.com/claranet/test)[![Ansible version](https://img.shields.io/badge/ansible-%3E%3D2.10-black.svg?style=flat-square&logo=ansible)](https://github.com/ansible/ansible)

⭐ Star us on GitHub — it motivates us a lot!

Install and configure SSHd. Manages Certificate Authority

**Platforms Supported**:

| Platform | Versions   |
|----------|------------|
| EL | all |
| Amazon | all |
| Debian | all |
| Ubuntu | all |

## ⚠️ Requirements

Ansible >= 2.1.

### Ansible role dependencies

None.

## ⚡ Installation

### Install with Ansible Galaxy

```shell
ansible-galaxy install ansible-role-sshd
```
### Install with git

If you do not want a global installation, clone it into your `roles_path`.

```bash
git clone claranet/ansible-role-sshd.git  ansible-role-sshd
```

But I often add it as a submodule in a given `playbook_dir` repository.

```bash
git submodule add claranet/ansible-role-sshd.git roles/ansible-role-sshd
```

As the role is not managed by Ansible Galaxy, you do not have to specify the
github user account.

### ✏️ Example Playbook

Basic usage is:

```yaml
- hosts: all
  roles:
    - role: ansible-role-sshd
```

## ⚙️ Role Variables

Variables are divided in three types.

The **default vars** section shows you which variables you may
override in your ansible inventory. As a matter of fact, all variables should
be defined there for explicitness, ease of documentation as well as overall
role manageability.

The **context variables** are shown in section below hint you
on how runtime context may affects role execution.

### Default variables


### Context variables

Those variables from `vars/*.{yml,json}` are loaded dynamically during task
runtime using the `include_vars` module.

Variables loaded from `vars/redhat-family.yml`.

| Variable Name | Value |
|---------------|-------|
| _sshd_service_name | sshd |

Variables loaded from `vars/amazon.yml`.

| Variable Name | Value |
|---------------|-------|
| _sshd_service_name | sshd |

Variables loaded from `vars/main.yml`.

| Variable Name | Value |
|---------------|-------|
| ansible_distro | {{ ansible_distribution \|lower \|replace('"', '') }} |
| ansible_distro_version | {{ ansible_distribution_version \|lower \|replace('/', '_') }} |
| ansible_distro_release | {{ ansible_distribution_release \|lower }} |
| ansible_distro_major_version | {{ ansible_distribution_major_version \|lower \|replace('/', '_') }} |
| _sshd_principals | {{ sshd_principals_default  \| combine(sshd_principals, recursive=True, list_merge=sshd_principals_list_merge) }} |
| _sshd_config | {{ sshd_config_default  \| combine(sshd_config, recursive=True, list_merge=sshd_config_list_merge) }} |
| _sshd_banner_file_path | /etc/banner |
| _sshd_banner_state | {{ 'present' if ssh_banner_template else 'absent' }} |
| _sshd_banner_lookup_method | {{ 'url' if sshd_banner_template is match('http(s)?://') else 'template' }} |
| _sshd_banner_template_content | {{ lookup(_sshd_banner_lookup_method, sshd_banner_template, split_lines=False, username=sshd_banner_template_username, password=sshd_banner_template_password) }} |
| _sshd_config_file_path | /etc/ssh/sshd_config |

Variables loaded from `vars/debian-family.yml`.

| Variable Name | Value |
|---------------|-------|
| _sshd_service_name | ssh |


## Introduction
In this document, a list of relevant settings for hardening sshd.
This document is non-exhaustive, however, it provides a solid base of security hardening 
measures.

As default, we do not authorize the password authentication. And we have enabled pubkey authentication option.

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the role, this includes new variables, 
   useful file locations, etc...
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](https://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

### Code of Conduct

#### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, color, religion, or sexual identity and
orientation.

#### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

#### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

#### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

#### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at fr-ansible-github@fr.clara.net. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

#### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version] and 
[Good-CONTRIBUTING.md-template.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426)

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/

## Author Information

Claranet France