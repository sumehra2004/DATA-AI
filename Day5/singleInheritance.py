class Father:
    def drive(self):
        print("Father can drive")
class Son(Father):
    def play(self):
        print("Son can play")   
s1=Son()
s1.drive()  
s1.play()
