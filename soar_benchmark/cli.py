from tyro.extras import SubcommandApp
from dataclasses import replace
from nntool.slurm import slurm_fn
from .configs.config_cell_type_annotation import (
    DefinedCellTypeAnnotationTaskConfig,
)
from soar_benchmark.dataset import JSONDatasetConfig
from soar_benchmark.task import CellTypeAnnotationTaskConfig, CellTypeAnnotationTask

app = SubcommandApp()


@slurm_fn
def run(config: CellTypeAnnotationTaskConfig):
    task = CellTypeAnnotationTask(config)
    task.run()


@app.command
def annotate(config: DefinedCellTypeAnnotationTaskConfig):
    run[config.slurm](config)


def main():
    app.cli()


if __name__ == "__main__":
    main()
