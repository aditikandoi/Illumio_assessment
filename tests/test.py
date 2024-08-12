import unittest
import os
from solution.solution import Solution
from tempfile import NamedTemporaryFile


class TestSolution(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_validate_file_exists(self):
        with NamedTemporaryFile(delete=True) as temp_file:
            self.solution.validate_file(temp_file.name)

    def test_validate_file_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            self.solution.validate_file('non_existent_file.txt')

    def test_validate_file_format_correct(self):
        self.solution.validate_file_format('dummy_file.csv', '.csv')

    def test_validate_file_format_incorrect(self):
        with self.assertRaises(ValueError):
            self.solution.validate_file_format('dummy_file.txt', '.csv')

    def test_read_lookup_table(self):
        with NamedTemporaryFile('w', delete=False, suffix='.csv') as temp_file:
            temp_file.write('dstport,protocol,tag\n25,tcp,sv_P1\n68,udp,sv_P2\n')
            temp_filename = temp_file.name

        self.solution.read_lookup_table(temp_filename)
        os.remove(temp_filename)
        self.assertEqual(self.solution.lookup_table, {('25', 'tcp'): 'sv_P1', ('68', 'udp'): 'sv_P2'})

    def test_read_lookup_table_invalid_format(self):
        with NamedTemporaryFile('w', delete=False, suffix='.csv') as temp_file:
            temp_file.write('dst_port,protocol,tag\n25,tcp,sv_P1\n68,udp,sv_P2\n')
            temp_filename = temp_file.name

        with self.assertRaises(Exception):
            self.solution.read_lookup_table(temp_filename)

        os.remove(temp_filename)

    def test_process_flow_logs_file(self):
        self.solution.lookup_table = {('25', 'tcp'): 'sv_P1', ('68', 'udp'): 'sv_P2'}

        with NamedTemporaryFile('w', delete=False, suffix='.txt') as temp_file:
            temp_file.write('2 123456789012 eni-abc123 192.0.2.1 203.0.113.1 12345 25 6 10 2000 1609459200 1609459260 ACCEPT OK\n')
            temp_file.write('2 123456789012 eni-abc123 192.0.2.1 203.0.113.1 12345 68 17 10 2000 1609459200 1609459260 ACCEPT OK\n')
            temp_filename = temp_file.name

        self.solution.process_flow_logs_file(temp_filename)
        os.remove(temp_filename)
        self.assertEqual(len(self.solution.tag_count), 2)
        self.assertEqual(self.solution.tag_count['sv_P1'], 1)
        self.assertEqual(self.solution.tag_count['sv_P2'], 1)
        self.assertEqual(len(self.solution.port_protocol_count), 2)
        self.assertEqual(self.solution.port_protocol_count[('25', 'tcp')], 1)
        self.assertEqual(self.solution.port_protocol_count[('68', 'udp')], 1)

    def test_process_flow_logs_file_incorrect_log_entry(self):
        self.solution.lookup_table = {('25', 'tcp'): 'sv_P1'}

        with NamedTemporaryFile('w', delete=False, suffix='.txt') as temp_file:
            temp_file.write('2 123456789012 eni-abc123 192.0.2.1 203.0.113.1 12345 - 25 17 2000 1609459200 1609459260 ACCEPT OK\n')
            temp_filename = temp_file.name

        self.solution.process_flow_logs_file(temp_filename)
        os.remove(temp_filename)
        self.assertEqual(self.solution.tag_count['untagged'], 1)

    def test_create_output_file(self):
        self.solution.tag_count = {'sv_P1': 1, 'sv_P2': 1}
        self.solution.port_protocol_count = {('25', 'tcp'): 1, ('68', 'udp'): 1}

        with NamedTemporaryFile('w', delete=False, suffix='.txt') as temp_file:
            temp_filename = temp_file.name

        self.solution.create_output_file(temp_filename)

        with open(temp_filename, 'r') as file:
            output = file.read()

        os.remove(temp_filename)

        expected_output = """Tag Counts:
Tag         Count       
sv_P1       1           
sv_P2       1           

Port/Protocol Combination Counts:
Port        Protocol    Count       
25          tcp         1           
68          udp         1           
"""
        self.assertEqual(output, expected_output)

    def test_create_output_file_invalid_format(self):
        with self.assertRaises(ValueError):
            self.solution.create_output_file('output.csv')


if __name__ == '__main__':
    unittest.main()
