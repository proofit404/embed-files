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


@llama_log_callback  # type: ignore[misc]
def _ignore_log(level: int, text: bytes, user_data: c_void_p) -> None:
    pass


llama_log_set(_ignore_log, c_void_p(0))


@command()
@argument("files", nargs=-1, type=ClickPath(path_type=Path, exists=True))
@option("-m", "--model", required=True, type=ClickPath(path_type=Path, exists=True))
def cli(files: list[Path], model: Path) -> None:
    if not files:
        echo("No files specified", err=True)
        exit(1)

    llama = Llama(
        model_path=str(model),
        embedding=True,
        verbose=False,
        n_ctx=0,  # Take text context from model.
    )

    data = {}

    for path in files:
        results = llama.create_embedding(f"clustering: {path.read_text()}")
        assert len(results["data"]) == 1
        data[str(path)] = results["data"][0]["embedding"]

    echo(dumps(data, ensure_ascii=False))
