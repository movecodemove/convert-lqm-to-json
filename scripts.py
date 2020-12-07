from subprocess import PIPE, run


def _bump_version():
    current_version = _run_and_capture(["poetry", "version", "-s"])

    run(["poetry", "version", "patch", "-s"])

    new_version = _run_and_capture(["poetry", "version", "-s"])

    for path in ["convert_lqm_to_json/__init__.py", "tests/test___init__.py"]:
        _replace_in_file(path, current_version, new_version)

    return new_version


def _replace_in_file(file_path, current_string, new_string):
    with open(file_path, "r+") as file:
        text = file.read()
        file.seek(0)
        file.write(text.replace(current_string, new_string))
        file.truncate()


def _run_and_capture(args):
    return run(args, stdout=PIPE, text=True).stdout.strip()


def build():
    run(["rm", "-rf", "dist"])
    run(["poetry", "build"])


def publish():
    test()
    version = _bump_version()
    run(["git", "add", "--all"])
    run(["git", "commit"])
    run(["git", "tag", "-a", f"v{version}", "-m", f"Version {version}"])
    run(["git", "push", "--follow-tags"])


def test():
    run(["pytest", "tests"])
