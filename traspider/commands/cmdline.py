import sys
from traspider.commands.create import CreateCommand



def _print_unknown_command(cmd_name):
    print("Unknown command: %s\n" % cmd_name)
    print('Output "traspider" to see how to create a spider file')


def _print_commands():
    print("Usage:")
    print("     traspider create -s <spider_name>")



def execute(argv=None):

    if argv is None:
        argv = sys.argv
    print(argv)
    if len(argv) < 2:
        _print_commands()
        return

    cmd_name = argv.pop(1)
    cmd_list = {
        "create": CreateCommand
    }

    if not cmd_name:
        _print_commands()
        sys.exit(0)
    elif cmd_name not in cmd_list:
        _print_unknown_command(cmd_name)
        sys.exit(2)

    cmd = cmd_list[cmd_name]()
    cmd.add_arguments()
    cmd.run_cmd()

    sys.exit()


if __name__ == '__main__':
    execute()
