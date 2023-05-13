import string
from random import seed, getrandbits
from math import log

class Random:
    def __init__(self, current):
        self.current = current
        seed(current)
    def __call__(self):
        return getrandbits(32)
        a = 1103515245
        c = 12345
        m = 2**32
        self.current = (a*self.current + c) % m
        return self.current

def prev_lcg(current, a, c, m):
    modinv = lambda a, m: pow(a, -1, m)
    return (current - c) * modinv(a, m) % m

int2base = lambda a, b: ''.join(
    [(string.digits +
      string.ascii_lowercase)[(a // b ** i) % b]
     for i in range(int(log(a, b)), -1, -1)]
)

class Address:
    def __init__(self, hexaddr: str, wall: int, shelf: int, volume: int, page: int):
        self.hexaddr = hexaddr      # 3260 symbols in b36
        self.wall = wall            # 0-3
        self.shelf = shelf          # 0-4
        self.volume = volume        # 0-31
        self.page = page            # 0-409

    def to_int(self) -> str:
        # Создаем уникальный ключ для генератора случайных чисел на основе значений полей
        key = f"1{self.wall}{self.shelf}{self.volume:02}{self.page:03}{self.hexaddr}"
        # Генерируем случайное число на основе ключа
        return int(key, 36)

    @classmethod
    def from_int(cls, addr):
        # Преобразуем случайное число обратно в ключ генератора случайных чисел
        key = int2base(addr, 36)
        # Разбиваем ключ на отдельные поля
        key = key[1:]
        wall, shelf, volume, page, hexaddr = key[:1], key[1:2], key[2:4], key[4:7], key[7:]
        # Создаем и возвращаем объект Address
        return cls(hexaddr, int(wall, 36), int(shelf, 36), int(volume, 36), int(page, 36))
    def __repr__(self):
        hexaddr = self.hexaddr
        wall = self.wall      
        shelf = self.shelf    
        volume = self.volume  
        page = self.page      
        # return f"<Address {hexaddr=} {wall=} {shelf=} {volume=} {page=}>"
        return f"<Address {hexaddr} {wall} {shelf} {volume} {page}>"



class Book:
    title: str # 25 sym
    content: str # 3200 sym
    
    def __init__(self, hexaddr: str, wall: int, shelf: int, volume: int, page: int):
        # generate content
        addr = Address(hexaddr, wall, shelf, volume, page)
        self.address = addr
        self.generate()
    
    @classmethod
    def from_addr(cls, addr: Address):
        return cls(addr.hexaddr,addr.wall,addr.shelf,addr.volume,addr.page)
    
    def generate(self):
        page = 'abcdefghijklmnopqrstuvwxyz,. '
        random = Random(self.address.to_int())
        self.content = ''.join([page[(random() % 29)] for i in range(3200)])
        self.title = ''.join([page[(random() % 29)] for i in range(25)])
        
    def next_page(self):
        self.address.page = min(409, self.address.page+1)
        self.generate()

    def prev_page(self):
        self.address.page = max(0, self.address.page-1)
        self.generate()
    
    def __repr__(self):
        wrapper = lambda s, w: [s[i:i + w] for i in range(0, len(s), w)]
        content = '|'+'|\n|'.join(wrapper(self.content, 80))+'|'
        text = f"Book {self.address}\n|{self.title:^80}|\n{content}\n"
        return text
    
def main():
    b = Book(int2base(1, 36), 0, 0, 0, 0)
    try:
        for i in range(1, 10**8):
            b.address.hexaddr = int2base(i, 36)
            if b.content.find('kotaz') > 0:
                print(b.address)
    except KeyboardInterrupt:
        print(f"i={i} stopped")
main()

    

# print(Book("asd", 0, 0, 0, 0))


# print(Address.from_addr(Address("asd", 1, 2, 3, 4).to_addr()))