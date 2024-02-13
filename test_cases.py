import unittest
from input_file import InputFile
from reaction import Reaction
from training_node import TrainingNode
from lolo_node import LOLONode
from loo_node import LOONode

from main import populate_reactions_from_excel


class BaseTestClass(unittest.TestCase):
    def setUp(self) -> None:
        # Test file attributes
        self.filename = "Test Excel File.xlsx"
        self.sheet_name = "Data"
        self.reaction_id_col_name = "Reaction ID"
        self.ligand_col_name = "Precat. Used"
        self.norm_cone_sigma_col_name = "Norm cone(sigma meta)"
        self.norm_cone_charton_col_name = "Norm cone(charton)"
        self.gibbs_free_energy_difference_col_name = "Measured Gibbs FED"

        # Dummy reaction attributes
        self.test_reaction_id1 = "123"
        self.test_ligand1 = "Copper"
        self.test_norm_cone_sigma1 = 0.5
        self.test_norm_cone_charton1 = 0.5
        self.test_gibbs_free_energy_difference1 = 0.5

        self.test_reaction_id2 = "124"
        self.test_ligand2 = "Hydrogen"
        self.test_norm_cone_sigma2 = 0.7
        self.test_norm_cone_charton2 = 0.7
        self.test_gibbs_free_energy_difference2 = 0.7

        # Test reaction list attributes
        self.test_file_reaction_quantity = 43

        # Training Node Test attributes
        self.complete_group = "Complete Group"
        self.training_group = "Training Group"
        self.complete_group_size = 43
        self.training_group_size = 21

        # LOLOnode attributes
        self.lolo_node_group_size = 8
        self.lolo_node_coefficients = {
            'TrixiePhos G3': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'CataXcium G3': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'P(o-tol)3 G2': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'PCy3 G3': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'PEt3 G3': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'PPh2Me G3': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'PPh3 G2': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435},
            'PtBu3 G3': {'Norm Cone Sigma': 1.9566619155795302, 'Norm Cone Charton': 4.5790650893926435}}
        self.lolo_predicted_gibbs_free_energy = [0.7786730668618804, 0.9263837212105479, 1.6649369929538829,
                                                 2.9482225138504057, 3.286365214287931, 0.7342966159642512,
                                                 2.6049322763582934, 0.6172139955050344, 1.3197097182603348,
                                                 2.3369039907145996, 0.7094126046027993, 2.257710454762916,
                                                 2.361198122735927, 1.2749870940386705, 0.5962977067156248,
                                                 2.5166557366719546, 2.5290454264524933, 0.59923332619484,
                                                 1.281263953578553, 2.372822482724781, 2.2688253370017497,
                                                 0.712905097425459, 1.1008042418069266, 2.1728418452620017,
                                                 0.6124959287739861, 0.5148342661673978, 2.0386221330452345,
                                                 2.0211855930619533, 0.5104308369485748, 1.091388952497102,
                                                 2.154257310591193, 0.6072571895399961, 2.0701468169826125,
                                                 2.3075797216253613, 0.5467591280038651, 2.165037047924019,
                                                 1.1690650893031502, 0.650476788220413, 0.6462032378622862,
                                                 2.7272804629411147, 1.3816937062166765, 2.446663452823074,
                                                 0.768784982588018]
        self.lolo_r_squared = 0.9025163010705327

        # LOOnode attributes
        self.loo_node_group_size = 8
        # self.loo_node_coefficients =
        self.loo_predicted_gibbs_free_energy = [0.7782803543895795, 0.9268962865822685, 1.686828991501714,
                                                2.8513582067151537, 3.3149561681265194, 0.7312861030302764,
                                                2.6141047357713, 0.6144792976530561, 1.3229152727803204,
                                                2.2263910206427893, 0.7091094752049348, 2.2596820417582633,
                                                2.387304497768084, 1.2756855021545312, 0.5938398698547575,
                                                2.4880333354334963, 2.503544287989376, 0.6090123038029569,
                                                1.278233861883772, 2.396070386134545, 2.3006492600879476,
                                                0.7251030372868921, 1.0984350066034339, 2.153946407291519,
                                                0.6180317944291236, 0.5225560446108032, 2.044527925463486,
                                                2.0244241388006037, 0.5163428091875308, 1.0883601671580898,
                                                2.1384963746853023, 0.6115515544677679, 2.095844222860813,
                                                2.2954723130118557, 0.5485757825923206, 2.1745114078652845,
                                                1.1684777166664284, 0.6500807698049357, 0.6431035623755786,
                                                2.753155565256182, 1.390747950797277, 2.2784940793661246,
                                                0.7649654346531868]
        self.loo_r_squared = 0.8862599383953862


class TestInputFile(BaseTestClass):

    def test_input_file(self):
        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        self.assertEqual(self.filename, file.get_file_name())
        self.assertEqual(self.sheet_name, file.get_sheet_name())
        self.assertEqual(self.reaction_id_col_name, file.get_reaction_id_col_name())
        self.assertEqual(self.ligand_col_name, file.get_ligand_col_name())
        self.assertEqual(self.norm_cone_sigma_col_name, file.get_norm_cone_sigma_col_name())
        self.assertEqual(self.norm_cone_charton_col_name, file.get_norm_cone_charton_col_name())
        self.assertEqual(self.gibbs_free_energy_difference_col_name, file.get_gibbs_free_energy_difference_col_name())


class TestReaction(BaseTestClass):

    def test_reaction(self):
        reaction = Reaction(self.test_reaction_id1, self.test_ligand1, self.test_norm_cone_sigma1,
                            self.test_norm_cone_charton1, self.test_gibbs_free_energy_difference1)

        self.assertEqual(self.test_reaction_id1, reaction.get_reaction_id())
        self.assertEqual(self.test_ligand1, reaction.get_ligand())
        self.assertEqual(self.test_norm_cone_sigma1, reaction.get_norm_cone_sigma())
        self.assertEqual(self.test_norm_cone_charton1, reaction.get_norm_cone_charton())
        self.assertEqual(self.test_gibbs_free_energy_difference1, reaction.get_gibbs_free_energy_difference())


class TestMain(BaseTestClass):

    def test_populate_reactions_from_excel(self):
        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        reaction_list = populate_reactions_from_excel(file)

        for reaction_object in reaction_list:
            self.assertIsInstance(reaction_object, Reaction,
                                  msg="Reaction list contains objects that are not Reactions")

        self.assertEqual(len(reaction_list), 43, msg="Reaction list was not fully populated")


class TestTrainingNode(BaseTestClass):

    def test_populate_reaction_groups(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        for reaction_object in training_node.get_reaction_groups()[self.complete_group]:
            self.assertIn(reaction_object, test_reaction_list,
                          msg="Not all reactions are in training node complete set")

        for reaction_object in training_node.get_reaction_groups()[self.training_group]:
            self.assertIn(reaction_object, test_reaction_list, msg="There are reaction objects in training set "
                                                                   "that are not in reaction list")

        self.assertEqual(len(training_node.get_reaction_groups()[self.complete_group]), self.complete_group_size,
                         msg="Training complete group size is incorrect")
        self.assertEqual(len(training_node.get_reaction_groups()[self.training_group]), self.training_group_size,
                         msg="Training training group size is incorrect")

    def test_calculate_training_group_coefficients(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        self.assertTrue(isinstance(training_node.get_coefficients()['Norm Cone Sigma'], float),
                        msg="Training set coefficients are not floats")
        self.assertTrue(isinstance(training_node.get_coefficients()['Norm Cone Charton'], float),
                        msg="Training set coefficients are not floats")

    def test_calculate_predicted_gibbs(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        self.assertEqual(len(training_node.get_predicted_gibbs_free_energy_difference()), self.complete_group_size,
                         msg="Training node predicted gibbs free energy difference list was not fully populated")

    def test_calculate_r_squared(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        self.assertTrue(isinstance(training_node.get_r_squared(), float),
                        msg="Training set r^2 value is not a float")

    class TestLOLONode(BaseTestClass):

        def test_populate_reaction_groups(self):
            file = InputFile(self.filename,
                             self.sheet_name,
                             self.reaction_id_col_name,
                             self.ligand_col_name,
                             self.norm_cone_sigma_col_name,
                             self.norm_cone_charton_col_name,
                             self.gibbs_free_energy_difference_col_name)

            test_reaction_list = populate_reactions_from_excel(file)

            lolo_node = LOLONode(test_reaction_list)

            self.assertEqual(lolo_node.get_reaction_groups().keys(), self.lolo_node_group_size,
                             msg="LOLONode - reactions were not split into 8 groups")

        def test_calculate_lolo_group_coefficients(self):
            file = InputFile(self.filename,
                             self.sheet_name,
                             self.reaction_id_col_name,
                             self.ligand_col_name,
                             self.norm_cone_sigma_col_name,
                             self.norm_cone_charton_col_name,
                             self.gibbs_free_energy_difference_col_name)

            test_reaction_list = populate_reactions_from_excel(file)

            lolo_node = LOLONode(test_reaction_list)

            self.assertDictEqual(lolo_node.get_coefficients(), self.lolo_node_coefficients,
                                 msg="LOLONode coefficients are not correct")

        def test_calculate_predicted_gibbs_free_energy_difference(self):
            file = InputFile(self.filename,
                             self.sheet_name,
                             self.reaction_id_col_name,
                             self.ligand_col_name,
                             self.norm_cone_sigma_col_name,
                             self.norm_cone_charton_col_name,
                             self.gibbs_free_energy_difference_col_name)

            test_reaction_list = populate_reactions_from_excel(file)

            lolo_node = LOLONode(test_reaction_list)

            self.assertListEqual(lolo_node.get_predicted_gibbs_free_energy_difference(),
                                 self.lolo_predicted_gibbs_free_energy,
                                 msg="LOLONODE predicted gibbs free energy difference is not correct")

        def test_calculate_r_squared(self):
            file = InputFile(self.filename,
                             self.sheet_name,
                             self.reaction_id_col_name,
                             self.ligand_col_name,
                             self.norm_cone_sigma_col_name,
                             self.norm_cone_charton_col_name,
                             self.gibbs_free_energy_difference_col_name)

            test_reaction_list = populate_reactions_from_excel(file)

            lolo_node = LOLONode(test_reaction_list)

            self.assertAlmostEqual(lolo_node.get_r_squared(), self.lolo_r_squared)


class TestLOLONode(BaseTestClass):

    def test_populate_reaction_groups(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        for reaction_object in training_node.get_reaction_groups()[self.complete_group]:
            self.assertIn(reaction_object, test_reaction_list,
                          msg="Not all reactions are in training node complete set")

        for reaction_object in training_node.get_reaction_groups()[self.training_group]:
            self.assertIn(reaction_object, test_reaction_list, msg="There are reaction objects in training set "
                                                                   "that are not in reaction list")

        self.assertEqual(len(training_node.get_reaction_groups()[self.complete_group]), self.complete_group_size,
                         msg="Training complete group size is incorrect")
        self.assertEqual(len(training_node.get_reaction_groups()[self.training_group]), self.training_group_size,
                         msg="Training training group size is incorrect")

    def test_calculate_training_group_coefficients(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        self.assertTrue(isinstance(training_node.get_coefficients()['Norm Cone Sigma'], float),
                        msg="Training set coefficients are not floats")
        self.assertTrue(isinstance(training_node.get_coefficients()['Norm Cone Charton'], float),
                        msg="Training set coefficients are not floats")

    def test_calculate_predicted_gibbs(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        self.assertEqual(len(training_node.get_predicted_gibbs_free_energy_difference()), self.complete_group_size,
                         msg="Training node predicted gibbs free energy difference list was not fully populated")

    def test_calculate_r_squared(self):

        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        training_node = TrainingNode(test_reaction_list)

        self.assertTrue(isinstance(training_node.get_r_squared(), float),
                        msg="Training set r^2 value is not a float")


class TestLOONode(BaseTestClass):

    def test_calculate_loo_group_coefficients(self):
        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        loo_node = LOONode(test_reaction_list)

        self.assertEqual(len(loo_node.get_coefficients().keys()), self.complete_group_size,
                         msg="LOONode not all coefficients calculated")

    def test_calculate_predicted_gibbs_free_energy_difference(self):
        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        loo_node = LOONode(test_reaction_list)

        self.assertListEqual(loo_node.get_predicted_gibbs_free_energy_difference(),
                             self.loo_predicted_gibbs_free_energy,
                             msg="LOONode predicted gibbs free energy difference not calculated correctly")

    def test_calculate_r_squared(self):
        file = InputFile(self.filename,
                         self.sheet_name,
                         self.reaction_id_col_name,
                         self.ligand_col_name,
                         self.norm_cone_sigma_col_name,
                         self.norm_cone_charton_col_name,
                         self.gibbs_free_energy_difference_col_name)

        test_reaction_list = populate_reactions_from_excel(file)

        loo_node = LOONode(test_reaction_list)

        self.assertAlmostEqual(loo_node.get_r_squared(), self.loo_r_squared)


if __name__ == '__main__':
    unittest.main()
