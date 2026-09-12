# student_analyzer/models/student.py
# q41
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    score: int
    email: str
    
    # q45
    def __post_init__(self):
        if not isinstance(self.score, int):
            raise TypeError(
                f"name: {self.name}, score must be int, got {type(self.score).__name__}"
            )
        if self.score < 0 or self.score > 100:
            raise InvalidScoreError(
                f"name: {self.name}, score must be between 0 and 100, got {self.score}"
            )
    
    def is_passed(self):
        return self.score >= 60
    
# q42    
    def get_grade(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"
        
# q43
# class在实例化后可以直接调用属性进行本身数据的一些行为

# q44 
# 因为InvalidScoreError是判定数值的范围，所以用ValueError
class InvalidScoreError(ValueError):
    pass

# q46
# 正常对象
# TypeError
# InvalidScoreError
# InvalidScoreError
    
# q47
# is_passed(),get_grade()只需要该实例的数据，所以可以放在Student类中
# get_average_score(),get_top_student(),get_passed_students()需要多个学生的数据，所以不应该放到Student类

