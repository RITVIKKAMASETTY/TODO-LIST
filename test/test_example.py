import pytest
def test():
    assert 1==1
class student:
    def __init__(self,firstname:str,lastname:str,major:str,years:int):
        self.firstname=firstname
        self.lastname=lastname
        self.major=major
        self.years=years
@pytest.fixture
def defaultstudent():
    return student("John","Doe","Computer Science",4)
def testpersoninitilization(defaultstudent):
    assert defaultstudent.firstname=="John"
    assert defaultstudent.lastname=="Doe"
    assert defaultstudent.major=="Computer Science"
    assert defaultstudent.years==4