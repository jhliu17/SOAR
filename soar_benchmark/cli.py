from tyro.extras import SubcommandApp

from .run import start_annotation_task
from .configs.config_cell_type_annotation import (
    DefinedCellTypeAnnotationTaskConfig,
)

app = SubcommandApp()


@app.command
def annotate(config: DefinedCellTypeAnnotationTaskConfig):
    start_annotation_task[config.slurm](config)


def main():
    app.cli()


if __name__ == "__main__":
    main()
