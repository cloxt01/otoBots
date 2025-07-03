

class Karakter:
    def __init__(self):
        pass
    def info(self):
        return f"{self.nama} - {self.hp} - {self.att}"
    def attack(self, target):
        print(f"\n{self.nama} menyerang {target.nama} !\n")
        target.hp -= self.att

class Pahlawan(Karakter):
    def __init__(self, nama, hp, att):
        self.nama = nama
        self.hp = hp
        self.att = att
        super().__init__()

class Musuh(Karakter):
    def __init__(self, nama, hp, att):
        self.nama = nama
        self.hp = hp
        self.att = att
        super().__init__()



Pahlawan = Pahlawan("Pahlawan1", 100, 10)
Musuhh = Musuh("Musuh1", 100, 5)


print(Pahlawan.info())
print(Musuhh.info())

Pahlawan.attack(Musuhh)


print(Pahlawan.info())
print(Musuhh.info())