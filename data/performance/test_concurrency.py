import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from mymodule import make_parallel

class TestMakeParallel(unittest.TestCase):

    def test_thread_creation(self):
        """
        Test if the correct number of threads is created based on the number of CPUs.
        """
        mock_func = MagicMock(return_value=10)
        parallel_func = make_parallel(mock_func)
        inputs = [1, 2, 3, 4, 5]
        with patch('os.cpu_count', return_value=4):
            result = parallel_func(inputs)
        mock_func.assert_not_called()
        self.assertEqual(len(result), 4)

    def test_output(self):
        """
        Test if the function returns the correct output given a simple input.
        """
        def func(x):
            return x + 1
        parallel_func = make_parallel(func)
        inputs = [1, 2, 3, 4, 5]
        result = parallel_func(inputs)
        self.assertEqual(result, [2, 3, 4, 5, 6])

if __name__ == '__main__':
    unittest.main()
