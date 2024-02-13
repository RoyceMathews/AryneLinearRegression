import pandas as pd
from typing import Union
from input_file import InputFile
from reaction import Reaction
from training_node import TrainingNode
from lolo_node import LOLONode
from loo_node import LOONode

file1 = InputFile("regression using Gibbs.xlsx",
                  "LOLO",
                  "Reaction ID",
                  "Precat. Used",
                  "Norm cone(sigma meta)",
                  "Norm cone(charton)",
                  "ΔΔG")


def main():

    reactions1 = populate_reactions_from_excel(file1)
    training_node1 = TrainingNode(reactions1)
    lolo_node1 = LOLONode(reactions1)
    loo_node1 = LOONode(reactions1)
    print(f"Training Node R^2: {training_node1.get_r_squared()}\n"
          f"Leave One Ligand Out R^2: {lolo_node1.get_r_squared()}\n"
          f"Leave One Out R^2: {loo_node1.get_r_squared()}")

    print(loo_node1.get_coefficients())
    print(loo_node1.get_predicted_gibbs_free_energy_difference())


def populate_reactions_from_excel(file: InputFile) -> Union[list, None]:
    try:
        aryne_raw_data = pd.read_excel(file.get_file_name(), sheet_name=file.get_sheet_name())
    except FileNotFoundError:
        print("The file name was not found")
        return None
    except ValueError:
        print("The specified sheet names were not found")
        return None

    # Reaction ID, Ligand, Norm Cone Sigma, Norm Cone Charton, Gibbs Free Energy Difference columns
    aryne_data = aryne_raw_data[[file.get_reaction_id_col_name(),
                                 file.get_ligand_col_name(),
                                 file.get_norm_cone_sigma_col_name(),
                                 file.get_norm_cone_charton_col_name(),
                                 file.get_gibbs_free_energy_difference_col_name()]]
    aryne_data = aryne_data.dropna()

    reaction_list = []

    # Create reaction objects, store in reaction_list
    for row in range(len(aryne_data)):
        reaction_list.append(
            Reaction(aryne_data.iloc[row][file.get_reaction_id_col_name()],
                     aryne_data.iloc[row][file.get_ligand_col_name()],
                     aryne_data.iloc[row][file.get_norm_cone_sigma_col_name()],
                     aryne_data.iloc[row][file.get_norm_cone_charton_col_name()],
                     aryne_data.iloc[row][file.get_gibbs_free_energy_difference_col_name()]))

    return reaction_list


if __name__ == "__main__":
    main()
