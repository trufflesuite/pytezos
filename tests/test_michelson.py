import os
import simplejson as json
from unittest import TestCase
from parameterized import parameterized

from pytezos.michelson import MichelsonParser
from pytezos.rpc.contract import parse_schema, decode_data


def get_data(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(path) as f:
        return f.read()


class TestMichelsonParser(TestCase):

    def setUp(self):
        self.parser = MichelsonParser()
        self.maxDiff = None

    @parameterized.expand([
        ('script/sample_0.tz', 'script/sample_0.json'),
        ('script/sample_1.tz', 'script/sample_1.json'),
        ('script/sample_2.tz', 'script/sample_2.json'),
    ])
    def test_parser(self, source_name, expected_name):
        source = get_data(source_name)
        res = self.parser.parse(source)
        expected = json.loads(get_data(expected_name))
        self.assertListEqual(expected, res)

    def test_schema_parsing(self):
        script = json.loads(get_data('storage/sample_0.json'))
        storage = next(s for s in script['code'] if s['prim'] == 'storage')
        schema = parse_schema(storage)
        data = decode_data(script['storage'], schema)
