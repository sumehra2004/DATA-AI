class Mother:
    def cook(self):
        print("Mother can cook")
class Daughter(Mother):
    def dance(self):
        print("Daughter can dance") 
class Son(Mother):
    def play(self):
        print("Son can play")

d1=Daughter()
d1.cook()  
d1.dance()     
s1=Son()
s1.cook()
s1.play()