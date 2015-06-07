import unittest
from diff import Diff

class TestDiff(unittest.TestCase):

    def setUp(self):
        self.old_dict = {"dict1":{"dict2": {"x":"A","z":"d"}}}
        self.new_dict = {"dict1":{"dict2": {"x":"C","y":"B"}}}
        self.old_flat = {"a":"a", "z":"z"}
        self.new_flat = {"a":"f", "b":"b"}
        self.old = {"result":{
                            "first name":"bob",
                            "last name":"segar",
                            "phone":{"home":"615-509-9910",
                                    "mobile":"615-555-4444"},
                            "title":["programmer", "dev-ops"],
                            "salary":{"starting":40000,
                                        "20150303":45000}}}

        self.new = {"result":{
                            "first name":"bob",
                            "last name":"segar",
                            "phone":{"mobile":"615-555-4444"},
                            "title":["python developer", "dev-ops"],
                            "salary":{"starting":40000,
                                        "20150303":45000},
                            "clearance":"level Z"}}

        self.d = Diff()

    def test_added_logic(self):
        result = self.d.added(self.old_dict, self.new_dict)
        expected = [{"operation": "ADDED", "field": "dict1.dict2.y", "new": "B"}]
        self.assertEqual(result, expected)

    def test_added_flat_dict(self):
        result = self.d.added(self.old_flat, self.new_flat)
        expected = [{'field': 'b', 'operation': 'ADDED', 'new': 'b'}]
        self.assertEqual(result, expected)

    def test_modified_logic(self):
        result = self.d.modified(self.old_dict, self.new_dict)
        expected = [{"operation": "MODIFIED", "field": "dict1.dict2.x", "old": "A", "new": "C"}]
        self.assertEqual(result, expected)

    def test_modified_flat_dict(self):
        result = self.d.modified(self.old_flat, self.new_flat)
        expected = [{'field': 'a', 'operation': 'MODIFIED', 'new': 'f', 'old': 'a'}]
        self.assertEqual(result, expected)

    def test_deleted_logic(self):
        result = self.d.deleted(self.old_dict, self.new_dict)
        expected = [{"operation": "DELETED", "field": "dict1.dict2.z", "old": "d"}]
        self.assertEqual(result, expected)

    def test_deleted_flat_dict(self):
        result = self.d.deleted(self.old_flat, self.new_flat)
        expected = [{'field': 'z', 'operation': 'DELETED', 'old': 'z'}]
        self.assertEqual(result, expected)

    def test_difference_logic(self):
        result = self.d.combine_results(self.old_dict, self.new_dict)
        expected = [
            {"operation": "ADDED", "field": "dict1.dict2.y", "new": "B"},
            {"operation": "MODIFIED", "field": "dict1.dict2.x", "old": "A", "new": "C"},
            {"operation": "DELETED", "field": "dict1.dict2.z", "old": "d"}
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
