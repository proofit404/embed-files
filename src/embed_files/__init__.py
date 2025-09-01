from ctypes import c_void_p
from json import dumps
from pathlib import Path

from click import argument
from click import command
from click import echo
from click import option
from click import Path as ClickPath
from llama_cpp import Llama
from llama_cpp import llama_log_callback
from llama_cpp import llama_log_set


@command()
@argument(
    "files",
    nargs=-1,
    type=ClickPath(path_type=Path, exists=True, dir_okay=False),
)
@option(
    "-m",
    "--model",
    required=True,
    type=ClickPath(path_type=Path, exists=True, dir_okay=False),
)
@option(
    "-t",
    "--template",
    required=True,
)
def cli(files: list[Path], model: Path, template: str) -> None:
    _verify_files(files)
    _verify_template(template)

    llama = Llama(
        model_path=str(model),
        embedding=True,
        verbose=False,
        n_ctx=0,  # Take text context from model.
    )

    data = {}

    for path in files:
        results = llama.create_embedding(template.format(path.read_text()))
        assert len(results["data"]) == 1
        data[str(path)] = results["data"][0]["embedding"]

    echo(dumps(data, ensure_ascii=False))


def _verify_files(files: list[Path]) -> None:
    if not files:
        echo("No files specified", err=True)
        exit(1)


def _verify_template(template: str) -> None:
    if "{}" not in template or template.count("{") != 1 or template.count("}") != 1:
        echo("Invalid template", err=True)
        exit(1)


@llama_log_callback  # type: ignore[misc]
def _ignore_log(level: int, text: bytes, user_data: c_void_p) -> None:
    pass


llama_log_set(_ignore_log, c_void_p(0))
