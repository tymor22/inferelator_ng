"""
Test workflow logic outline using completely
artificial stubs for dependancies.
"""

import unittest
from .. import workflow
import os

my_dir = os.path.dirname(__file__)

class StubWorkflow(workflow.WorkflowBase):

    """
    Artificial work flow for logic testing.
    """

    cd_called = False
    test_case = None

    def run(self):
        self.get_data()

    def compute_common_data(self):
        cd_called = True

    def get_priors(self):
        return [StubPrior(1), StubPrior(2)]

    def get_bootstraps(self):
        return [StubBootstrap("A"), StubBootstrap("B")]

    def emit_results(self, priors):
        # check that everything got initialized properly
        assert self.exp_mat is not None
        assert self.meta_data is not None
        assert self.tf_names is not None
        assert self.priors_data is not None
        assert self.gold_standard is not None
        test = self.test_case
        idents = [1, 2]
        names = ["A", "B"]
        test.assertEqual([p.ident for p in priors], idents)
        for p in priors:
            test.assertEqual(p.names, names)

class StubBootstrap(object):

    def __init__(self, name):
        self.name = name

class StubPrior(object):

    """
    Completely artificial prior object shell implementation.
    """

    def __init__(self, ident):
        self.ident = ident

    names = []

    def run_bootstrap(self, workflow, bootstrap_parameters):
        self.names = self.names + [bootstrap_parameters.name]

    bootstrap_results = None

    def combine_bootstrap_results(self, workflow, results):
        self.bootstrap_results = results

class TestWorkflowStub(unittest.TestCase):

    def test_stub(self):
        # create and configure the work flow
        work = StubWorkflow()
        work.input_dir = os.path.join(my_dir, "../../data/dream4")
        work.test_case = self
        # run the workflow (validation tests in emit_results)
        work.run()

    def test_stub_without_metadata(self):
        # create and configure the work flow
        work = StubWorkflow()
        work.input_dir = os.path.join(my_dir, "../../data/dream4_no_metadata_for_test_purposes")
        work.test_case = self
        # run the workflow (validation tests in emit_results)
        work.run()
        self.assertEqual(work.meta_data.shape, (421, 5))
        self.assertEqual(work.meta_data.columns.tolist(), ['condName', 'del.t', 'is1stLast', 'isTs', 'prevCol'])

    def test_stub_without_gold_standard(self):
        # create and configure the work flow
        work = StubWorkflow()
        work.priors_file = "priors.tsv"
        work.input_dir = os.path.join(my_dir, "../../data/dream4_no_gs_for_test_purposes")
        work.test_case = self
        # run the workflow (validation tests in emit_results)
        work.run()
        self.assertEqual(work.gold_standard, None)
