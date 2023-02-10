import rpy2

import rpy2.robjects as ro

from django.test import TestCase
from forsys.parse_forsys_output import ForsysScenarioSetOutput


class TestForsysScenarioSetOutput(TestCase):
    def test_parses_output(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()
        parsed_output = ForsysScenarioSetOutput(
            raw_forsys_output, ["p1", "p2"],
            None, None, "proj_id", "area", "cost")

        scenarios = parsed_output.scenarios

        self.assertDictEqual(scenarios,
                             {
                                 'p1:1 p2:1': {
                                     'priority_weights': {'p1': 1, 'p2': 1},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.1},
                                          'total_score': 0.6,
                                          'rank': 1},
                                         {'id': 2,
                                          'weighted_priority_scores': {
                                              'p1': 0.1, 'p2': 0.4},
                                          'total_score': 0.5,
                                          'rank': 2},
                                         {'id': 3,
                                          'weighted_priority_scores': {
                                              'p1': 0.3, 'p2': 0.1},
                                          'total_score': 0.4,
                                          'rank': 3},
                                     ],
                                     'cumulative_ranked_project_area': [10, 21, 33],
                                     'cumulative_ranked_project_cost': [500, 1100, 1900]
                                 },
                                 'p1:1 p2:2': {
                                     'priority_weights': {'p1': 1, 'p2': 2},
                                     'ranked_projects': [
                                         {'id': 2,
                                          'weighted_priority_scores': {
                                              'p1': 0.1, 'p2': 0.8},
                                          'total_score': 0.9,
                                          'rank': 1},
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.2},
                                          'total_score': 0.7,
                                          'rank': 2},
                                         {'id': 3,
                                          'weighted_priority_scores': {
                                              'p1': 0.3, 'p2': 0.2},
                                          'total_score': 0.5,
                                          'rank': 3},
                                     ],
                                     'cumulative_ranked_project_area': [11, 21, 33],
                                     'cumulative_ranked_project_cost': [600, 1100, 1900]
                                 }
                             })

    def test_fails_if_priority_ordering_is_wrong(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()

        with self.assertRaises(Exception) as context:
            # priority order is ["p2", "p1"] instead of ["p1", "p2"]
            ForsysScenarioSetOutput(
                raw_forsys_output, ["p2", "p1"],
                None, None, "proj_id", "area", "cost")

        self.assertEqual(str(context.exception),
                         'header, Pr_1_p2, is not a forsys output header')

    def test_fails_if_proj_id_header_is_wrong(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()

        with self.assertRaises(Exception) as context:
            # project id is "project_id" instead of "proj_id"
            ForsysScenarioSetOutput(
                raw_forsys_output, ["p1", "p2"],
                None, None, "project_id", "area", "cost")

        self.assertEqual(str(context.exception),
                         'header, project_id, is not a forsys output header')

    def test_fails_if_area_header_is_wrong(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()

        with self.assertRaises(Exception) as context:
            # area header is "area_ha" instead of "area"
            ForsysScenarioSetOutput(
                raw_forsys_output, ["p1", "p2"],
                None, None, "proj_id", "area_ha", "cost")

        self.assertEqual(
            str(context.exception),
            'header, ETrt_area_ha, is not a forsys output header')

    def test_fails_if_cost_header_is_wrong(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()

        with self.assertRaises(Exception) as context:
            # cost header is "c" instead of "cost"
            ForsysScenarioSetOutput(
                raw_forsys_output, ["p1", "p2"],
                None, None, "proj_id", "area", "c")

        self.assertEqual(
            str(context.exception),
            'header, ETrt_c, is not a forsys output header')

    def test_limits_area(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()
        parsed_output = ForsysScenarioSetOutput(
            raw_forsys_output, ["p1", "p2"],
            25, None, "proj_id", "area", "cost")

        scenarios = parsed_output.scenarios

        self.assertDictEqual(scenarios,
                             {
                                 'p1:1 p2:1': {
                                     'priority_weights': {'p1': 1, 'p2': 1},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.1},
                                          'total_score': 0.6,
                                          'rank': 1},
                                         {'id': 2,
                                          'weighted_priority_scores': {
                                              'p1': 0.1, 'p2': 0.4},
                                          'total_score': 0.5,
                                          'rank': 2},
                                     ],
                                     'cumulative_ranked_project_area': [10, 21],
                                     'cumulative_ranked_project_cost': [500, 1100]
                                 },
                                 'p1:1 p2:2': {
                                     'priority_weights': {'p1': 1, 'p2': 2},
                                     'ranked_projects': [
                                         {'id': 2,
                                          'weighted_priority_scores': {
                                              'p1': 0.1, 'p2': 0.8},
                                          'total_score': 0.9,
                                          'rank': 1},
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.2},
                                          'total_score': 0.7,
                                          'rank': 2},
                                     ],
                                     'cumulative_ranked_project_area': [11, 21],
                                     'cumulative_ranked_project_cost': [600, 1100]
                                 }
                             })

    def test_limits_area_by_skipping_top_project(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()
        parsed_output = ForsysScenarioSetOutput(
            raw_forsys_output, ["p1", "p2"],
            10, None, "proj_id", "area", "cost")

        scenarios = parsed_output.scenarios

        self.assertDictEqual(scenarios,
                             {
                                 'p1:1 p2:1': {
                                     'priority_weights': {'p1': 1, 'p2': 1},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.1},
                                          'total_score': 0.6,
                                          'rank': 1},
                                     ],
                                     'cumulative_ranked_project_area': [10],
                                     'cumulative_ranked_project_cost': [500]
                                 },
                                 'p1:1 p2:2': {
                                     'priority_weights': {'p1': 1, 'p2': 2},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.2},
                                          'total_score': 0.7,
                                          'rank': 2},
                                     ],
                                     'cumulative_ranked_project_area': [10],
                                     'cumulative_ranked_project_cost': [500]
                                 }
                             })

        
    def test_limits_cost(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()
        parsed_output = ForsysScenarioSetOutput(
            raw_forsys_output, ["p1", "p2"],
            None, 1200, "proj_id", "area", "cost")

        scenarios = parsed_output.scenarios

        self.assertDictEqual(scenarios,
                             {
                                 'p1:1 p2:1': {
                                     'priority_weights': {'p1': 1, 'p2': 1},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.1},
                                          'total_score': 0.6,
                                          'rank': 1},
                                         {'id': 2,
                                          'weighted_priority_scores': {
                                              'p1': 0.1, 'p2': 0.4},
                                          'total_score': 0.5,
                                          'rank': 2},
                                     ],
                                     'cumulative_ranked_project_area': [10, 21],
                                     'cumulative_ranked_project_cost': [500, 1100]
                                 },
                                 'p1:1 p2:2': {
                                     'priority_weights': {'p1': 1, 'p2': 2},
                                     'ranked_projects': [
                                         {'id': 2,
                                          'weighted_priority_scores': {
                                              'p1': 0.1, 'p2': 0.8},
                                          'total_score': 0.9,
                                          'rank': 1},
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.2},
                                          'total_score': 0.7,
                                          'rank': 2},
                                     ],
                                     'cumulative_ranked_project_area': [11, 21],
                                     'cumulative_ranked_project_cost': [600, 1100]
                                 }
                             })

    def test_limits_cost_by_skipping_top_project(self) -> None:
        raw_forsys_output = self._get_raw_forsys_output()
        parsed_output = ForsysScenarioSetOutput(
            raw_forsys_output, ["p1", "p2"],
            None, 550, "proj_id", "area", "cost")

        scenarios = parsed_output.scenarios

        self.assertDictEqual(scenarios,
                             {
                                 'p1:1 p2:1': {
                                     'priority_weights': {'p1': 1, 'p2': 1},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.1},
                                          'total_score': 0.6,
                                          'rank': 1}
                                     ],
                                     'cumulative_ranked_project_area': [10],
                                     'cumulative_ranked_project_cost': [500]
                                 },
                                 'p1:1 p2:2': {
                                     'priority_weights': {'p1': 1, 'p2': 2},
                                     'ranked_projects': [
                                         {'id': 1,
                                          'weighted_priority_scores': {
                                              'p1': 0.5, 'p2': 0.2},
                                          'total_score': 0.7,
                                          'rank': 2},
                                     ],
                                     'cumulative_ranked_project_area': [10],
                                     'cumulative_ranked_project_cost': [500]
                                 }
                             })
    
    def _convert_dictionary_of_lists_to_rdf(
            self, lists: dict) -> ro.vectors.DataFrame:
        data = {}
        for key in lists.keys():
            if len(lists[key]) == 0:
                continue
            el = lists[key][0]
            if isinstance(el, str):
                data[key] = ro.StrVector(lists[key])
            elif isinstance(el, float):
                data[key] = ro.FloatVector(lists[key])
            elif isinstance(el, int):
                data[key] = ro.IntVector(lists[key])

        rdf = ro.vectors.DataFrame(data)
        return rdf

    def _get_raw_forsys_output(self) -> ro.vectors.ListVector:
        data = {
            "proj_id": [1, 2, 3, 2, 1, 3],
            "Pr_1_p1": [1, 1, 1, 1, 1, 1],
            "Pr_2_p2": [1, 1, 1, 2, 2, 2],
            "ETrt_p1": [0.5, 0.1, 0.3, 0.1, 0.5, 0.3],
            "ETrt_p2": [0.1, 0.4, 0.1, 0.4, 0.1, 0.1],
            "treatment_rank": [1, 2, 3, 1, 2, 3],
            "ETrt_area": [10, 11, 12, 11, 10, 12],
            "ETrt_cost": [500, 600, 800, 600, 500, 800],
        }
        raw_forsys_output = ro.vectors.ListVector(
            {"stand_output": self._convert_dictionary_of_lists_to_rdf({}),
             "project_output": self._convert_dictionary_of_lists_to_rdf(data),
             "subset_output": self._convert_dictionary_of_lists_to_rdf({})})
        return raw_forsys_output
