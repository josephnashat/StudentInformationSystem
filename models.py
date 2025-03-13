from abc import ABC, abstractmethod

from utilities import Utilities
class Person:
    def __init__(self, name, age, gender):
        self._name = name
        self._age = age
        self._gender = gender
        
    @abstractmethod        
    def to_dict(self):
        pass
    
    @abstractmethod
    def collect_data(self):
        pass
    
class Admin(Person):
    def __init__(self, name, age, gender, username, password):
        super().__init__(name, age, gender)
        self.username = username
        self.password = password
        
    def to_dict(self):
        return {
            "name": self._name,
            "age": self._age,
            "gender": self._gender,
            "username": self.username,
            "password": self.password
        }
        
    @classmethod
    def collect_data(cls):
        data = {}
        data['name'] = input('Enter Name: ')
        if len(data['name']) == 0:
            raise InputError('Name is required')            
        try:
            data['age'] = float(input('Enter age: '))
        except:
            raise InputError('Age is not valid')
        gender = input('Gender (Male/Female): ')
        if gender.strip().lower() not in ['male', 'female']:
            raise InputError('Gender is not valid only Male or Female')
        else:
            data['gender'] = gender
        data['username'] = input('Enter Username: ')
        if len(data['username']) == 0:
            raise InputError('Username is required')
        password = input('Enter Password: ')
        if len(password) == 0:
            raise InputError('Password is required')        
        data['password'] = Utilities.hash_password(password)
        return cls(**data)        
    
    @classmethod
    def of(cls, dict):
        return cls(**dict)
        
    
    
class Student(Person):
    def __init__(self, name, age, gender, student_id, courses):
        super().__init__(name, age, gender)
        self.student_id = student_id
        self.courses = courses
        
        
    def to_dict(self):
        return {
            "name": self._name,
            "age": self._age,
            "gender": self._gender,
            "student_id": self.student_id,
            "courses": self.courses
        }
        
    @classmethod
    def collect_data(cls):
        data = {}
        data['name'] = input('Enter student name: ')
        if len(data['name']) == 0:
            raise InputError('Name is required')      
        try:
            data['age'] = float(input('Enter student age: '))
        except:
            raise InputError('Age is not valid')
        gender = input('Gender (Male/Female): ')
        if gender.strip().lower() not in ['male', 'female']:
            raise InputError('Gender is not valid only Male or Female')
        else:
            data['gender'] = gender
        data['student_id'] = input('Enter Student ID: ')
        if len(data['student_id']) == 0:
            raise InputError('StudentID is required')              
        courses = input('Enter courses comma separated: ')
        if len(courses) == 0:
            raise InputError('StudentID is required')              
        
        courses_list = list(map(lambda c: c.strip().lower(),courses.split(',')))                
        data['courses'] = list(set(courses_list))
        return cls(**data)
        
        
    @classmethod
    def of(cls, dict):
        return cls(**dict)        
        
        
class CourseNotFound(Exception):        
    pass
        
class InputError(Exception):        
    pass

class StudentNotFound(Exception):        
    pass
