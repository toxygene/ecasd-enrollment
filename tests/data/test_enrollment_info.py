from ecasd_enrollment.data.enrollment_info import get_yearly_share_per_grade_by_school, get_predicted_yearly_share_per_grade_by_school, \
    get_students_per_grade_by_year_and_school, get_students_per_grade_by_year
from unittest import TestCase


class TestEnrollmentInfo(TestCase):
    def test_get_yearly_share_per_grade_by_school(self):
        share = get_yearly_share_per_grade_by_school(2014, 2015)

        self.assertEqual(144, len(share))

        self.assertAlmostEqual(0.07277, share.xs((2014, "K", "Flynn"))["Share"], 4)
        self.assertAlmostEqual(0.10869, share.xs((2014, "4", "Sherman"))["Share"], 4)
        self.assertAlmostEqual(0.09176, share.xs((2015, "1", "Manz"))["Share"], 4)

    def test_get_predicted_yearly_share_per_grade_by_school(self):
        prediction = get_predicted_yearly_share_per_grade_by_school(2012, 2013)

        self.assertEqual(144, len(prediction))

        self.assertAlmostEqual(0.06710, prediction.xs((2012, "K", "Flynn"))["Predicted Share"], 4)
        self.assertAlmostEqual(0.09008, prediction.xs((2013, "5", "Davey"))["Predicted Share"], 4)

    def test_get_students_per_grade_by_year_and_school(self):
        students_per_year_and_school_and_grade = get_students_per_grade_by_year_and_school(2012, 2013)

        self.assertEqual(144, len(students_per_year_and_school_and_grade))
        self.assertEqual(55, students_per_year_and_school_and_grade.xs((2012, "Flynn", "K"))["Students"])
        self.assertEqual(63, students_per_year_and_school_and_grade.xs((2012, "Putnam Heights", "3"))["Students"])
        self.assertEqual(33, students_per_year_and_school_and_grade.xs((2013, "Longfellow", "5"))["Students"])

    def test_get_students_per_grade_by_year(self):
        students_per_year_and_grade = get_students_per_grade_by_year(2012, 2013)

        self.assertEqual(12, len(students_per_year_and_grade))
        self.assertEqual(824, students_per_year_and_grade.xs((2012, "K"))["Students"])
        self.assertEqual(730, students_per_year_and_grade.xs((2013, "3"))["Students"])
