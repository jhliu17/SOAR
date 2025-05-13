from nntool.slurm import SlurmConfig
from .misc import output_folder

single_gpu_slurm_config = SlurmConfig(
    mode="slurm",
    slurm_job_name="chat",
    slurm_partition="zhanglab.p",
    slurm_output_folder=f"{output_folder}/slurm",
    node_list="laniakea",
    cpus_per_task=4,
    gpus_per_task=1,
    mem="64GB",
    pack_code=True,
    use_packed_code=True,
)

slurm_config = SlurmConfig(
    mode="slurm",
    slurm_job_name="chat",
    slurm_partition="zhanglab.p",
    slurm_output_folder=f"{output_folder}/slurm",
    node_list="laniakea",
    cpus_per_task=4,
    gpus_per_task=4,
    mem="64GB",
    pack_code=True,
    use_packed_code=True,
)

large_slurm_config = SlurmConfig(
    mode="slurm",
    slurm_job_name="chat",
    slurm_partition="zhanglab.p",
    slurm_output_folder=f"{output_folder}/slurm",
    node_list="laniakea",
    cpus_per_task=8,
    gpus_per_task=8,
    mem="64GB",
    pack_code=True,
    use_packed_code=True,
)

cpu_slurm_config = SlurmConfig(
    mode="slurm",
    slurm_job_name="chat",
    slurm_partition="zhanglab.p",
    slurm_output_folder=f"{output_folder}/slurm",
    node_list="laniakea",
    cpus_per_task=1,
    gpus_per_task=0,
    mem="16GB",
    pack_code=True,
    use_packed_code=True,
)
