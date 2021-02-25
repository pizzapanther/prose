from io import StringIO
import os

from dotenv import load_dotenv
from poetry.console.application import Application
from poetry.console.commands.run import RunCommand
from poetry.console.commands.shell import ShellCommand


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
        stream = StringIO()
        for key, value in envs.items():
            stream.write("{}={}\n".format(key, value))

        stream.seek(0)
        load_dotenv(stream=stream, override=True)

    def handle(self):
        os.environ['PROSE_PROJECT_HOME'] =  str(self.application.poetry.pyproject.file.path.parent)
        self.set_envs()
        return super().handle()


class ProseRun(DotenvCommand, RunCommand):
    pass


class ProseShell(DotenvCommand, ShellCommand):
    pass


class ProseApp(Application):
    OVERRIDE_COMMANDS = {
        'run': ProseRun,
        'shell': ProseShell,
    }

    def get_default_commands(self):
        commands = super().get_default_commands()
        for i, cmd in enumerate(commands):
            if cmd.name in self.OVERRIDE_COMMANDS:
                commands[i] = self.OVERRIDE_COMMANDS[cmd.name]()

        return commands


def main():
    return ProseApp().run()


if __name__ == "__main__":
    main()
