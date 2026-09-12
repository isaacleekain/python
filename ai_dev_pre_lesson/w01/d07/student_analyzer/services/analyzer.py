# student_analyzer/services/analyzer.py
# q59
from ..models.student import Student



class StudentAnalyzer:
    def __init__(self, students):
        self.students = students
        
    def get_average_score(self):
        return sum([i.score for i in self.students]) / len(self.students)
    
    def get_top_student(self):
        return max(self.students, key=lambda x: x.score)
    
    def get_passed_students(self):
        return [i for i in self.students if i.is_passed()]
    
    # q64
    def get_student_by_name(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None
    
    # q65
    def get_students_by_grade(self, grade):
        return [i for i in self.students if i.get_grade() == grade.upper()]
    