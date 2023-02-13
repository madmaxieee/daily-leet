from rich.progress import Progress, SpinnerColumn, TextColumn

def BasicSpinner(transient=True):
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=transient,
    )