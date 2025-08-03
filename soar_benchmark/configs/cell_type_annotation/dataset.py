from soar_benchmark.dataset import CSVDatasetConfig
from .misc import project_path

# datasets
soar_rna_0shot_dataset = CSVDatasetConfig(
    f"{project_path}/datasets/soar_rna/data.csv",
)
