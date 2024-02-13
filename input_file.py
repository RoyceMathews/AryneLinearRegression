import pandas as pd


class InputFile:

    def __init__(self, file_name: str, sheet_name: str, reaction_id_col_name: str, ligand_col_name: str,
                 norm_cone_sigma_col_name: str, norm_cone_charton_col_name: str,
                 gibbs_free_energy_difference_col_name: str):
        self._file_name = file_name
        self._sheet_name = sheet_name
        self._reaction_id_col_name = reaction_id_col_name
        self._ligand_col_name = ligand_col_name
        self._norm_cone_sigma_col_name = norm_cone_sigma_col_name
        self._norm_cone_charton_col_name = norm_cone_charton_col_name
        self._gibbs_free_energy_difference_col_name = gibbs_free_energy_difference_col_name

    def get_file_name(self):
        return self._file_name

    def get_sheet_name(self):
        return self._sheet_name

    def get_reaction_id_col_name(self):
        return self._reaction_id_col_name

    def get_ligand_col_name(self):
        return self._ligand_col_name

    def get_norm_cone_sigma_col_name(self):
        return self._norm_cone_sigma_col_name

    def get_norm_cone_charton_col_name(self):
        return self._norm_cone_charton_col_name

    def get_gibbs_free_energy_difference_col_name(self):
        return self._gibbs_free_energy_difference_col_name
