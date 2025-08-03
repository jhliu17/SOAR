import tyro

from nntool.slurm import slurm_fn
from configs.config_cell_type_annotation import (
    DefinedCellTypeAnnotationTaskConfig,
)
from soar_benchmark.task import CellTypeAnnotationTaskConfig, CellTypeAnnotationTask


@slurm_fn
def run(config: CellTypeAnnotationTaskConfig):
    task = CellTypeAnnotationTask(config)
    task.run()


if __name__ == "__main__":
    config: CellTypeAnnotationTaskConfig = tyro.cli(DefinedCellTypeAnnotationTaskConfig)
    run[config.slurm](config)
