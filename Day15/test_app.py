# from app import add, calcc, sub, mul, div
# def test_add():
#     result=add(2,3)
#     assert result==5
# def test_sub():
#     result=sub(5,2)
#     assert result==3    

# def test_mul():
#     result=mul(2,3)
#     assert result==6
# def test_div():
#     result=div(6,2)
#     assert result==3


# def test_calculator():
#     assert add(2,3)==5
#     assert sub(5,2)==3
#     assert mul(2,3)==6
#     assert div(6,2)==3

# import pytest
# from app import calcc

# @pytest.fixture
# def calc():
#     return calcc()

# def test_calc_add(calc):
#     assert calc.add(2,3)==5

import pytest
from app import div
def test_div_zero():
    with pytest.raises(ValueError):
        div(5,0)
        