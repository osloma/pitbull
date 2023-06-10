import unittest
from ark_download import download_file

class TestArkDownload(unittest.TestCase):
    def test_download_file(self):
      """
        Test if download_file function downloads a file from a specified URL and saves it to the local directory with the 
        specified filename. The test checks if the downloaded file contains the word "example".
        
        Input:
        url: string, the URL of the file to download
        filename: string, the name of the file to save
        
        Output:
        None
        """
        url = "https://example.com/file.txt"
        filename = "test.txt"
        download_file(url, filename)
        with open(filename) as f:
            contents = f.read()
        self.assertIn("example", contents)

if __name__ == '__main__':
    unittest.main()
