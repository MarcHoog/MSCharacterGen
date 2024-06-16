import struct
import sys
import lz4.block
import pygame

class NX:
    
    def __init__(self, path, populate=True):
        
        self.path = path
        
        self.f = open(path, 'rb')
        magic = self.f.read(4).decode('ascii')
        if magic != 'PKG4':
            raise ValueError('Invalid magic')
        
        
        self.node_count = int.from_bytes(self.f.read(4),'little')
        self.node_offset = int.from_bytes(self.f.read(8),'little')
        self.string_count = int.from_bytes(self.f.read(4),'little')
        self.string_offset = int.from_bytes(self.f.read(8),'little')
        self.image_count = int.from_bytes(self.f.read(4),'little') 
        self.image_offset = int.from_bytes(self.f.read(8),'little')
        self.sound_count = int.from_bytes(self.f.read(4),'little')
        self.sound_offset = int.from_bytes(self.f.read(8),'little')
        
        self.nodes = {}
        self.strings = {}
        self.images = {}
        
        if populate:
            self.populate_nodes()
        
    def get_node(self, index):
        node = self.nodes.get(index, None)
        if node:
            return node
        
        self.f.seek(self.node_offset + index * 20, 0)
        self.nodes[index] = Node.create_node(self.f.read(20), self)
        return self.nodes[index]

    def populate_nodes(self):
        for index in range(self.node_count):
            self.get_node(index)
    
    def read_string(self, index):
        
        if index in self.strings:
            return self.strings[index]
        
        self.f.seek(
            self.string_offset + index * 8
        )
        offset = int.from_bytes(self.f.read(8), 'little')
        self.f.seek(offset)
        string_length = int.from_bytes(self.f.read(2), 'little')
        self.strings[index] = self.f.read(string_length).decode('utf-8')
        return self.strings[index]
    

    def read_image(self, index, width, height):
        image = self.images.get(index)
        if not image:
            self.f.seek(
                    self.image_offset + index * 8)
            
            offset = int.from_bytes(self.f.read(8), 'little')
            
            self.f.seek(offset)
            compressed_size = int.from_bytes(self.f.read(4), 'little')
            compressed_bytes = self.f.read(compressed_size) 
            bytes_ = lz4.block.decompress(compressed_bytes, width * height * 4, True)
            image = pygame.image.frombuffer(bytes_, (width, height), 'BGRA')
            
        return image

class Node:
    
    def __init__(self, 
                 name_index, 
                 child_index,
                 child_count,
                 NX
                 ):
        
        
        self.name = NX.read_string(name_index)
        self.child_index = child_index
        self.child_count = child_count
        self.NX = NX
        
        self.child_map = {}
        self.populate_child_map()
        
    def resolve(self, path):
        node = self
        for p in path.split('/'):
            node = node.child_map[p]
        return node
        
    def populate_child_map(self):
        if self.child_count == 0:
            return
        
        for i in range(self.child_count):
            child = self.NX.get_node(self.child_index + i)
            self.child_map[child.name] = child
    
    @staticmethod
    def create_node(bytes_, NXFile):
        
        # a node is 20 bytes long:
        # Bottom data points to the offset table or just returns the full value
        t,b = bytes_[:12], bytes_[12:]
        node_header = struct.unpack('<IIHH', t)
        kwargs = {
                    'name_index':node_header[0], 
                    'child_index':node_header[1], 
                    'child_count':node_header[2], 
                #    'data':b,
                    'NX': NXFile,}
        
        node_type = node_header[3]
        
        if node_type == 0:  # no data
            return NoDataNode(**kwargs)
                      
        elif node_type == 1:  # int64
            value = int.from_bytes(b, 'little', signed=True)
            return Int64Node(value, **kwargs)
            
        elif node_type == 2:  # double
            value = struct.unpack('<d', b)
            return DoubleNode(value, **kwargs)    

        elif node_type == 3:  # string
            return StringNode(**kwargs)
        
        elif node_type == 4:  # point
            x = int.from_bytes(b[:4], 'little', signed=True)
            y = int.from_bytes(b[4:8], 'little', signed=True)
            return pointNode(x, y, **kwargs)
        
        elif node_type == 5:  # Bitmap
            image_index = int.from_bytes(b[:4], 'little')
            width = int.from_bytes(b[4:6], 'little')
            height = int.from_bytes(b[6:8], 'little')
            return BitMapNode(image_index, width, height, **kwargs)
            
        elif node_type == 6:  # Audio
            return AudioNode(**kwargs)
    
    # how to make ['stand1'][z] notation work on a class
    def __getitem__(self, child:str):
        return self.resolve(child)
    
    def __contains__(self, child:str):
        return child in self.child_map

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'
                
class NoDataNode(Node):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
class Int64Node(Node):
    def __init__(self, value, **kwargs):
        self.value = value
        super().__init__(**kwargs)
           
class DoubleNode(Node):
    def __init__(self, value, **kwargs):
        self.value = value
        super().__init__(**kwargs)

class StringNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class pointNode(Node):
    def __init__(self,x,y, **kwargs):
        super().__init__(**kwargs)
        
        self.x = x
        self.y = y

class BitMapNode(Node):
    def __init__(self,image_index, width, height, **kwargs):
        self.image_index = image_index
        self.width = width
        self.height = height

        super().__init__(**kwargs)
        
    @property
    def image(self):
        return self.NX.read_image(self.image_index, self.width, self.height)
    
    def load_image(self):
        img = self.image
        img.set_alpha(255,255)
        return img.convert_alpha()

class AudioNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    
...