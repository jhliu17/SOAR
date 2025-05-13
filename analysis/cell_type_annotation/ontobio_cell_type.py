import ontobio
from thefuzz import process
from collections import namedtuple

# Load Cell Ontology
ontology = ontobio.ontol_factory.OntologyFactory().create("cl")
CLCellType = namedtuple("CLCellType", ["name", "id", "original_name"])


def map_cell_name_to_cl_name(cell_name, return_ambiguity: bool = False):
    matches: list[CLCellType] = []
    for term in ontology.graph.nodes:
        label = ontology.label(term)

        # retrieve all candidates that contain the cell name
        if label is not None and cell_name.lower() in label.lower():
            matches.append(CLCellType(label, term, cell_name))

        if label is not None and label.lower() in cell_name.lower():
            matches.append(CLCellType(label, term, cell_name))

        # exact match
        if label is not None and cell_name.lower() == label.lower():
            return CLCellType(label, term, cell_name)

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        # handle multiple matches, e.g., return all or return the best fuzzy match one
        if return_ambiguity:
            return matches

        choices = {m.name: i for i, m in enumerate(matches)}
        best_match = process.extractOne(cell_name, choices.keys())
        return matches[choices[best_match[0]]]
    return CLCellType("", "", cell_name)


def get_broad_cell_type(cl: CLCellType):
    # Find parent terms
    parents = ontology.parents(cl.id)
    broad_types: list[CLCellType] = []
    for parent in parents:
        parent_label = ontology.label(parent)
        broad_types.append(CLCellType(parent_label, parent, cl.original_name))
    return broad_types


def map_cell_name_to_broad_type(cell_name):
    clname = map_cell_name_to_cl_name(cell_name)

    if clname is not None:
        return get_broad_cell_type(clname)
    return None


if __name__ == "__main__":
    # Example usage
    cell_name = "T cell"
    cl_matches = map_cell_name_to_cl_name(cell_name)
    print(f"Cell name: {cl_matches.name}, CL ID: {cl_matches.id}")

    # Example usage
    cell_name = "neuron"
    broad_types = map_cell_name_to_broad_type(cell_name)
    print(f"Cell name: {cell_name}, Broad cell types: {broad_types}")
