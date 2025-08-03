import tyro

from .cell_type_annotation import experiment_soar_rna


# combine all experiments
experiments = dict(
    **experiment_soar_rna.experiments,
)
DefinedCellTypeAnnotationTaskConfig = tyro.extras.subcommand_type_from_defaults(experiments)
