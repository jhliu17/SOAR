from nntool.slurm import slurm_fn
from soar_benchmark.task import CellTypeAnnotationTaskConfig, CellTypeAnnotationTask


@slurm_fn
def start_annotation_task(config: CellTypeAnnotationTaskConfig):
    task = CellTypeAnnotationTask(config)
    task.run()
