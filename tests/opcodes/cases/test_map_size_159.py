from unittest import TestCase

from tests import abspath

from pytezos.repl.interpreter import Interpreter
from pytezos.michelson.converter import michelson_to_micheline
from pytezos.repl.parser import parse_value


class OpcodeTestmap_size_159(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.i = Interpreter(debug=True)
        
    def test_opcode_map_size_159(self):
        res = self.i.execute(f'INCLUDE "{abspath("opcodes/contracts/map_size.tz")}"')
        self.assertTrue(res['success'])
        
        res = self.i.execute('RUN { Elt "a" 1 ; Elt "b" 2 ; Elt "c" 3 ;     Elt "d" 4 ; Elt "e" 5 ; Elt "f" 6 } 111')
        self.assertTrue(res['success'])
        
        type_expr = self.i.ctx.stack[0].type_expr['args'][1]
        expected_expr = michelson_to_micheline('6')
        expected_val = parse_value(expected_expr, type_expr)
        self.assertEqual(expected_val, self.i.ctx.stack[0]._val[1])