class Reaction:
    def __init__(self, reaction_id, ligand, norm_cone_sigma, norm_cone_charton, gibbs_free_energy_difference):
        self._reaction_id = reaction_id
        self._ligand = ligand
        self._norm_cone_sigma = norm_cone_sigma
        self._norm_cone_charton = norm_cone_charton
        self._gibbs_free_energy_difference = gibbs_free_energy_difference

    def get_reaction_id(self):
        return self._reaction_id

    def get_ligand(self):
        return self._ligand

    def get_norm_cone_sigma(self):
        return self._norm_cone_sigma

    def get_norm_cone_charton(self):
        return self._norm_cone_charton

    def get_gibbs_free_energy_difference(self):
        return self._gibbs_free_energy_difference
