from subprocess import PIPE, run


def _bump_version():
    current_version = _run_command(["poetry", "version", "-s"], capture_output=True)

    _run_command(["poetry", "version", "patch", "-s"])

    new_version = _run_command(["poetry", "version", "-s"], capture_output=True)

    for path in ["convert_lqm_to_json/__init__.py", "tests/test___init__.py"]:
        _replace_in_file(path, current_version, new_version)

    return new_version


def _replace_in_file(file_path, current_string, new_string):
    with open(file_path, "r+") as file:
        text = file.read()
        file.seek(0)
        file.write(text.replace(current_string, new_string))
        file.truncate()


def _run_command(args, capture_output=False):
    result = run(args, capture_output, text=True if capture_output else False)

    if result.returncode == 0:
        if capture_output:
            return result.stdout.strip()

    else:
        if capture_output:
            print(
                result.stderr.strip() or f"Error encountered running {arg[0]} command."
            )

        exit(result.returncode)


def build():
    _run_command(["rm", "-rf", "dist"])
    _run_command(["poetry", "build"])


def commit():
    _run_command(["git", "add", "--all"])
    _run_command(["git", "commit"])


def publish():
    version = _bump_version()
    commit()
    _run_command(["git", "tag", "-a", f"v{version}", "-m", f"Version {version}"])
    _run_command(["git", "push", "--follow-tags"])


def test():
    _run_command(["pytest", "tests"])
