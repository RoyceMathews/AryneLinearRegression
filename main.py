import pandas as pd
from typing import Union
from input_file import InputFile
from reaction import Reaction
from training_node import TrainingNode
from lolo_node import LOLONode
from loo_node import LOONode
import logging as log

FILE_NAME = "regression using Gibbs.xlsx"
SHEET_NAME = "LOLO"
REACTION_COLUMN_NAME = "Reaction ID"
LIGAND_COLUMN_NAME = "Precat. Used"
NORM_CONE_SIGMA_COLUMN_NAME = "Norm cone(sigma meta)"
NORM_CONE_CHARTON_COLUMN_NAME = "Norm cone(charton)"
GIBBS_COLUMN_NAME = "ΔΔG"


def main():
    file1 = InputFile(
        FILE_NAME,
        SHEET_NAME,
        REACTION_COLUMN_NAME,
        LIGAND_COLUMN_NAME,
        NORM_CONE_SIGMA_COLUMN_NAME,
        NORM_CONE_CHARTON_COLUMN_NAME,
        GIBBS_COLUMN_NAME
    )

    try:
        reactions1 = populate_reactions_from_excel(file1)
    except Exception:
        exit(-1)

    training_node1 = TrainingNode(reactions1)
    lolo_node1 = LOLONode(reactions1)
    loo_node1 = LOONode(reactions1)
    log.info("Training Node R^2: %s", training_node1.get_r_squared())
    log.info("Leave One Ligand Out R^2: %s", lolo_node1.get_r_squared())
    log.info("Leave One Out R^2: %s", loo_node1.get_r_squared())

    log.info('LOO Node Coefficients %s', loo_node1.get_coefficients())
    log.info('LOO Node Predicted Gibbs Free Energy Difference %s',
             loo_node1.get_predicted_gibbs_free_energy_difference())


def populate_reactions_from_excel(file: InputFile) -> Union[list, None]:
    try:
        aryne_raw_data = pd.read_excel(file.get_file_name(), sheet_name=file.get_sheet_name())
    except FileNotFoundError as e:
        log.exception("The file name was not found")
        raise
    except ValueError:
        log.exception("The specified sheet names were not found")
        raise

    # Reaction ID, Ligand, Norm Cone Sigma, Norm Cone Charton, Gibbs Free Energy Difference columns
    aryne_data = aryne_raw_data[[file.get_reaction_id_col_name(),
                                 file.get_ligand_col_name(),
                                 file.get_norm_cone_sigma_col_name(),
                                 file.get_norm_cone_charton_col_name(),
                                 file.get_gibbs_free_energy_difference_col_name()]]
    aryne_data = aryne_data.dropna()

    reaction_list = []

    # Create reaction objects, store in reaction_list
    for _, row in aryne_raw_data.iterrows():
        reaction = Reaction(row[file.get_reaction_id_col_name()],
                            row[file.get_ligand_col_name()],
                            row[file.get_norm_cone_sigma_col_name()],
                            row[file.get_norm_cone_charton_col_name()],
                            row[file.get_gibbs_free_energy_difference_col_name()])
        reaction_list.append(reaction)

    return reaction_list


if __name__ == "__main__":
    main()
