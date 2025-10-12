import pandas as pd
import unittest

from ecasd_enrollment.data.kindergarten import get_births_five_years_ago_and_kindergartener_enrollments, get_ratio_of_births_to_kindergarten_enrollments, get_predicted_ratio_of_births_to_kindergarten_enrollments


class TestKindergarten(unittest.TestCase):
    def test_get_enrollments_and_births_five_years_ago(self):
        result = get_births_five_years_ago_and_kindergartener_enrollments(2018, 2020)

        self.assertEqual(3, len(result))
        self.assertEqual(764, result.xs(2018)["Kindergarteners"])
        self.assertEqual(1002, result.xs(2018)["Births Five Years Ago"])
        self.assertEqual(763, result.xs(2019)["Kindergarteners"])
        self.assertEqual(1080, result.xs(2019)["Births Five Years Ago"])
        self.assertTrue(pd.isna(result.xs(2020)["Kindergarteners"]))
        self.assertEqual(1029, result.xs(2020)["Births Five Years Ago"])

    def test_get_ratio_of_births_to_kindergarten_enrollments(self):
        result = get_ratio_of_births_to_kindergarten_enrollments(2015, 2018)

        self.assertEqual(4, len(result))
        self.assertAlmostEqual(0.72927, result.loc[2015], 4)
        self.assertAlmostEqual(0.78014, result.loc[2016], 4)
        self.assertAlmostEqual(0.69961, result.loc[2017], 4)
        self.assertAlmostEqual(0.76247, result.loc[2018], 4)

    def test_get_predicted_ratio_of_births_to_kindergarten_enrollments(self):
        result = get_predicted_ratio_of_births_to_kindergarten_enrollments(2016, 2019)

        self.assertEqual(4, len(result))
        self.assertAlmostEqual(0.73388, result.loc[2016], 4)
        self.assertAlmostEqual(0.74633, result.loc[2017], 4)
        self.assertAlmostEqual(0.73634, result.loc[2018], 4)
        self.assertAlmostEqual(0.74741, result.loc[2019], 4)


if __name__ == '__main__':
    unittest.main()
