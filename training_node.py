import pandas as pd
from sklearn import linear_model
from scipy.stats import linregress
import random


class TrainingNode:
    def __init__(self, reactions: list):
        self._reactions = reactions.copy()
        self._reaction_groups = {}
        self.populate_reaction_groups()
        self._coefficients = {}
        self.calculate_training_group_coefficients()
        self._predicted_gibbs_fed = []
        self.calculate_predicted_gibbs_free_energy_difference()
        self._r_squared = None
        self.calculate_r_squared()

    def populate_reaction_groups(self) -> None:
        """
        Randomizes the complete reaction list and stores half the list into a training list
        """
        random.shuffle(self._reactions)
        midpoint = len(self._reactions) // 2

        self._reaction_groups['Training Group'] = self._reactions[:midpoint]
        self._reaction_groups['Complete Group'] = self._reactions

    def calculate_training_group_coefficients(self) -> None:
        """
        Calculates linear regression coefficients for training group
        """

        independent_var_dict = {'norm_cone_sigma': [], 'norm_cone_charton': []}
        dependant_var_dict = {'gibbs_free_energy_difference': []}

        for reaction in self._reaction_groups['Training Group']:
            independent_var_dict['norm_cone_sigma'].append(reaction.get_norm_cone_sigma())
            independent_var_dict['norm_cone_charton'].append(reaction.get_norm_cone_charton())
            dependant_var_dict['gibbs_free_energy_difference'].append(reaction.get_gibbs_free_energy_difference())

        independent_var_df = pd.DataFrame(independent_var_dict)
        dependant_var_df = pd.DataFrame(dependant_var_dict)

        lin_reg = linear_model.LinearRegression()
        lin_reg.fit(independent_var_df, dependant_var_df)
        coefficients = lin_reg.coef_.tolist()

        self._coefficients['Norm Cone Sigma'] = coefficients[0][0]
        self._coefficients['Norm Cone Charton'] = coefficients[0][1]

    def calculate_predicted_gibbs_free_energy_difference(self) -> None:
        """
        Calculate predicted gibbs FED using training set coefficients and complete reaction group
        """
        for reaction in self._reaction_groups['Complete Group']:
            predicted_gibbs_fed = \
                (reaction.get_norm_cone_sigma() * self._coefficients['Norm Cone Sigma']) + \
                (reaction.get_norm_cone_charton() * self._coefficients['Norm Cone Charton'])

            self._predicted_gibbs_fed.append(predicted_gibbs_fed)

    def calculate_r_squared(self) -> None:
        """
        Calculate R^2 using predicted gibbs FED and measured gibbs FED
        """
        measured_gibbs_fed_list = []
        for reaction in self._reaction_groups['Complete Group']:
            measured_gibbs_fed_list.append(reaction.get_gibbs_free_energy_difference())

        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = linregress(measured_gibbs_fed_list,
                                                                 self._predicted_gibbs_fed)
        # Calculate R-squared
        self._r_squared = r_value ** 2

    def get_r_squared(self):
        return self._r_squared

    def get_coefficients(self):
        return self._coefficients

    def get_reaction_groups(self):
        return self._reaction_groups

    def get_predicted_gibbs_free_energy_difference(self):
        return self._predicted_gibbs_fed

