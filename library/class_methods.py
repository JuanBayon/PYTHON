class Person: 
    def __init__(self, name, age, is_alive): 
        self.__name = name 
        self.__age = age 
    
    @classmethod
    def from_birth_year(cls, name, birthyear): 

    @staticmethod
    def is_adult(age):
        return age > 18

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, x):
        if (x == "" or x == None):
            print("Por favor, escriba un nombre")
        elif len(x) < 4 or len(x) > 6:
            print("Escribe un nombre con 4,5,6 catacteres")
        else:
            self.__name = x