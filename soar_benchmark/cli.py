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
def experiment(config: DefinedCellTypeAnnotationTaskConfig):
    config: CellTypeAnnotationTaskConfig
    run[config.slurm](config)


@app.command
def annotate(config: DefinedCellTypeAnnotationTaskConfig, dataset: JSONDatasetConfig):
    config: CellTypeAnnotationTaskConfig
    config = replace(config, dataset=dataset)
    run[config.slurm](config)


def main():
    app.cli()


if __name__ == "__main__":
    main()
