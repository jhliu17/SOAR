import json
from typing import Union
import scanpy as sc
import pandas as pd

from dataclasses import dataclass
from torch.utils.data import Dataset


@dataclass
class DatasetBaseConfig:
    csv_path: str = ""
    demo_path: str = ""
    use_demo: bool = False


class DatasetBase(Dataset):
    def __init__(
        self,
        config: DatasetBaseConfig,
    ):
        self.use_demo = config.use_demo
        self.demo = ""
        if self.use_demo:
            with open(config.demo_path) as f:
                self.demo = json.load(f)

    def __len__(self):
        raise NotImplementedError

    def get_sample(self, index):
        raise NotImplementedError

    def __getitem__(self, index):
        sample = self.get_sample(index)
        return sample


@dataclass
class CSVDatasetConfig(DatasetBaseConfig):
    pass


class CSVDataset(DatasetBase):
    def __init__(
        self,
        config: CSVDatasetConfig,
    ):
        super().__init__(config)
        self.df = pd.read_csv(config.csv_path)

    def __len__(self):
        return len(self.df)

    def get_sample(self, index):
        row = self.df.iloc[index]
        dataset = row["dataset"]
        tissue = row["tissue"]
        genes = [i.strip() for i in row["marker"].split(",")]
        label = row["manual annotation"]
        label_cl = row["manual CLname"]
        label_id = row["manual CLID"]
        broadtype = row["manual broadtype"]

        sample = {
            "index": index,
            "dataset": dataset,
            "tissue": tissue,
            "genes": genes,
            "label": label,
            "label_cl": label_cl,
            "label_id": label_id,
            "broadtype": broadtype,
            "demo": self.demo,
        }
        return sample

    def __getitem__(self, index):
        sample = self.get_sample(index)
        return sample


@dataclass
class H5ADDatasetConfig(DatasetBaseConfig):
    h5ad_path: str = ""
    tissue: str = ""
    dataset_name: str = ""
    gene_num: int = 10
    cell_type_to_label: Union[dict[str, str], None] = None


class H5ADDataset(DatasetBase):
    def __init__(
        self,
        config: H5ADDatasetConfig,
    ):
        super().__init__(config)
        self.config = config
        self.adata = sc.read_h5ad(config.h5ad_path)
        self.sample_list = self.adata.uns["gene_list"]["names"].dtype.names

    def __len__(self):
        return len(self.sample_list)

    def get_sample(self, index):
        cell_type = self.sample_list[index]

        dataset = self.config.dataset_name
        tissue = self.config.tissue
        genes = list(self.adata.uns["gene_list"]["names"][cell_type][: self.config.gene_num])
        label = (
            cell_type
            if self.config.cell_type_to_label is None
            else self.config.cell_type_to_label.get(cell_type, cell_type)
        )
        label_cl = ""
        label_id = ""
        broadtype = ""

        sample = {
            "index": index,
            "dataset": dataset,
            "tissue": tissue,
            "genes": genes,
            "label": label,
            "label_cl": label_cl,
            "label_id": label_id,
            "broadtype": broadtype,
            "demo": self.demo,
        }
        return sample

    def __getitem__(self, index):
        sample = self.get_sample(index)
        return sample
