from io import StringIO
import os

from dotenv import load_dotenv, find_dotenv
from clikit.ui.components import Paragraph
from clikit.api.args.format.args_format import NoSuchOptionException
from cleo import option
from poetry.console.application import Application
from poetry.console.commands.run import RunCommand
from poetry.console.commands.shell import ShellCommand

from prose.__version__ import __version__


class ConfigCommand:

    def get_prose_config(self, *args, data=None, default=None):
        if data is None:
            args = ['tool', 'prose'] + list(args)
            data = self.application.poetry.pyproject.data

        if args and args[0] in data:
            if len(args) == 1:
                return data[args[0]]

            else:
                return self.get_prose_config(*args[1:], data=data[args[0]], default=default)

        return default


class DotenvCommand(ConfigCommand):

    def set_envs(self):
        envs = self.get_prose_config('env')
        if envs:
            stream = StringIO()
            for key, value in envs.items():
                stream.write("{}={}\n".format(key, value))

            stream.seek(0)
            # load env from toml config
            load_dotenv(stream=stream, override=True)

        # load from env from .env
        envpath = find_dotenv(usecwd=True)
        if envpath:
            load_dotenv(envpath, override=True)

        envs = self.option("env")
        for env in envs:
            load_dotenv(env, override=True)

    def argument(self, key=None, original=False):
        args = super().argument(key=key)

        if key == "args" and not original:
            envs, arg_begin = self.extract_env(args)
            return args[arg_begin:]

        return args

    def extract_env(self, original):
        envs = []
        arg_begin = 0

        # -enarf; -e narf; --env narf; --env=narf
        for i, a in enumerate(original):
            if a == "-e" or a == "--env":
                envs.append(original[i + 1])
                arg_begin = i + 2

            elif a.startswith("-e"):
                envs.append(a.replace("-e", ""))
                arg_begin = i + 1

            elif a.startswith("--env="):
                envs.append(a.replace("--env", ""))
                arg_begin = i + 1

        return envs, arg_begin

    def option(self, key=None):
        try:
            return super().option(key=key)

        except NoSuchOptionException:
            if key == 'env':
                args = self.argument("args", original=True)
                envs, arg_begin = self.extract_env(args)
                return envs

            raise

    def handle(self):
        os.environ['PROSE_PROJECT_HOME'] = str(self.application.poetry.pyproject.file.path.parent)
        self.set_envs()
        return super().handle()


class ProseRun(DotenvCommand, RunCommand):
    pass


class ProsePoe(ProseRun):
    name = "poe"
    description = "task runner using poethepoet module"

    def handle(self):
        os.environ['PROSE_PROJECT_HOME'] = str(self.application.poetry.pyproject.file.path.parent)
        self.set_envs()

        args = self.argument("args")
        return self.env.execute("poe", *args)


class ProseShell(DotenvCommand, ShellCommand):
    options = [option("env", "e", "Dotenv file to load", multiple=True, flag=False)]


class ProseApp(Application):
    OVERRIDE_COMMANDS = {
        'run': ProseRun,
        'shell': ProseShell,
    }

    def __init__(self):
        super().__init__()

        self._dispatcher.add_listener("pre-handle", self.prose_version)

    def prose_version(self, event, event_name, dispatcher):
        if event.args.is_option_set("version"):
            p = Paragraph("Prose version <c1>{}</c1>".format(__version__))
            p.render(event.io)

    def get_default_commands(self):
        commands = super().get_default_commands()
        for i, cmd in enumerate(commands):
            if cmd.name in self.OVERRIDE_COMMANDS:
                commands[i] = self.OVERRIDE_COMMANDS[cmd.name]()

        commands.append(ProsePoe())
        return commands


def main():
    return ProseApp().run()


if __name__ == "__main__":
    main()
