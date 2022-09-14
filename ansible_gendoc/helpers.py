from pathlib import Path
from rich import print
import re
import os
import fnmatch
import yaml


def load_yml_file(fpath, verbose):

    # yaml = ruamel.yaml.YAML(typ='safe')

    with open(fpath, "r") as stream:
        content = yaml.load(stream, Loader=yaml.FullLoader)
    if verbose:
        print("Loaded '%s':\n" % fpath)
        print(content)
        print("\n")

    return content


def load_yml_files(dpath, verbose):
    """
    Safe load multiple yaml files.

    All top level values are expected to be keys.
    """
    content = []
    if os.path.isdir(dpath):
        for f in get_filenames(dpath, "*.yml"):
            new_content = {
                "filename": f,
                "content": load_yml_file(os.path.join(dpath, f), verbose),
            }
            content.append(new_content)
    if verbose:
        print("Loaded '%s':\n" % dpath)
        print(content)
        print("\n")

    return content


def get_filenames(dpath, pattern):
    """Yield files in given directory matching pattern."""
    return fnmatch.filter(os.listdir(dpath), pattern)


def write_file(data, fpath):
    """write a file to disk only if content has changed."""
    Path(os.path.dirname(fpath)).mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(fpath):
        with open(fpath, "w") as f:
            f.write(data)
    else:
        with open(fpath, "r+") as f:
            # replace content only if needed
            if data != f.read():
                f.truncate(0)
                f.seek(0)
                f.write(data)


def read_file(fpath):
    """
    Read a file and literaly return content.
    If file is yaml, it must skip the stream header.
    """
    with open(fpath, "r") as f:
        # skip '---' header of yaml streams
        if os.path.splitext(fpath)[1] == ".yml":
            f.readline()

        # eat up every empty lines
        pos = f.tell()
        line = f.readline()

        while not line.strip():
            pos = f.tell()
            line = f.readline()

        # go back to non-empty line
        f.seek(pos)

        return f.read()


def read_files(dpath, type, verbose):
    """
    Read every files files under a given directory.
    Return a list of dictionaries. Each dictionary contains the filename
    and the file content.
    """
    if os.path.isdir(dpath):
        dfiles = []
        for f in get_filenames(dpath, type):
            if verbose:
                print("Reading file '%s'" % os.path.join(dpath, f))
            dfiles.append({"filename": f, "content": read_file(os.path.join(dpath, f))})
        return dfiles
    else:
        if verbose:
            print("'%s' directory doesn't exist...skipping" % dpath)
        return None


def controlleveltitle(mdfiles):
    for file in mdfiles:
        if "README" not in file["filename"]:
            file["content"] = re.sub(r"((?:[#]+))", r"#\1", file["content"])
    return mdfiles

def _convert_dict_of_string(d):

    if isinstance(d, dict):
        output = {}
        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                t = yaml.dump(v)
            else:
                t = v
            output[k] = t
        return output
    else:
        return d


def convert_dict_of_string(dict):
    """ """
    output = []
    for file in dict:
        temp = {}
        temp["filename"] = file['filename']
        temp['content'] = _convert_dict_of_string(file['content'])
        output.append(temp)

    return output


def convert_string(dict):
    """ """
    output = []
    for file in dict:
        temp = {}
        temp["filename"] = file['filename']
        value =  yaml.dump(file['content'],Dumper=MyDumper)
        temp['content'] = re.sub(r'^(.)$',r'        \1', value)
        output.append(temp)

    return output


import yaml

class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)