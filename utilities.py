import time
import sys
import pyfiglet
from rich.console import Console
from rich.table import Table
class Utilities:
    @staticmethod
    def fancy(text, delay=0.05, use_ascii=False, style="bold red", lstTable=None,  tblTitle=""):        
        console = Console()
        if len(text) > 0:
            ascii_text = text
            if use_ascii:
                ascii_text = pyfiglet.figlet_format(text)
            
            if delay != 0:    
                for char in ascii_text:
                    console.print(f"{char}", end="", style=style)  # Using Rich color formatting
                    sys.stdout.flush()
                    time.sleep(delay)
            else:
                console.print(ascii_text,  style=style)
        else:
            if lstTable:
                table = Table(title=tblTitle, style=style)
                for id,item in enumerate(lstTable):
                    if id == 0:
                        for key, _ in item.items():
                            table.add_column(key, justify="center", style=style)
                    vals = [", ".join(map(str,v)) if isinstance(v, list) else str(v) for v in item.values()]
                    table.add_row(*vals)
                console.print(table)  # Redraw table with new row
            
        print() 
        
    @staticmethod        
    def login():
        import getpass
        username = input("👤 Username: ")  
        print("🔑 Enter your password: ")  
        password = getpass.getpass("")  
        return username, password


    @staticmethod        
    def save_load_json_file(filename,mode='r', js_string=None ):
        import json
        try:
            if mode == 'r':
                with open(filename, mode, encoding="utf-8") as file:
                    return json.load(file)  
            elif mode == 'w' and isinstance(js_string, list):
                with open(filename, mode, encoding="utf-8") as file:
                    json.dump(js_string, file, indent=4)            
        except json.JSONDecodeError:  
            return []
        
    @staticmethod
    def save_to_csv(filename, data):
        import csv
        with open(filename, "w", newline="", encoding="utf-8") as file:
            fieldnames = data[0].keys()  
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  
            writer.writerows(data)  

    @staticmethod        
    def show_menu():
        print()
        menu = [
            {'key': 1, 'Action': 'Add New Student'}, 
            {'key': 2, 'Action': 'View All Students'},
            {'key': 3, 'Action': 'Search For Student'},
            {'key': 4, 'Action': 'Enroll Student in Course'}, 
            {'key': 5, 'Action': 'Remove Student enrollment'},
            {'key': 6, 'Action': 'Update student main information'},
            {'key': 7, 'Action': 'Delete Student'},            
            {'key': 8, 'Action': 'Export Students to CSV'},      
            {'key': 9, 'Action': 'Add New System Admin'},      
            {'key': 10, 'Action': 'Save and Exit'}] 
        Utilities.fancy('', delay=0, style='bold red', use_ascii=True, lstTable=menu, tblTitle="Select Option")  
        choice = input(" ✏️   Enter your choice: ").strip().lower()
        return choice
    
    @staticmethod
    def hash_password(password):
        import bcrypt
        salt = b'$2b$12$lY8OOM.FYmujWbANc7fGeO'
        hashed = bcrypt.hashpw(password.encode(), salt)  
        return hashed.decode('utf-8')  