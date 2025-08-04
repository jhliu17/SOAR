from soar_benchmark.dataset import JSONDatasetConfig
from .misc import project_path

# datasets
soar_rna_0shot_dataset = JSONDatasetConfig(
    json_path=f"{project_path}/datasets/soar_rna.json",
)
