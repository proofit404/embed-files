from json import loads

import pytest
from click.testing import CliRunner

from embed_files import cli


model_argument = pytest.mark.parametrize(
    "model_argument",
    [
        pytest.param("-m", id="0"),
        pytest.param("--model", id="1"),
    ],
)


template_argument = pytest.mark.parametrize(
    "template_argument",
    [
        pytest.param("-t", id="0"),
        pytest.param("--template", id="1"),
    ],
)


model_path = pytest.mark.parametrize(
    ("model_path", "template_value"),
    [
        pytest.param("vendor/mxbai-embed-xsmall-v1.gguf", "{}", id="0"),
        pytest.param("vendor/nomic-embed-text-v1.5.gguf", "clustering: {}", id="1"),
    ],
)


@model_argument
@template_argument
@model_path
def test_embed_files(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            model_argument,
            model_path,
            template_argument,
            template_value,
            "docs/installation.md",
        ],
    )
    assert result.exit_code == 0

    output: dict[str, list[float]] = loads(result.output)
    assert list(output) == ["docs/installation.md"]

    vector = output["docs/installation.md"]
    assert isinstance(vector, list)
    assert all(isinstance(x, float) for x in vector)


# Files.


@model_argument
@template_argument
@model_path
def test_no_files_error(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [model_argument, model_path, template_argument, template_value],
    )
    assert result.exit_code == 1

    assert result.output == "No files specified\n"


@model_argument
@template_argument
@model_path
def test_files_does_not_exists_error(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [model_argument, model_path, template_argument, template_value, "haontsuh.md"],
    )
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Invalid value for '[FILES]...': File 'haontsuh.md' does not exist.
"""
    assert result.output == expected


@model_argument
@template_argument
@model_path
def test_files_is_dir_error(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [model_argument, model_path, template_argument, template_value, "docs"],
    )
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Invalid value for '[FILES]...': File 'docs' is a directory.
"""
    assert result.output == expected


# Model.


@template_argument
@model_path
def test_no_model_error(
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [template_argument, template_value, "docs/installation.md"],
    )
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Missing option '-m' / '--model'.
"""
    assert result.output == expected


@model_argument
@template_argument
@model_path
def test_model_does_not_exists_error(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            model_argument,
            "nshuasno.gguf",
            template_argument,
            template_value,
            "docs/installation.md",
        ],
    )
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Invalid value for '-m' / '--model': File 'nshuasno.gguf' does not exist.
"""
    assert result.output == expected


@model_argument
@template_argument
@model_path
def test_model_is_dir_error(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            model_argument,
            "vendor",
            template_argument,
            template_value,
            "docs/installation.md",
        ],
    )
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Invalid value for '-m' / '--model': File 'vendor' is a directory.
"""
    assert result.output == expected


# Template.


@model_argument
@model_path
def test_no_template_error(
    model_argument: str,
    model_path: str,
    template_value: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(cli, [model_argument, model_path, "docs/installation.md"])
    assert result.exit_code == 2

    expected = """Usage: cli [OPTIONS] [FILES]...
Try 'cli --help' for help.

Error: Missing option '-t' / '--template'.
"""
    assert result.output == expected


@model_argument
@template_argument
@model_path
@pytest.mark.parametrize(
    "template_invalid",
    [
        pytest.param("foo", id="0"),  # No {content} placeholder.
        pytest.param("{foo}", id="1"),  # Unknown placeholder.
        pytest.param("foo {", id="2"),  # Invalid syntax: unclosed "{" char.
    ],
)
def test_invalid_template(
    model_argument: str,
    model_path: str,
    template_argument: str,
    template_value: str,
    template_invalid: str,
) -> None:
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            model_argument,
            model_path,
            template_argument,
            template_invalid,
            "docs/installation.md",
        ],
    )
    assert result.exit_code == 1

    assert result.output == "Invalid template\n"
