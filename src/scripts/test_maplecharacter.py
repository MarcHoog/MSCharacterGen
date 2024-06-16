import unittest
from nx import NX
from maplecharacter import offset_calculator

class TestMapleCharacter(unittest.TestCase):
    
    
    character = NX('./content/Character.nx')
    char_root = character.get_node(0)
    char_body = char_root.resolve('00002000.img/stand1/0/body')
    char_arm = char_root.resolve('00002000.img/stand1/0/arm')
    char_head = char_root.resolve('00012000.img/stand1/0/head')
    
    #def test_calculate_offset_body(self):
    #    sprite = MaplestorySprite(self.char_body)
    #    offset = sprite.calculate_offset()
    #    self.assertEqual(offset, (-16, -31))
        
    def test_calculate_offset_arm(self):
        offsets = offset_calculator([self.char_body, self.char_arm, self.char_head])

if __name__ == "__main__":
    unittest.main()