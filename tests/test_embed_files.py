from json import loads

import pytest
from click.testing import CliRunner

from embed_files import cli


@pytest.mark.parametrize(
    "option_name",
    [pytest.param("-m", id="0"), pytest.param("--model", id="1")],
)
def test_embed_files(option_name: str) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [option_name, "testing/nomic-embed-text-v1.5.gguf", "docs/installation.md"],
    )
    assert result.exit_code == 0

    output: dict[str, list[float]] = loads(result.output)
    assert list(output) == ["docs/installation.md"]

    vector = output["docs/installation.md"]
    assert isinstance(vector, list)
    assert all(isinstance(x, float) for x in vector)


def test_no_model_error() -> None:
    runner = CliRunner()

    result = runner.invoke(cli, ["docs/installation.md"])
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Missing option '-m' / '--model'.
"""
    assert result.output == expected


def test_model_does_not_exists_error() -> None:
    runner = CliRunner()

    result = runner.invoke(cli, ["-m", "nshuasno.gguf", "docs/installation.md"])
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Invalid value for '-m' / '--model': Path 'nshuasno.gguf' does not exist.
"""
    assert result.output == expected


def test_no_files_error() -> None:
    runner = CliRunner()

    result = runner.invoke(cli, ["-m", "testing/nomic-embed-text-v1.5.gguf"])
    assert result.exit_code == 1

    assert result.output == "No files specified\n"


def test_files_does_not_exists_error() -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "--model",
            "testing/nomic-embed-text-v1.5.gguf",
            "haontsuh.md",
        ],
    )
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Invalid value for '[FILES]...': Path 'haontsuh.md' does not exist.
"""
    assert result.output == expected
