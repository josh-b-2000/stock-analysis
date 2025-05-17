import typer

app = typer.Typer()


@app.command()
def extract() -> None:
    raise NotImplementedError()


@app.command()
def recommend_buy() -> None:
    raise NotImplementedError()


def cli() -> None:
    app()


if __name__ == "__main__":
    cli()
