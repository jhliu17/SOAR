from nntool.utils import get_output_path
from nntool.utils.utils_module import read_toml_file

# general config
project_path = read_toml_file("./env.toml")["project"]["path"]
huggingface_token = read_toml_file("./env.toml")["huggingface"]["token"]
openai_token = read_toml_file("./env.toml")["openai"]["token"]

output_folder = get_output_path(f"{project_path}/outputs/cell_type_annotation", append_date=True)[0]
