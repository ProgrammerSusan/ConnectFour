import unittest
import client

class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response({"column": 1}), '{"column": 1}\n')

if __name__ == '__main__':
  unittest.main()
