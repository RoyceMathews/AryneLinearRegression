import pandas as pd
from sklearn import linear_model
from scipy.stats import linregress


class LOONode:
    def __init__(self, reactions: list):
        self._reactions = reactions.copy()
        self._coefficients = {}
        self.calculate_loo_group_coefficients()
        self._predicted_gibbs_fed = []
        self.calculate_predicted_gibbs_free_energy_difference()
        self._r_squared = None
        self.calculate_r_squared()

    def calculate_loo_group_coefficients(self) -> None:
        """
        Calculates linear regression coefficients. Leave one reaction out per experiment
        """

        # All ligands except 1
        for reaction_leave_out in self._reactions:
            # Initialize/clear dict
            independent_var_dict = {'norm_cone_sigma': [], 'norm_cone_charton': []}
            dependant_var_dict = {'gibbs_free_energy_difference': []}

            # Populate df
            for reaction in self._reactions:
                if reaction != reaction_leave_out:
                    independent_var_dict['norm_cone_sigma'].append(reaction.get_norm_cone_sigma())
                    independent_var_dict['norm_cone_charton'].append(reaction.get_norm_cone_charton())
                    dependant_var_dict['gibbs_free_energy_difference'].append(
                        reaction.get_gibbs_free_energy_difference())

            independent_var_df = pd.DataFrame(independent_var_dict)
            dependant_var_df = pd.DataFrame(dependant_var_dict)

            lin_reg = linear_model.LinearRegression()
            lin_reg.fit(independent_var_df, dependant_var_df)
            coefficients = lin_reg.coef_.tolist()

            # Key = ligand left out
            self._coefficients[reaction_leave_out] = {'Norm Cone Sigma': None, 'Norm Cone Charton': None}
            self._coefficients[reaction_leave_out]['Norm Cone Sigma'] = coefficients[0][0]
            self._coefficients[reaction_leave_out]['Norm Cone Charton'] = coefficients[0][1]

    def calculate_predicted_gibbs_free_energy_difference(self) -> None:
        """
        Calculate predicted gibbs FED.
        Multiply respective coefficients by reaction left out norm cone sigma/charton.
        Combine all predicted gibbs FED lists
        """
        for reaction_left_out in self._coefficients.keys():
            predicted_gibbs_fed = \
                (reaction_left_out.get_norm_cone_sigma() * self._coefficients[reaction_left_out]['Norm Cone Sigma']) + \
                (reaction_left_out.get_norm_cone_charton() * self._coefficients[reaction_left_out]['Norm Cone Charton'])

            self._predicted_gibbs_fed.append(predicted_gibbs_fed)

    def calculate_r_squared(self) -> None:
        """
        Calculate R^2 using predicted gibbs FED and measured gibbs FED
        """
        measured_gibbs_fed_list = []
        for reaction in self._reactions:
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

    def get_predicted_gibbs_free_energy_difference(self):
        return self._predicted_gibbs_fed
