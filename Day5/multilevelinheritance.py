class Grandfather:
    def wisdom(self):
        print("Grandfather shares wisdom")
class Father(Grandfather):
    def drive(self):
        print("Father can drive")
class Son(Father):
    def play(self):
        print("Son can play")   
s1=Son()
s1.wisdom() 
s1.drive()
s1.play()