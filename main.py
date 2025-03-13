from utilities import Utilities
from database import FileRepository
from models import *
fr = FileRepository('')
#Show Login Form
Utilities.fancy('Please Login To Your Account', delay=0, style='bold green', use_ascii=False)        
username, password = Utilities.login()
# username, password = 'david', 'pass'
username, password = 'joe', '123'
valid_login = fr.admin_login(username, password)
print()

if valid_login:
    print()
    Utilities.fancy(f'WELCOME {username} to Student Management System', delay=0.0001, style='bold green', use_ascii=True)
    print()
    while True:
        user_choice = Utilities.show_menu()
        if user_choice == '1':
            Utilities.fancy('Add New Student', delay=0, style='bold green', use_ascii=False)        
            try:
                student = Student.collect_data()
                fr.add_student(student)
                Utilities.fancy(f'Student Added Successfully', delay=0, style='bold green', use_ascii=False)                        
            except InputError as e:
                Utilities.fancy(f'Error, {e}', delay=0, style='bold red', use_ascii=False)
        elif user_choice == '2':
            Utilities.fancy('View All Students', delay=0, style='bold green', use_ascii=False)        
            stdsList = fr.get_all_students()
            ls = [std.to_dict() for std in stdsList]
            if len(ls) > 0:
                Utilities.fancy('', delay=0, style='bold red', use_ascii=True, lstTable=ls, tblTitle="Students List")              
            else:
                Utilities.fancy(f'No Students Added Yet!', delay=0, style='bold red', use_ascii=False)                        
                
        elif user_choice == '3':
            Utilities.fancy('Search For Student', delay=0, style='bold green', use_ascii=False)        
            search_term = input('Enter Search Key: ')
            ls = fr.search_student(search_term)
            if len(ls) > 0:
                Utilities.fancy('', delay=0, style='bold red', use_ascii=True, lstTable=ls, tblTitle="Search result")              
            else:
                Utilities.fancy(f'Not Found!', delay=0, style='bold red', use_ascii=False)                        
        elif user_choice == '4': 
            Utilities.fancy('Enroll Student in Course', delay=0, style='bold green', use_ascii=False)  
            student_id = input('Enter Student ID: ')
            courses = input('Enter Courses (comma separated) to enroll student in: ')
            try:
                fr.enroll_course(student_id, courses)
                Utilities.fancy(f'Courses Added Successfully', delay=0, style='bold green', use_ascii=False)                        
            except StudentNotFound as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)          
        elif user_choice == '5':
            Utilities.fancy('Remove Student enrollment', delay=0, style='bold green', use_ascii=False)     
            student_id = input('Enter Student ID: ')
            courses = input('Enter Courses (comma separated) to remove student from: ')
            try:
                fr.remove_course(student_id, courses)
                Utilities.fancy(f'Courses Removed Successfully', delay=0, style='bold green', use_ascii=False)                        
            except StudentNotFound as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)                    
            except CourseNotFound as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)                    
        elif user_choice == '6':
            Utilities.fancy('Update student', delay=0, style='bold green', use_ascii=False)   
            try:
                student = Student.collect_data()
                fr.update_students(student)
                Utilities.fancy(f'Student Added Successfully', delay=0, style='bold green', use_ascii=False)                        
            except InputError as e:
                Utilities.fancy(f'Error, {e}', delay=0, style='bold red', use_ascii=False)            
            
        elif user_choice == '7':
            Utilities.fancy('Delete Student', delay=0, style='bold green', use_ascii=False)   
            student_id = input('Enter StudentID to delete: ')
            try:
                fr.deletes_students(student_id)
                Utilities.fancy(f'Student Deleted Successfully', delay=0, style='bold green', use_ascii=False)                                        
            except StudentNotFound as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)                                    
        elif user_choice == '8':
            Utilities.fancy('Export Students to CSV', delay=0, style='bold green', use_ascii=False)  
            file_name = input('Enter file name: ')
            try:
                fr.export_students_csv(file_name) 
                Utilities.fancy(f'Exported successfully to {file_name}', delay=0, style='bold green', use_ascii=False)                                
            except Exception as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)                                                    
        elif user_choice == '9':
            Utilities.fancy('Add New System Admin', delay=0, style='bold green', use_ascii=False)   
            try:
                admin = Admin.collect_data()
                fr.add_admin(admin)
                Utilities.fancy(f'Admin Added Successfully', delay=0, style='bold green', use_ascii=False)                        
            except InputError as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)          
        elif user_choice == '10':
            Utilities.fancy('Saving Data and Exit', delay=0, style='bold green', use_ascii=False)   
            try:            
                fr.persist_students()
                fr.persist_admins()
            except Exception as e:
                Utilities.fancy(f'Error {e}', delay=0, style='bold red', use_ascii=False)                          
            break
        else:
            Utilities.fancy('Invalid choice', delay=0, style='bold red', use_ascii=False)                        
        
    Utilities.fancy('Goodbye', delay=0, style='bold green', use_ascii=True)        
else: 
    Utilities.fancy('Invalid Login', delay=0, style='bold red', use_ascii=True)
    