from jinja2 import Environment, PackageLoader, FileSystemLoader
from rich import print
from pathlib import Path
from ansible_gendoc.helpers import (
    load_yml_file,
    load_yml_files,
    write_file,
    read_files,
    controlleveltitle,
    convert_dict_of_string,
    convert_string
)
from git import Repo

import subprocess
import os
import typer


class Gendoc:
    def __init__(self, **kwargs):
        """initiate object with provided options."""
        self.mode = kwargs.get("mode")
        self.verbose = kwargs.get("verbose")
        self.dry_run = kwargs.get("dry_run")
        self.sphinx = kwargs.get("sphinx")
        if "target" in kwargs:
            self.target = os.path.abspath(kwargs.get("target"))
        self.rolespath = os.path.abspath(kwargs.get("path"))
        self.clean = kwargs.get("clean")
        self.opts = kwargs
        self.dirpath = os.getcwd()

    def _run_command(self, command):
        """ """
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
        )
        out, err = p.communicate()
        return_code = p.returncode
        return {
            "code": p.returncode,
            "out": out,
            "err": err,
        }


    def _make_role_doc(self, role):
        # Read ansible galaxy info
        if os.path.isfile(os.path.join(role["path"], "meta/.galaxy_install_info")):
            ansible_galaxy_info = load_yml_file(
                os.path.join(role["path"], "meta/.galaxy_install_info"), self.verbose
            )
        else:
            ansible_galaxy_info = None
        ## Read meta of roles
        meta_vars = load_yml_file(
            os.path.join(role["path"], "meta/main.yml"), self.verbose
        )
        # load literaly role vars/*.yml
        vars_files = load_yml_files(os.path.join(role["path"], "vars"), self.verbose)
        # load literaly role defaults/*.yml
        defaults_files = load_yml_files(
            os.path.join(role["path"], "defaults"), self.verbose
        )

        docs_md_files = read_files(os.path.join(role["path"]), "*.md", self.verbose)
        docs_md_files = controlleveltitle(docs_md_files)

        # load template and create templating environment
        if os.path.isfile(os.path.join(self.rolespath, "templates/README.j2")):
            env = Environment(
                loader=FileSystemLoader(searchpath=os.path.join(self.rolespath, "templates")),
                lstrip_blocks=True,
                trim_blocks=True,
            )
        else:
            env = Environment(
                loader=PackageLoader("ansible_gendoc", "templates"),
                lstrip_blocks=True,
                trim_blocks=True,
            )
        role_defaults_files = convert_dict_of_string(defaults_files)
        string_role_defaults_files = convert_string(defaults_files)
        # render role
        template = env.get_template("README.j2")
        # render method accepts the same arguments as the dict constructor
        t = template.render(
            self.opts,
            rolename=role["name"],
            repoowner=role["repoowner"],
            repourl=role["repourl"],
            reponame=role["reponame"],
            role_meta_vars=meta_vars,
            role_vars_files=convert_dict_of_string(vars_files),
            role_defaults_files=role_defaults_files,
            string_role_defaults_files=string_role_defaults_files,
            ansible_galaxy_info=ansible_galaxy_info,
            role_docs_md_files=docs_md_files,
        )
        if self.verbose or self.dry_run:
            print("\n*********************************************\n")
            print("Markdown Generated")
            print(t)

        if not self.dry_run:
            write_file(t, os.path.join(role["path"], "README.md"))
            if self.sphinx:
                write_file(
                    t,
                    os.path.join(
                        self.dirpath,
                        os.path.join(self.target, "source", role["target"]),
                        "readme.md",
                    ),
                )

        if self.verbose:
            print("Role '%s' ...done\n" % role["name"])

    def render(self):
        """
        Render README.md
        """
        role = {}
        if os.path.isfile(os.path.join(self.rolespath, "meta/main.yml")):
            role["name"] = os.path.basename(os.path.abspath(self.rolespath))
            role["repoowner"] = ""
            role["repourl"] = ""
            role["reponame"] = ""
            role["path"] = self.rolespath
            try:
                repo = Repo(role["path"])
                role["repoowner"] = repo.remotes.origin.url.split("/")[-2].split(':')[1]
                role["reponame"] = repo.remotes.origin.url.split("/")[-1].split(".git")[0]
                role["repourl"] = repo.remotes.origin.url.split(".git")[0].split(':')[1]
            except:
                pass
            self._make_role_doc(role)

        else:
            print("There is no role in this Path !!!!")
            raise typer.Exit(code=1)
