import os, sys, json, unittest
import pandas as pd
ROOT=os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,ROOT)
from src.entity_resolution import normalize_name, compare_records
from src.anomaly_detection import flag_duplicate_payments, flag_unusual_amounts
from src.graph_engine import build_entity_graph

class LedgerLensTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT,"data/synthetic/business_records.json")) as f:
            cls.records=json.load(f)
        cls.tx=pd.read_csv(os.path.join(ROOT,"data/synthetic/transactions.csv"))
    def test_01_suffix_normalization(self):
        self.assertEqual(normalize_name("ABC Technologies Pvt Ltd"),"abc technologies")
    def test_02_same_registration_match(self):
        r=compare_records(self.records[0],self.records[1])
        self.assertEqual(r["recommendation"],"REVIEW_HIGH_SIMILARITY")
    def test_03_identifier_conflict_override(self):
        r=compare_records(self.records[3],self.records[4])
        self.assertEqual(r["recommendation"],"INVESTIGATE_IDENTIFIER_CONFLICT")
    def test_04_no_automatic_merge(self):
        self.assertFalse(compare_records(self.records[0],self.records[1])["automatic_merge"])
    def test_05_empty_name_safe(self):
        self.assertEqual(normalize_name(""),"")
    def test_06_duplicate_reference_flag(self):
        out=flag_duplicate_payments(self.tx)
        self.assertTrue(out.loc[out.transaction_reference=="NEFT-1003","duplicate_reference"].all())
    def test_07_unique_reference_not_duplicate(self):
        out=flag_duplicate_payments(self.tx)
        self.assertFalse(out.loc[out.transaction_reference=="NEFT-1001","duplicate_reference"].any())
    def test_08_amount_column_preserved(self):
        out=flag_unusual_amounts(self.tx)
        self.assertIn("amount",out.columns)
    def test_09_graph_nodes(self):
        g=build_entity_graph(self.records,self.tx.to_dict("records"))
        self.assertIn("R001",g.nodes)
        self.assertIn("T001",g.nodes)
    def test_10_graph_edges(self):
        g=build_entity_graph(self.records,self.tx.to_dict("records"))
        self.assertTrue(g.has_edge("T001","R001"))
    def test_11_conflicting_ids_are_not_auto_merged(self):
        r=compare_records(self.records[3],self.records[4])
        self.assertFalse(r["automatic_merge"])
    def test_12_pair_score_is_bounded(self):
        r=compare_records(self.records[0],self.records[1])
        self.assertGreaterEqual(r["score"],0)
        self.assertLessEqual(r["score"],1)

if __name__=="__main__":
    unittest.main()
