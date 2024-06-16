from pygame.math import Vector2
from typing import Dict, Any

class Character:
    
    
    def __init__(self, nx, body='00002000.img', head='00012000.img'):
        
        stand = ''
        
        self.nx = nx
        self.root = nx.get_node(0)
        
        self.body = body
        self.head = head
        
        self.sprites = {
            'char_body': self.root.resolve(f'{self.body}/stand1/0/body'),
            'char_arm': self.root.resolve(f'{self.body}/stand1/0/arm'),
            'char_head': self.root.resolve(f'{self.head}/stand1/0/head'),
        }

        self.offsets: Dict[str, Vector2] = {}

    def calculate_offsets(self):
        flip = False
        offset = Vector2(0,0)   
        origin = Vector2(0,0)   
        brow = Vector2(0,0)   
        
        neck = Vector2(0,0)   
        body_neck = Vector2(0,0)   
        head_neck = Vector2(0,0)   
        
        navel = Vector2(0,0)   
        body_navel = Vector2(0,0)   
        arm_navel = Vector2(0,0)
        
        hand = Vector2(0,0)   
        body_hand = Vector2(0,0)   
        arm_hand = Vector2(0,0)   

        for k, sprite in self.sprites.items():
            offset = Vector2(0,0)
            
            if 'origin' in sprite:
                flip = True
                origin.x = -sprite['origin'].x         
                origin.y = -sprite['origin'].y

            if 'neck' in sprite['map']:
                neck.x = -sprite['map']['neck'].x * int(flip)
                neck.y = -sprite['map']['neck'].y
                
                if sprite.name == 'body':
                      body_neck = neck.copy()
                elif sprite.name == 'head':
                      head_neck = neck.copy()
                
            if 'brow' in sprite['map']:
                brow.x = -sprite['map']['brow'].x * int(flip)
                brow.y = -sprite['map']['brow'].y
                if sprite.name == 'head':
                      head_brow = brow.copy()
                      
                offset.x = (origin.x + head_neck.x - body_neck.x - head_brow.x + brow.x)
                offset.y = (origin.y + head_neck.y - body_neck.y - head_brow.y + brow.y)


            if 'hand' in sprite['map']:
                hand.x = -sprite['map']['hand'].x * int(  flip)
                hand.y = -sprite['map']['hand'].y
                if sprite.name == 'arm':
                      arm_hand = hand.copy()
                if sprite.name == 'body':
                      body_hand = hand.copy()
                    
                offset.x = (origin.x + hand.x + arm_navel.x - arm_hand.x - body_navel.x)
                offset.y = (origin.y + hand.y + arm_navel.y - arm_hand.y - body_navel.y)
                
            
            if 'navel' in sprite['map']:
                navel.x = -sprite['map']['navel'].x * int(flip)
                navel.y = -sprite['map']['navel'].y
                if sprite.name == 'body':
                      body_navel = navel.copy()
                if sprite.name == 'arm':
                      arm_navel = navel.copy()
                    
                offset.x = origin.x + navel.x - body_navel.x #-TamingNavel[0]
                offset.y = origin.y + navel.y - body_navel.y #-TamingNavel[1]
            
            self.offsets[k] = offset
