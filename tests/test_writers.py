"""Tests for SSSOM writers."""
import json
import os
import unittest

from jsonasobj2 import JsonObj

from sssom.parsers import parse_sssom_json, parse_sssom_rdf, parse_sssom_table
from sssom.writers import write_fhir_json, write_json, write_owl, write_rdf, write_table
from tests.constants import data_dir as test_data_dir
from tests.constants import test_out_dir


class TestWrite(unittest.TestCase):
    """A test case for SSSOM writers."""

    def setUp(self) -> None:
        """Set up the test case with a basic SSSOM example."""
        self.msdf = parse_sssom_table(f"{test_data_dir}/basic.tsv")
        # self.msdf = read_sssom_table(f"{test_data_dir}/basic-simple.tsv")
        self.mapping_count = 141  # 141 for basic.tsv

    def test_write_sssom_dataframe(self):
        """Test writing as a dataframe."""
        tmp_path = os.path.join(test_out_dir, "test_write_sssom_dataframe.tsv")
        with open(tmp_path, "w") as tmp_file:
            write_table(self.msdf, tmp_file)
        msdf = parse_sssom_table(tmp_path)
        self.assertEqual(
            len(msdf.df),
            self.mapping_count,
            f"{tmp_file} has the wrong number of mappings.",
        )

    def test_write_sssom_rdf(self):
        """Test writing as RDF."""
        path_1 = os.path.join(test_out_dir, "test_write_sssom_rdf.rdf")
        with open(path_1, "w") as file:
            write_rdf(self.msdf, file)
        msdf = parse_sssom_rdf(path_1, self.msdf.prefix_map)
        self.assertEqual(
            len(msdf.df),
            self.mapping_count,
            f"{path_1} has the wrong number of mappings.",
        )

        # TODO this test doesn't make sense
        path_2 = os.path.join(test_out_dir, "test_write_sssom_rdf.rdf.tsv")
        with open(path_2, "w") as file:
            write_table(self.msdf, file)

    def test_write_sssom_json(self):
        """Test writing as JSON."""
        path = os.path.join(test_out_dir, "test_write_sssom_json.json")
        with open(path, "w") as file:
            write_json(self.msdf, file)
        msdf = parse_sssom_json(path)
        self.assertEqual(
            len(msdf.df),
            self.mapping_count,
            f"{path} has the wrong number of mappings.",
        )

    def test_write_sssom_fhir(self):
        """Test writing as FHIR ConceptMap JSON."""
        path = os.path.join(test_out_dir, "test_write_sssom_fhir.json")
        with open(path, "w") as file:
            write_fhir_json(self.msdf, file)
        # todo: @Joe: after implementing reader/importer, change this to `msdf = parse_sssom_fhir_json()`
        with open(path, "r") as file:
            d: JsonObj = json.load(file)
        # todo: @Joe: What else is worth checking?
        self.assertEqual(
            len(d["group"][0]["element"]),
            self.mapping_count,
            f"{path} has the wrong number of mappings.",
        )

    def test_write_sssom_owl(self):
        """Test writing as OWL."""
        tmp_file = os.path.join(test_out_dir, "test_write_sssom_owl.owl")
        with open(tmp_file, "w") as file:
            write_owl(self.msdf, file)
        # FIXME this test doesn't test anything
        # TODO implement "read_owl" function
        self.assertEqual(1, 1)
