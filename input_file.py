import pandas as pd
from dataclasses import dataclass


@dataclass(frozen=True)
class InputFile:
    file_name: str
    sheet_name: str
    reaction_id_col_name: str
    ligand_col_name: str
    norm_cone_sigma_col_name: str
    norm_cone_charton_col_name: str
    gibbs_free_energy_difference_col_name: str

    def get_file_name(self):
        return self.file_name

    def get_sheet_name(self):
        return self.sheet_name

    def get_reaction_id_col_name(self):
        return self.reaction_id_col_name

    def get_ligand_col_name(self):
        return self.ligand_col_name

    def get_norm_cone_sigma_col_name(self):
        return self.norm_cone_sigma_col_name

    def get_norm_cone_charton_col_name(self):
        return self.norm_cone_charton_col_name

    def get_gibbs_free_energy_difference_col_name(self):
        return self.gibbs_free_energy_difference_col_name
