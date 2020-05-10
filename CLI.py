"""
Defines the command-line interface to DumbGDrive
"""

import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from DumbGDrive import *

class CLI:

    command_prefix='cli_method_'
    command_groups=['files']

    def __init__(self, group=None, command=None):
        if group is None or command is None:
            self.argv = sys.argv
            parser = argparse.ArgumentParser()
            parser.add_argument("group", type=str)
            parser.add_argument("command", type=str, default='', nargs="?")
            parse, unknown = parser.parse_known_args()
            self.group = parse.group
            self.cmd = parse.command
            sys.argv = [sys.argv[0]] + unknown
        else:
            self.group = group
            self.cmd = command

    def get_parse_dict(self, *spec):
        sys.argv[0] = self.group + " " + self.cmd
        parser = argparse.ArgumentParser()
        keys = []
        for arg in spec:
            if len(arg) > 1:
                arg_name, arg_dict = arg
            else:
                arg_name = arg[0]
                arg_dict = {}
            if 'dest' in arg_dict:
                keys.append(arg_dict['dest'])
            else:
                keys.append(arg_name)
            parser.add_argument(arg_name, **arg_dict)
        args = parser.parse_args()
        opts = {k: getattr(args, k) for k in keys}
        return {k:o for k,o in opts.items() if not (isinstance(o, str) and o=="")}

    def get_command(self, group=None, cmd=None):
        if group is None:
            group = self.group
        if cmd is None:
            cmd = self.cmd
        try:
            fun = getattr(self, self.command_prefix + group + "_" + cmd.replace("-", "_"))
        except AttributeError:
            fun = "Unknown command '{}' for command group '{}'".format(cmd.replace("_", "-"), group)
        return fun

    def get_help(self):
        from collections import OrderedDict

        if self.group == "":
            groups = OrderedDict((k, OrderedDict()) for k in self.command_groups)
        else:
            groups = OrderedDict([(self.group, OrderedDict())])

        indent="    "
        template = "{group}:\n{commands}"
        if self.cmd == "":
            for k in vars(type(self)):
                for g in groups:
                    if k.startswith("cli_method_"+g):
                        groups[g][k.split("_", 1)[1].replace("_", "-")] = getattr(self, k)
        else:
            template = "{group}{commands}"
            indent = "  "
            groups[self.group][self.cmd] = self.get_command()

        blocks = []
        make_command_info = lambda name, fun, indent: "{0}{1}{3}{0}  {2}".format(
            indent,
            name,
            "" if fun.__doc__ is None else fun.__doc__.strip(),
            "\n" if fun.__doc__ is not None else ""
            )
        for g in groups:
            blocks.append(
                template.format(
                    group = g,
                    commands = "\n".join(make_command_info(k, f, indent) for k, f in groups[g].items())
                )
            )
        return "\n\n".join(blocks)

    #region CLI Methods
    # this is just an example of how you can add
    def cli_method_files_list(self):
        """Lists files on a GDrive. Args: --root=ROOT_PATH"""
        parse_dict = self.get_parse_dict(
            ("--root", dict(default="", type=str, dest='root'))
        )
        print(FilesService.list(**parse_dict))
    #endregion

    def run(self):
        res = self.get_command()
        if not isinstance(res, str):
            res = res()
        else:
            print(res)
        return res

    def help(self, print_help=True):
        sys.argv.pop(1)
        res = self.get_help()
        if print_help:
            print(res)
        return res

    @classmethod
    def run_command(cls, parse):
        # detect whether interactive run or not
        interact = parse.interact or (len(sys.argv) == 1 and not parse.help and not parse.script)

        # in interactive/script envs we expose stuff
        if parse.script or interact:
             sys.path.insert(0, os.getcwd())
             interactive_env = {
                 "__name__": "DumbGDrive.script",
                 'FilesService': FilesService()
                }
        # in a script environment we just read in the script and run it
        if parse.script:
            with open(parse.script) as script:
                src = script.read()
            interactive_env["__file__"] = parse.script
            exec(src, interactive_env, interactive_env)
        elif parse.help:
            if len(sys.argv) == 1:
                print("dumbgdrive [--interact|--script] GRP CMD [ARGS] runs the DumbGDrive with the specified command")
            group = sys.argv[1] if len(sys.argv) > 1 else ""
            command = sys.argv[2] if len(sys.argv) > 2 else ""
            CLI(group=group, command=command).help()
        elif len(sys.argv) > 1:
            CLI().run()
        if interact:
            import code
            code.interact(banner="DumbGDrive Interactive Session", readfunc=None, local=interactive_env, exitmsg=None)

    @classmethod
    def run_parse(cls, parse, unknown):
        sys.argv = [sys.argv[0]] + unknown
        # print(sys.argv)
        cls.run_command(parse)

    @classmethod
    def parse_and_run(cls):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--script", default="", type=str, dest="script",
                            help='a script to run'
                            )
        parser.add_argument("--interact", default=True, action='store_const', const=True, dest="interact",
                            help='start an interactive session after running'
                            )
        parser.add_argument("--help", default=False, action='store_const', const=True, dest="help")
        parser.add_argument("--fulltb", default=False, action='store_const', const=True, dest="full_traceback")
        new_argv = []
        for k in sys.argv[1:]:
            if not k.startswith("--"):
                break
            new_argv.append(k)
        unknown = sys.argv[1+len(new_argv):]
        sys.argv = [sys.argv[0]]+new_argv
        parse = parser.parse_args()

        if parse.full_traceback:
            cls.run_parse(parse, unknown)
        else:
            error = None
            try:
                cls.run_parse(parse, unknown)
            except Exception as e:
                error = e
            if error is not None:
                print(error)

if __name__ == "__main__":
    CLI.parse_and_run()