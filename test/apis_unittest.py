# To run this unit test:
# python apis_unittest.py
#
# You may need first to install the Python requests package with:
# pip install requests

import requests, unittest

class TestApis(unittest.TestCase):
    baseurl = 'https://genomic-variants.herokuapp.com/api/'

    def test_noSuchRequestMissing(self):
        response = requests.get(TestApis.baseurl)
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], 'no such request /api/')
        self.assertEqual(error['code'], 404)

    def test_noSuchRequestIncorrect(self):
        response = requests.get(TestApis.baseurl + 'badRequest')
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], 'no such request /api/badRequest')
        self.assertEqual(error['code'], 404)

    def test_getGeneNamesStartingWithRequiresParameterMissing(self):
        response = requests.get(TestApis.baseurl + 'getGeneNamesStartingWith')
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], '/api/getGeneNamesStartingWith GET requires parameter prefix')
        self.assertEqual(error['code'], 400)

    def test_getGenesNamedRequiresParameterMissing(self):
        response = requests.get(TestApis.baseurl + 'getGenesNamed')
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], '/api/getGenesNamed GET requires parameter name')
        self.assertEqual(error['code'], 400)

    def test_getGeneNamesStartingWithRequiresParameterIncorrect(self):
        response = requests.get(TestApis.baseurl + 'getGeneNamesStartingWith?p=xy')
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], '/api/getGeneNamesStartingWith GET requires parameter prefix')
        self.assertEqual(error['code'], 400)

    def test_getGenesNamedRequiresParameterIncorrect(self):
        response = requests.get(TestApis.baseurl + 'getGenesNamed?n=XYLT1')
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], '/api/getGenesNamed GET requires parameter name')
        self.assertEqual(error['code'], 400)

    def test_getGeneNamesStartingWithParameterTooShort(self):
        response = requests.get(TestApis.baseurl + 'getGeneNamesStartingWith?prefix=')
        json = response.json()
        error = json['error']
        self.assertEqual(error['message'], '/api/getGeneNamesStartingWith GET parameter prefix requires at least 1 characters')
        self.assertEqual(error['code'], 400)

    def test_getGeneNamesStartingWithZeroHits(self):
        response = requests.get(TestApis.baseurl + 'getGeneNamesStartingWith?prefix=xyz')
        json = response.json()
        data = json['data']
        names = data['names']
        self.assertEqual(len(names), 0)

    def test_getGeneNamesStartingWitPositiveHits(self):
        response = requests.get(TestApis.baseurl + 'getGeneNamesStartingWith?prefix=xy')
        json = response.json()
        data = json['data']
        names = data['names']
        for name in names:
            self.assertEqual(name[:2].lower(), 'xy')

    def test_getGenesNamedZeroHits(self):
        response = requests.get(TestApis.baseurl + 'getGenesNamed?name=xyz')
        json = response.json()
        data = json['data']
        self.assertEqual(len(data), 0)

    def test_getGenesNamedPositiveHits(self):
        response = requests.get(TestApis.baseurl + 'getGenesNamed?name=XYLT1')
        json = response.json()
        data = json['data']
        for gene in data:
            self.assertEqual(gene['name'], 'XYLT1')

if __name__ == '__main__':
    unittest.main()
