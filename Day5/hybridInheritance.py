class A:
    def method_a(self):
        print("Method A from class A")
class B(A):
    def method_b(self):
        print("Method B from class B")
class C(A):
    def method_c(self):
        print("Method C from class C")
class D(B, C):
    def method_d(self):
        print("Method D from class D")
d1 = D()
d1.method_a()   
d1.method_b()
d1.method_c()
d1.method_d()
