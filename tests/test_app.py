import unittest
from app import groups, rank_causes


class GraphTests(unittest.TestCase):
    def test_intermediate_node_connects_alerts(self):
        self.assertEqual(groups([('a', 'bridge'), ('b', 'bridge')], {'a', 'b', 'c'}), [{'a', 'b'}, {'c'}])

    def test_upstream_dependency_ranks_first(self):
        edges = [('web', 'api'), ('api', 'db')]
        self.assertEqual(rank_causes(edges, {'web', 'api', 'db'})[0], ('db', 2))


if __name__ == '__main__':
    unittest.main()
