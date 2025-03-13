from abc import ABC, abstractmethod
from utilities import Utilities
from models import InputError, Person, Admin, Student, StudentNotFound, CourseNotFound

class SchoolRepository(ABC):
    admins_list = []
    students_list = []
    
    @abstractmethod
    def persist_students(self):
        pass
    
    @abstractmethod
    def export_students_csv(self, filename):
        pass
    
    @abstractmethod
    def persist_admins(self):
        pass    
    
    def add_admin(self,admin):
        self.admins_list.append(admin)        
            
    def admin_login(self, username, password):    
        hash_pass = Utilities.hash_password(password)
        return len([admin for admin in self.admins_list if admin.username == username and admin.password == hash_pass]) > 0
    
    def add_student(self,student_new):
        lst = [student for student in self.students_list if student.student_id == student_new.student_id]
        if len(lst) == 0:
            self.students_list.append(student_new)  
        else:
            raise InputError(f'Student with the same id {student_new.student_id} added before')
    
    def get_all_students(self):
        return self.students_list.copy()
    
    def search_student(self, search):
        result = [student.to_dict() for student in self.students_list 
                  if search in student._name or search in str(student._age) or search in str(student.student_id) or search in student._gender or search in student.courses].copy()
        return result
    
    def update_students(self, student):
        old_student = self.get_student_by_id(student.student_id)
        old_student._name = student._name
        old_student._age = student._age
        old_student._gender = student._gender
        old_student.courses = student.courses
        
        
        
    
    def deletes_students(self, studentId):
        lst = [student for student in self.students_list if student.student_id == studentId]
        if len(lst) == 0 :
            raise StudentNotFound(f'Student with ID {studentId} not found')
        else:
            self.students_list.remove(lst[0])
    
    def enroll_course(self, student_id, courses_to_add):
        student = self.get_student_by_id(student_id)
        courses_list = list(map(lambda c: c.strip().lower(),courses_to_add.split(',')))        
        consolidate_courses = student.courses.copy()
        consolidate_courses.extend(courses_list)
        student.courses = list(set(consolidate_courses))
        
    def remove_course(self, student_id, courses_to_remove):
        student = self.get_student_by_id(student_id)
        courses_list = list(set(list(map(lambda c: c.strip().lower(),courses_to_remove.split(',')))))
        for course in courses_list:    
            if course in student.courses:
                student.courses.remove(course)
            else:
                raise CourseNotFound(f'Course: {course} not found in student {student_id} registration')
        
    def get_student_by_id(self, student_id):
        result = [student for student in self.students_list if student_id == str(student.student_id) ].copy()
        if len(result) == 0 :
            raise StudentNotFound(f'Student with ID {student_id} not found')
        return result[0]
    
    

#Joe nice trick ;)
def singleton(cls):
    instances = {}  

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs) 
        return instances[cls]  

    return get_instance    
    
@singleton    
class FileRepository(SchoolRepository):
    def __init__(self, connection_string):
        super().__init__()
        self.admin_connection_string = connection_string + 'admins.json'
        self.students_connection_string = connection_string + 'students.json'
        self.___load_admins()
        self.___load_students()
        
    def persist_students(self):
        students_json = ([s.to_dict() for s in self.students_list])
        Utilities.save_load_json_file(self.students_connection_string, 'w',students_json)
        
    def export_students_csv(self, filename):
        students_json = ([s.to_dict() for s in self.students_list])
        if not filename.endswith('.csv'):
            filename += '.csv'            
        Utilities.save_to_csv(filename,students_json)
        

    def persist_admins(self):
        admins_json = ([s.to_dict() for s in self.admins_list])
        Utilities.save_load_json_file(self.admin_connection_string, 'w',admins_json)

        
    def ___load_admins(self):
        loaded_data = Utilities.save_load_json_file(self.admin_connection_string, 'r')        
        self.admins_list = [Admin.of(obj) for obj in loaded_data]
    
    def ___load_students(self):
        loaded_data = Utilities.save_load_json_file(self.students_connection_string, 'r')
        self.students_list = [Student.of(obj) for obj in loaded_data]
        
        
        
        