'''
DATA 200 Lab 1
Implement CheckMyGrade Application

Data Structures used:
    - Dictionary: students_dic, courses_dic, professors_dic, login_dic
    - Linked List: student_list 
    - Array: grade

Last modified: 03/16/2026
'''

# Import necessary libraries
import csv
import os
import time
import statistics as stats  

# Import the encdyc module for text security
import encdyc

# Shift cipher with a shift of 7
_cipher = encdyc.TextSecurity(7)


# CSV file paths
STUDENTS_CSV = "students.csv"
COURSES_CSV = "courses.csv"
PROFESSORS_CSV = "professors.csv"
LOGIN_CSV = "login.csv"

def _read_csv(file_path):
    """
    Read data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file to read.
    
    Returns:
        list: List of dictionaries, where each dictionary represents a row in the CSV file.
              Returns empty list if file does not exist.
    """
    data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data

def _write_csv(file_path, data, fieldnames):
    """
    Write data to a CSV file.
    
    Args:
        file_path (str): Path to the output CSV file.
        data (list): List of dictionaries to write, where each dictionary represents a row.
        fieldnames (list): List of column names for the CSV header.
    
    Returns:
        None
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)



# Linked List Node class for students
class _Node:
    """Internal node class for linked list.
    
    Attributes:
        email (str): The student email stored in this node.
        next (_Node): Reference to the next node in the linked list.
    """
    def __init__(self, email):
        """Initialize a linked list node.
        
        Args:
            email (str): The student email to store in this node.
        """
        self.email = email
        self.next = None

# Linked list to store student emails for quick access and management
class LinkedList:
    """Linked list implementation for managing student emails.
    
    Attributes:
        head (_Node): Reference to the first node in the linked list.
        _size (int): Current number of nodes in the linked list.
    """
    def __init__(self):
        """Initialize an empty linked list."""
        self.head = None
        self._size = 0

    def append(self, email):
        """Add a new email to the end of the linked list.
        
        Args:
            email (str): The student email to append.
        
        Returns:
            None
        """
        new_node = _Node(email)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def remove(self, email):
        """Remove an email from the linked list.
        
        Args:
            email (str): The student email to remove.
        
        Returns:
            bool: True if the email was found and removed, False otherwise.
        """
        current = self.head
        previous = None
        while current:
            if current.email == email:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def find(self, email):
        """Search for an email in the linked list.
        
        Args:
            email (str): The student email to search for.
        
        Returns:
            bool: True if the email is found, False otherwise.
        """
        current = self.head
        while current:
            if current.email == email:
                return True
            current = current.next
        return False
    
    def to_list(self):
        """Convert the linked list to a Python list.
        
        Returns:
            list: List of all student emails in the linked list.
        """
        emails = []
        current = self.head
        while current:
            emails.append(current.email)
            current = current.next
        return emails

    def size(self):
        """Get the number of nodes in the linked list.
        
        Returns:
            int: The size of the linked list.
        """
        return self._size   


'''
Student: FirstName, LastName, email_address, Courses.id, Grades, marks
Functions: 
display_records()
add_new_student()
delete_new_student()
check_my_grades()
update_student_record()
check_my_marks()
enroll_course() # Add function to enroll a student in a course
sort_students_by_last_name()
sort_students_by_grade()
sort_students_by_email
search_student_by_email()   
'''

# Dictionary to store all students
# Use email as the key
students_dic = {}
student_list = LinkedList()  # Linked list to manage student emails

# Define the student class with the specified attributes and functions
class Student():
    """Represents a student in the grade management system.
    
    Attributes:
        FirstName (str): The student's first name.
        LastName (str): The student's last name.
        email_address (str): The student's unique email address.
    """

    def __init__(self, FirstName, LastName, email_address):
        """Initialize a Student object.
        
        Args:
            FirstName (str): The student's first name.
            LastName (str): The student's last name.
            email_address (str): The student's email address.
        """
        self.FirstName = FirstName
        self.LastName = LastName
        self.email_address = email_address
    
    def display_records(self):
        """Display the student's complete information and enrolled courses.
        
        Prints the student's name, email address, and all enrolled courses
        with their grades and marks.
        
        Returns:
            None
        """
        print(f"Name: {self.FirstName} {self.LastName}")
        print(f"Email Address: {self.email_address}")
        courses = students_dic[self.email_address]["courses"]
        if courses:
            print("Courses:")
            for c in courses:
                print(f"  Course ID: {c['Courses_id']} | Grade: {c['Grades']} | Marks: {c['marks']}")
        else:
            print("Courses: None")

    def check_my_grades(self):
        """Get the student's grades for all enrolled courses.
        
        Returns:
            list: List of tuples (course_id, grade) for all enrolled courses.
        """
        courses = students_dic[self.email_address]["courses"]
        return [(c["Courses_id"], c["Grades"]) for c in courses]  
    
    def check_my_marks(self):
        """Get the student's marks for all enrolled courses.
        
        Returns:
            list: List of tuples (course_id, marks) for all enrolled courses.
        """
        courses = students_dic[self.email_address]["courses"]
        return [(c["Courses_id"], c["marks"]) for c in courses]   

def add_new_student(FirstName, LastName, email_address, Courses_id, Grades, marks):
    """Add a new student to the system with an initial course enrollment.
    
    Args:
        FirstName (str): The student's first name.
        LastName (str): The student's last name.
        email_address (str): The student's unique email address.
        Courses_id (str): The ID of the course to enroll the student in.
        Grades (str): The student's grade in the course.
        marks (str): The student's marks/score in the course.
    
    Returns:
        None
    
    Prints:
        Success message if added, or error message if student already exists
        or course does not exist.
    """
    # Check student does not already exist
    if email_address in students_dic:
        print("Student with this email already exists.")
        return

    # Check course exists before adding student to it
    if Courses_id not in courses_dic:
        print(f"Course {Courses_id} does not exist. Please add the course first.")
        return

    new_student = Student(FirstName, LastName, email_address)
    students_dic[email_address] = {
        "student": new_student,
        "courses": [{"Courses_id": Courses_id, "Grades": Grades, "marks": marks}]
    }
    student_list.append(email_address)  # Add student email to linked list
    save_students_to_csv()  # Save students to CSV after adding new student
    print(f"Student {FirstName} {LastName} added successfully.")      


def delete_student(email_address):
    """Delete a student from the system.
    
    Args:
        email_address (str): The email address of the student to delete.
    
    Returns:
        None
    
    Prints:
        Success message if deleted, or error message if student not found.
    """
    if email_address in students_dic:
        student_name = f"{students_dic[email_address]['student'].FirstName} {students_dic[email_address]['student'].LastName}"
        del students_dic[email_address]
        student_list.remove(email_address)  # Remove student email from linked list
        save_students_to_csv()  # Save students to CSV after deleting student
        print(f"Student {student_name} deleted successfully.")
    else:
        print("Student with this email does not exist.")


def update_student_record(email_address, Courses_id, FirstName=None, LastName=None, Grades=None, marks=None):
    """Update a student's personal information and/or course grades/marks.
    
    Args:
        email_address (str): The email address of the student to update.
        Courses_id (str): The ID of the course whose grades/marks to update.
        FirstName (str, optional): New first name. Defaults to None (no change).
        LastName (str, optional): New last name. Defaults to None (no change).
        Grades (str, optional): New grade for the course. Defaults to None (no change).
        marks (str, optional): New marks for the course. Defaults to None (no change).
    
    Returns:
        None
    
    Prints:
        Success message if updated, or error message if student not found.
    """
    if email_address in students_dic:
        upt_student = students_dic[email_address]
        if FirstName:
            upt_student["student"].FirstName = FirstName
        if LastName:
            upt_student["student"].LastName = LastName
        # Update course record    
        for c in upt_student["courses"]:
            if c["Courses_id"] == Courses_id:
                if Grades is not None:
                    c["Grades"] = Grades
                if marks is not None:
                    c["marks"] = marks
                break
        save_students_to_csv()  # Save students to CSV after updating record
        print(f"Student {upt_student['student'].FirstName} {upt_student['student'].LastName}'s record updated successfully.")
    else:
        print("Student with this email does not exist.")

def enroll_course(email_address, Courses_id, Grades, marks):
    """Enroll an existing student in a new course.
    
    Args:
        email_address (str): The email address of the student to enroll.
        Courses_id (str): The ID of the course to enroll in.
        Grades (str): The student's grade in the course.
        marks (str): The student's marks/score in the course.
    
    Returns:
        None
    
    Prints:
        Success message if enrolled, or error message if student/course
        not found or student already enrolled in course.
    """
    # Check student exists before enrolling them in a course
    if email_address not in students_dic:
        print("Student with this email does not exist.")
        return
    # Check course exists before enrolling student in it
    if Courses_id not in courses_dic:
        print(f"Course {Courses_id} does not exist. Please add the course first.")
        return

    # Check if student is already enrolled in the course
    courses = students_dic[email_address]["courses"]
    for c in courses:
        if c["Courses_id"] == Courses_id:
            print(f"Student is already enrolled in {Courses_id}.")
            return
    # Enroll student in the course
    courses.append({"Courses_id": Courses_id, "Grades": Grades, "marks": marks})
    save_students_to_csv()  # Save students to CSV after enrolling in course    
    name = f"{students_dic[email_address]['student'].FirstName} {students_dic[email_address]['student'].LastName}"
    print(f"Student {name} enrolled in {Courses_id} successfully.")


def sort_students_by_last_name(reverse=False):
    """Sort all students alphabetically by last name.
    
    Sorts students in ascending order by their last name and displays
    the execution time. Uses O(n log n) sorting algorithm.
    
    Returns:
        list: List of Student objects sorted alphabetically by last name.
    
    Prints:
        Execution time of the sort operation.
    """
    start = time.perf_counter()
    emails = student_list.to_list()
    sorted_emails = sorted(
        emails,
        key=lambda e: students_dic[e]["student"].LastName.lower(), reverse=reverse
    )
    elapsed = time.perf_counter() - start
    print(f"Sort by name ({"DESC" if reverse else "ASC"}) — time: {elapsed:.6f}s")
    return [students_dic[e]["student"] for e in sorted_emails]

def sort_students_by_grade(Courses_id, reverse=False):
    """Sort students by their marks in a specific course.
    
    Sorts enrolled students in ascending order by marks in the specified
    course and displays the execution time. Uses O(n log n) sorting algorithm.
    
    Args:
        Courses_id (str): The ID of the course to sort by.
    
    Returns:
        list: List of Student objects sorted by marks in ascending order.
              Only includes students enrolled in the specified course.
    
    Prints:
        Execution time of the sort operation.
    """
    start = time.perf_counter()
    enrolled = [
        e for e in student_list.to_list()
        if any(c["Courses_id"] == Courses_id
               for c in students_dic[e]["courses"])
    ]
    def get_marks(email):
        for c in students_dic[email]["courses"]:
            if c["Courses_id"] == Courses_id:
                try:    return float(c["marks"])
                except: return 0.0
        return 0.0
    sorted_emails = sorted(enrolled, key=get_marks, reverse=reverse)
    elapsed = time.perf_counter() - start
    print(f"Sort by grade {Courses_id} ({"DESC" if reverse else "ASC"}) — time: {elapsed:.6f}s")
    return [students_dic[e]["student"] for e in sorted_emails]    

def search_student_by_email(email_address):
    """Search for a student by their email address.
    
    Performs a search for a student using their email as the key and
    displays the execution time. Uses O(1) dictionary lookup.
    
    Args:
        email_address (str): The email address to search for.
    
    Returns:
        Student: The Student object if found, None otherwise.
    
    Prints:
        Execution time of the search operation.
        Error message if student not found.
    """
    start = time.perf_counter()
    if email_address in students_dic:
        student = students_dic[email_address]["student"]
        elapsed = time.perf_counter() - start
        print(f"Search by email — time: {elapsed:.6f}s")
        return student
    else:
        elapsed = time.perf_counter() - start
        print(f"Search by email — time: {elapsed:.6f}s")
        print("Student with this email does not exist.")
        return None
    

def sort_students_by_email(reverse=False):
    """Sort all students alphabetically by email address.
 
    Args:
        reverse (bool): If True, sort descending. Default ascending.
 
    Returns:
        list[Student]: Sorted list of Student objects.
 
    Prints:
        Sort direction and elapsed time.
    """
    start  = time.perf_counter()
    emails = student_list.to_list()
    sorted_emails = sorted(emails, key=lambda e: e.lower(), reverse=reverse)
    elapsed = time.perf_counter() - start
    direction = "DESC" if reverse else "ASC"
    print(f"Sort by email ({direction}) — {elapsed:.6f}s")
    return [students_dic[e]["student"] for e in sorted_emails]

    
def save_students_to_csv():
    rows = []
    for email, data in students_dic.items():
        student = data["student"]
        courses = data["courses"]
        for c in courses:
            rows.append({
                "Email_address": email,
                "FirstName": student.FirstName,
                "LastName": student.LastName,
                "Courses_id": c["Courses_id"],
                "Grades": c["Grades"],
                "marks": c["marks"]
            })
    fieldnames = ["Email_address", "FirstName", "LastName", "Courses_id", "Grades", "marks"]
    _write_csv(STUDENTS_CSV, rows, fieldnames)

def load_students_from_csv():
    rows = _read_csv(STUDENTS_CSV)
    for row in rows:
        email = row["Email_address"]
        if email not in students_dic:
            student = Student(row["FirstName"], row["LastName"], email)
            students_dic[email] = {
                "student": student,
                "courses": []
            }
            student_list.append(email)
        students_dic[email]["courses"].append({
            "Courses_id": row["Courses_id"],
            "Grades": row["Grades"],
            "marks": row["marks"]
        })
    

'''
Course: Course_id, Credits, Course_name, description
Functions:
display_courses()
add_new_course()
delete_course()
update_course() # only modify credits and description
calculate_course_statistics() # Add function to calculate average, median, highest, and lowest marks for a course
'''
# Dictionary to store all courses
# Use course_id as the key
courses_dic = {} 

# Define the course class with the specified attributes and functions
class Course():
    """Represents a course in the grade management system.
    
    Attributes:
        Course_id (str): The unique course identifier.
        Credits (str): The number of credits for this course.
        Course_name (str): The name of the course.
        description (str): Course description (optional).
    """
    
    def __init__(self, Course_id, Credits, Course_name, description=None):
        """Initialize a Course object.
        
        Args:
            Course_id (str): The unique course identifier.
            Credits (str): The number of credits for this course.
            Course_name (str): The name of the course.
            description (str, optional): Course description. Defaults to None.
        """
        self.Course_id = Course_id
        self.Credits = Credits
        self.Course_name = Course_name
        self.description = description
    
    def display_courses(self):
        """Display the course's information.
        
        Prints the course ID, name, credits, and description (if available).
        
        Returns:
            None
        """
        print(f"Course ID: {self.Course_id}")
        print(f"Course Name: {self.Course_name}")
        print(f"Credits: {self.Credits}")
        if self.description:
            print(f"Description: {self.description}")

def add_new_course(Course_id, Credits, Course_name, description=None):
    """Add a new course to the system.
    
    Args:
        Course_id (str): The unique course identifier.
        Credits (str): The number of credits for the course.
        Course_name (str): The name of the course.
        description (str, optional): Course description. Defaults to None.
    
    Returns:
        None
    
    Prints:
        Success message if added, or error message if course ID already exists.
    """
    if Course_id in courses_dic:
        print("Course with this ID already exists.")
        return
    else:
        new_course = Course(Course_id, Credits, Course_name, description)
        courses_dic[Course_id] = new_course
        save_course_to_csv()  # Save courses to CSV after adding new course 
        print(f"Course {Course_name} added successfully.")

def delete_course(Course_id):
    """Delete a course from the system.
    
    Removes the course from the system and cascades the deletion by
    removing it from all student enrollments and professor assignments.
    
    Args:
        Course_id (str): The ID of the course to delete.
    
    Returns:
        None
    
    Prints:
        Success message if deleted, or error message if course not found.
    """
    if Course_id in courses_dic:
        course_name = courses_dic[Course_id].Course_name
        del courses_dic[Course_id]
        # Remove from students
        for student in students_dic.values():
            student["courses"] = [ 
                c for c in student["courses"]
                if c["Courses_id"] != Course_id
        ]

        # Remove from professors
        for professor in professors_dic.values():
            professor["courses"] = [
                c for c in professor["courses"]
                if c["Courses_id"] != Course_id
            ]
        save_course_to_csv()  # Save courses to CSV after deleting course
        save_students_to_csv()  # Save students to CSV after cascading deletion 
        save_professors_to_csv()  # Save professors to CSV after cascading deletion
        print(f"Course {course_name} deleted successfully.")
    else:
        print("Course with this ID does not exist.")


def update_course(Course_id, Credits=None, Course_name=None, description=None):
    """Update an existing course's details.
 
    Args:
        Course_id (str): ID of the course to update.
        Credits (str|int, optional): New credits value.
        Course_name (str, optional): New course name.
        description (str, optional): New description.
 
    Returns:
        bool: True on success, False if not found.
    """
    if Course_id not in courses_dic:
        print(f"Course '{Course_id}' does not exist.")
        return False
    c = courses_dic[Course_id]
    if Credits is not None:
        c.Credits = Credits
    if Course_name is not None:
        c.Course_name = Course_name
    if description is not None:
        c.description = description
    save_course_to_csv()
    print(f"Course '{Course_id}' updated successfully.")
    return True


def calculate_course_statistics(Course_id):
    """Calculate statistics for marks in a specific course.
    
    Calculates and displays the average, median, highest, and lowest marks
    for all students enrolled in the specified course.
    
    Args:
        Course_id (str): The ID of the course to calculate statistics for.
    
    Returns:
        None
    
    Prints:
        Course statistics (average, median, highest, lowest) or error message
        if course not found or no marks available.
    """
    if Course_id not in courses_dic:
        print(f"Course {Course_id} does not exist.")
        return

    marks = []
    for student in students_dic.values():
        for c in student["courses"]:
            if c["Courses_id"] == Course_id:
                try:
                    marks.append(float(c["marks"]))
                except ValueError:
                    continue

    if not marks:
        print(f"No marks available for course {Course_id}.")
        return

    average = stats.mean(marks)
    median = stats.median(marks)
    highest = max(marks)
    lowest = min(marks)

    print(f"Statistics for Course {Course_id}:")
    print(f"Average Marks: {average:.2f}")
    print(f"Median Marks: {median:.2f}")
    print(f"Highest Marks: {highest:.2f}")
    print(f"Lowest Marks: {lowest:.2f}")


def save_course_to_csv():
    rows = []
    for course_id, course in courses_dic.items():
        rows.append({
            "Course_id": course.Course_id,
            "Credits": course.Credits,
            "Course_name": course.Course_name,
            "description": course.description if course.description else ""
        })
    fieldnames = ["Course_id", "Credits", "Course_name", "description"] 
    _write_csv(COURSES_CSV, rows, fieldnames)


def load_courses_from_csv():
    rows = _read_csv(COURSES_CSV)
    for row in rows:
        course_id = row["Course_id"]
        if course_id not in courses_dic:
            course = Course(
                Course_id=row["Course_id"],
                Credits=row["Credits"],
                Course_name=row["Course_name"],
                description=row.get("description", "")
            )
            courses_dic[course_id] = course
    

"""
Professor: Name, email_address, Rank, Courses.id
Functions:
professor_details()
add_new_professor()
delete_professor()
modify_professor_details() # only modify name and rank
assign_course_to_professor() # Add function to assign a course to a professor
delete_course_from_professor() # Add function to delete a course from a professor
show_courses_details_by_professor()
"""

professors_dic = {}

class Professor():
    """Represents a professor in the grade management system.
    
    Attributes:
        Name (str): The professor's full name.
        email_address (str): The professor's unique email address.
        Rank (str): The professor's academic rank (e.g., Professor, Associate Professor).
    """
    
    def __init__(self, Name, email_address, Rank):
        """Initialize a Professor object.
        
        Args:
            Name (str): The professor's full name.
            email_address (str): The professor's email address.
            Rank (str): The professor's academic rank.
        """
        self.Name = Name
        self.email_address = email_address
        self.Rank = Rank

    def professor_details(self):
        """Display the professor's complete information and assigned courses.
        
        Prints the professor's name, email address, rank, and all assigned
        courses with their names.
        
        Returns:
            None
        """
        print(f"Name: {self.Name}")
        print(f"Email Address: {self.email_address}")
        print(f"Rank: {self.Rank}")
        courses = professors_dic[self.email_address]["courses"]
        if courses:
            print("Courses:")
            for c in courses:
                if c["Courses_id"] in courses_dic:
                    print(f"  Course ID: {c['Courses_id']} | Course Name: {courses_dic[c['Courses_id']].Course_name}")
        else:
            print("Courses: None")

def add_new_professor(Name, email_address, Rank, Courses_id):
    """Add a new professor to the system with an initial course assignment.
    
    Args:
        Name (str): The professor's full name.
        email_address (str): The professor's unique email address.
        Rank (str): The professor's academic rank.
        Courses_id (str): The ID of the course to assign to the professor.
    
    Returns:
        None
    
    Prints:
        Success message if added, or error message if professor already exists
        or course does not exist.
    """
    if email_address in professors_dic:
        print("Professor with this email already exists.")
        return
    if Courses_id not in courses_dic:
        print(f"Course {Courses_id} does not exist. Please add the course first.")
        return

    new_professor = Professor(Name, email_address, Rank)
    professors_dic[email_address] = {
        "professor": new_professor,
        "courses": [{"Courses_id": Courses_id}]
    }
    save_professors_to_csv()  # Save professors to CSV after adding new professor   
    print(f"Professor {Name} added successfully.")  

def delete_professor(email_address):
    """Delete a professor from the system.
    
    Args:
        email_address (str): The email address of the professor to delete.
    
    Returns:
        None
    
    Prints:
        Success message if deleted, or error message if professor not found.
    """
    if email_address in professors_dic:
        professor_name = professors_dic[email_address]['professor'].Name
        del professors_dic[email_address]
        save_professors_to_csv()  # Save professors to CSV after deleting professor 
        print(f"Professor {professor_name} deleted successfully.")
    else:
        print("Professor with this email does not exist.")

def modify_professor_details(email_address, Name=None, Rank=None):
    """Update a professor's name and/or rank.
    
    Args:
        email_address (str): The email address of the professor to update.
        Name (str, optional): New name for the professor. Defaults to None (no change).
        Rank (str, optional): New rank for the professor. Defaults to None (no change).
    
    Returns:
        None
    
    Prints:
        Success message if updated, or error message if professor not found.
    """
    if email_address in professors_dic:
        upt_professor = professors_dic[email_address]
        if Name:
            upt_professor["professor"].Name = Name
        if Rank:
            upt_professor["professor"].Rank = Rank
        save_professors_to_csv()  # Save professors to CSV after modifying details
        print(f"Professor {upt_professor['professor'].Name}'s details updated successfully.")
    else:
        print("Professor with this email does not exist.")

def assign_course_to_professor(email_address, Courses_id):
    """Assign a course to an existing professor.
    
    Args:
        email_address (str): The email address of the professor.
        Courses_id (str): The ID of the course to assign.
    
    Returns:
        None
    
    Prints:
        Success message if assigned, or error message if professor/course
        not found or professor already assigned to course.
    """
    if email_address not in professors_dic:
        print("Professor with this email does not exist.")
        return
    if Courses_id not in courses_dic:
        print(f"Course {Courses_id} does not exist. Please add the course first.")
        return

    courses = professors_dic[email_address]["courses"]
    for c in courses:
        if c["Courses_id"] == Courses_id:
            print(f"Professor is already assigned to {Courses_id}.")
            return
    courses.append({"Courses_id": Courses_id})
    save_professors_to_csv()  # Save professors to CSV after assigning course   
    print(f"Course {Courses_id} assigned to Professor {professors_dic[email_address]['professor'].Name} successfully.")

def delete_course_from_professor(email_address, Courses_id):
    """Remove a course assignment from a professor.
    
    Args:
        email_address (str): The email address of the professor.
        Courses_id (str): The ID of the course to remove.
    
    Returns:
        None
    
    Prints:
        Success message if removed, or error message if professor/course
        not found or professor not assigned to course.
    """
    if email_address not in professors_dic:
        print("Professor with this email does not exist.")
        return
    if Courses_id not in courses_dic:
        print(f"Course {Courses_id} does not exist. Please add the course first.")
        return

    courses = professors_dic[email_address]["courses"]
    for c in courses:
        if c["Courses_id"] == Courses_id:
            courses.remove(c)
            save_professors_to_csv()  # Save professors to CSV after deleting course assignment
            print(f"Course {Courses_id} removed from Professor {professors_dic[email_address]['professor'].Name} successfully.")
            return
    print(f"Professor is not assigned to {Courses_id}.")

def show_courses_details_by_professor(email_address):
    """Display all courses assigned to a professor with details.
    
    Args:
        email_address (str): The email address of the professor.
    
    Returns:
        None
    
    Prints:
        Professor's name and list of assigned courses with ID, name, and credits.
        Error message if professor not found.
    """
    if email_address in professors_dic:
        professor = professors_dic[email_address]['professor']
        print(f"Professor: {professor.Name}")
        courses = professors_dic[email_address]["courses"]
        if courses:
            print("Courses:")
            for c in courses:
                course_details = courses_dic[c['Courses_id']]
                print(f"  Course ID: {course_details.Course_id} | Course Name: {course_details.Course_name} | Credits: {course_details.Credits}")
        else:
            print("Courses: None")
    else:
        print("Professor with this email does not exist.")

def save_professors_to_csv():   
    rows = []
    for email, data in professors_dic.items():
        professor = data["professor"]
        courses = data["courses"]
        for c in courses:
            rows.append({
                "Email_address": email,
                "Name": professor.Name,
                "Rank": professor.Rank,
                "Courses_id": c["Courses_id"]
            })
    fieldnames = ["Email_address", "Name", "Rank", "Courses_id"]
    _write_csv(PROFESSORS_CSV, rows, fieldnames)

def load_professors_from_csv(): 
    rows = _read_csv(PROFESSORS_CSV)
    for row in rows:
        email = row["Email_address"]
        if email not in professors_dic:
            professor = Professor(row["Name"], email, row["Rank"])
            professors_dic[email] = {
                "professor": professor,
                "courses": []
            }
        professors_dic[email]["courses"].append({
            "Courses_id": row["Courses_id"]
        })


'''
Grades: Grade_id, Grade, Marks range
Functions:
display_grade_report()
add_grade()
delete_grade()
modify_grade()
'''



class Grade():
    """Manages the grade scale and grade assignments.
    
    Attributes:
        _grade_table (list): Array of dictionaries storing grade information
                           (Grade_id, Grade letter, Min_marks, Max_marks).
    """

    # Array to store grade information
    _grade_table = [
        {"Grade_id": "1", "Grade": "A", "Min_marks": 90, "Max_marks": 100},
        {"Grade_id": "2", "Grade": "B", "Min_marks": 80, "Max_marks": 89},
        {"Grade_id": "3", "Grade": "C", "Min_marks": 70, "Max_marks": 79},
        {"Grade_id": "4", "Grade": "D", "Min_marks": 60, "Max_marks": 69},
        {"Grade_id": "5", "Grade": "F", "Min_marks": 0, "Max_marks": 59}
    ]
    
    def display_grade_report(self):
        """Display the complete grade scale.
        
        Prints all grades in the system with their ID, letter, and marks range.
        
        Returns:
            None
        """
        print("Grade Report:")
        for grade in self._grade_table:
            print(f"Grade ID: {grade['Grade_id']} | Grade: {grade['Grade']} \
                  | Marks Range: {grade['Min_marks']}-{grade['Max_marks']}")

    def add_grade(self, Grade_id, Grade, Min_marks, Max_marks):
        """Add a new grade to the grading scale.
        
        Args:
            Grade_id (str): Unique identifier for the grade.
            Grade (str): The letter grade (e.g., 'A', 'B', 'C').
            Min_marks (int): Minimum marks required for this grade.
            Max_marks (int): Maximum marks for this grade.
        
        Returns:
            None
        
        Prints:
            Success message if added, or error message if grade ID already exists.
        """
        for grade in self._grade_table:
            if grade["Grade_id"] == Grade_id:
                print("Grade with this ID already exists.")
                return
        self._grade_table.append({
            "Grade_id": Grade_id,
            "Grade": Grade,
            "Min_marks": Min_marks,
            "Max_marks": Max_marks
        })
        print(f"Grade {Grade} added successfully.")

    def delete_grade(self, Grade_id):
        """Remove a grade from the grading scale.
        
        Args:
            Grade_id (str): The ID of the grade to delete.
        
        Returns:
            None
        
        Prints:
            Success message if deleted, or error message if grade not found.
        """
        for grade in self._grade_table:
            if grade["Grade_id"] == Grade_id:
                self._grade_table.remove(grade)
                print(f"Grade {grade['Grade']} deleted successfully.")
                return
        print("Grade with this ID does not exist.") 

    def modify_grade(self, Grade_id, Grade=None, Min_marks=None, Max_marks=None):
        """Update a grade's letter and/or marks range.
        
        Args:
            Grade_id (str): The ID of the grade to modify.
            Grade (str, optional): New letter grade. Defaults to None (no change).
            Min_marks (int, optional): New minimum marks. Defaults to None (no change).
            Max_marks (int, optional): New maximum marks. Defaults to None (no change).
        
        Returns:
            None
        
        Prints:
            Success message if modified, or error message if grade not found.
        """
        for grade in self._grade_table:
            if grade["Grade_id"] == Grade_id:
                if Grade:
                    grade["Grade"] = Grade
                if Min_marks is not None:
                    grade["Min_marks"] = Min_marks
                if Max_marks is not None:
                    grade["Max_marks"] = Max_marks
                print(f"Grade {grade['Grade']} modified successfully.")
                return
        print("Grade with this ID does not exist.")

    
    def get_grade_by_marks(self, marks):
        """Get the letter grade for a given marks value.
        
        Args:
            marks (int or float): The marks to look up.
        
        Returns:
            str: The corresponding letter grade, or error message if not found.
        """
        for grade in self._grade_table:
            if grade["Min_marks"] <= marks <= grade["Max_marks"]:
                return grade["Grade"]
        return "Grade not found for the given marks."
    
grades = Grade()

'''
LoginUser: Email_id, password
Functions:
login()
logout()
change_password()
encrypt_password()
decrypt_password()
'''
login_dic = {}

class LoginUser():
    """Manages user authentication and registration.
    
    Attributes:
        _LOGIN_FIELDS (list): List of field names for login records.
    """

    _LOGIN_FIELDS = ["Email_id", "Password", "role"]

    def register(self, Email_id, Password, role="student"):
        """Register a new user in the system.
        
        Args:
            Email_id (str): The user's email address.
            Password (str): The user's password (will be encrypted).
            role (str, optional): The user's role. Defaults to 'student'.
                                Possible values: 'student', 'professor', 'admin'.
        
        Returns:
            None
        
        Prints:
            Success message if registered, or error message if email already exists.
        """
        if Email_id in login_dic:
            print("User with this email already exists.")
            return
        encrypted_password = _cipher.encrypt(Password)
        login_dic[Email_id] = {"Password": encrypted_password, "role": role}
        save_login_to_csv()  # Save login records to CSV after registering new user
        print(f"User {Email_id} registered successfully as {role}.")


    def login(self, Email_id, Password):
        """Authenticate a user with email and password.
        
        Args:
            Email_id (str): The user's email address.
            Password (str): The user's password (will be compared with encrypted version).
        
        Returns:
            bool: True if login successful, False otherwise.
        
        Prints:
            Success or error message based on authentication result.
        """
        if Email_id not in login_dic:
            print("User with this email does not exist.")
            return False
        encrypted_password = login_dic[Email_id]["Password"]
        decrypted_password = _cipher.decrypt(encrypted_password)
        if Password == decrypted_password:
            print(f"User {Email_id} logged in successfully.")
            return True
        else:
            print("Incorrect password.")
            return False
        
    def logout(self, Email_id):
        """Log out a user from the system.
        
        Args:
            Email_id (str): The email address of the user to log out.
        
        Returns:
            None
        
        Prints:
            Logout confirmation message.
        """
        print(f"User {Email_id} logged out successfully.")
    
    def change_password(self, Email_id, old_password, new_password):
        """Change a user's password.
        
        Args:
            Email_id (str): The user's email address.
            old_password (str): The user's current password (must be correct).
            new_password (str): The new password to set.
        
        Returns:
            bool: True if password changed successfully, False otherwise.
        
        Prints:
            Success message if password changed, or error message if old password
            is incorrect or user not found.
        """
        if Email_id not in login_dic:
            print("User with this email does not exist.")
            return False
        encrypted_password = login_dic[Email_id]["Password"]
        decrypted_password = _cipher.decrypt(encrypted_password)
        if old_password == decrypted_password:
            new_encrypted_password = _cipher.encrypt(new_password)
            login_dic[Email_id]["Password"] = new_encrypted_password
            save_login_to_csv()  # Save login records to CSV after changing password
            print(f"Password for user {Email_id} changed successfully.")
            return True
        else:
            print("Incorrect old password.")
            return False    

login_user = LoginUser()

def save_login_to_csv():   
    rows = []
    for email, data in login_dic.items():
        rows.append({
            "User_id": email,
            "Password": data["Password"],
            "role": data["role"]
        })
    fieldnames = ["User_id", "Password", "role"]
    _write_csv(LOGIN_CSV, rows, fieldnames)

def load_login_from_csv():
    rows = _read_csv(LOGIN_CSV)
    for row in rows:
        email = row["User_id"]
        login_dic[email] = {
            "Password": row["Password"],
            "role": row["role"]
        }

def report_by_course(Course_id):
    """Generate and display a report for a specific course.
    
    Displays all students enrolled in the course with their grades and marks,
    and includes course statistics.
    
    Args:
        Course_id (str): The ID of the course to generate report for.
    
    Returns:
        None
    
    Prints:
        Course report with student details and statistics, or error message
        if course not found or no students enrolled.
    """
    if Course_id not in courses_dic:
        print(f"Course {Course_id} does not exist.")
        return
    found = False
    print(f"Report for Course {Course_id}:")
    for student_email in student_list.to_list():
        student = students_dic[student_email]["student"]
        for c in students_dic[student_email]["courses"]:
            if c["Courses_id"] == Course_id:
                print(f"Student: {student.FirstName} {student.LastName} | Grade: {c['Grades']} | Marks: {c['marks']}")
                found = True
    
    if not found:   
        print(f"No students enrolled in course {Course_id}.")
    else:
        calculate_course_statistics(Course_id)


def report_by_professor(email_address):
    """Generate and display a report for a specific professor.
    
    Displays all courses assigned to the professor and generates course
    reports with student enrollment for each course.
    
    Args:
        email_address (str): The email address of the professor.
    
    Returns:
        None
    
    Prints:
        Professor report with course details and student enrollments,
        or error message if professor not found or no courses assigned.
    """
    if email_address not in professors_dic:
        print("Professor with this email does not exist.")
        return
    professor = professors_dic[email_address]['professor']
    print(f"Report for Professor {professor.Name}:")
    courses = professors_dic[email_address]["courses"]
    if courses:
        for c in courses:
            course_details = courses_dic[c['Courses_id']]
            print(f"Course ID: {course_details.Course_id} | Course Name: {course_details.Course_name} | Credits: {course_details.Credits}")
            report_by_course(course_details.Course_id)
    else:
        print("No courses assigned to this professor.")


def report_by_student(email_address):
    """Generate and display a report for a specific student.
    
    Displays all courses enrolled by the student with course details,
    grades, and marks.
    
    Args:
        email_address (str): The email address of the student.
    
    Returns:
        None
    
    Prints:
        Student report with course enrollment details and grades,
        or error message if student not found or not enrolled in any courses.
    """
    if email_address not in students_dic:
        print("Student with this email does not exist.")
        return
    student = students_dic[email_address]['student']
    print(f"Report for Student {student.FirstName} {student.LastName}:")
    courses = students_dic[email_address]["courses"]
    if courses:
        for c in courses:
            course_details = courses_dic[c['Courses_id']]
            print(f"Course ID: {course_details.Course_id} | Course Name: {course_details.Course_name} | Credits: {course_details.Credits} | Grade: {c['Grades']} | Marks: {c['marks']}")
    else:
        print("No courses enrolled for this student.")



def initialize_system():
    """Initialize the system by loading data from CSV files.
    
    Loads students, courses, professors, and login records from their
    respective CSV files into the system's data structures.
    
    Returns:
        None
    
    Prints:
        Confirmation message after loading data.
    """
    load_students_from_csv()
    load_courses_from_csv()
    load_professors_from_csv()
    load_login_from_csv()
    print("System initialized with data from CSV files.")



if __name__ == '__main__':
    # Initialize application (load data from CSV files)
    initialize_system()
    
    # Example usage
    print("=" * 70)
    print("CHECKMYGRADE APPLICATION - DEMO")
    print("=" * 70)
    
    # Add some courses
    print("\n--- Adding Courses ---")
    add_new_course("DATA200", "3", "Data Science", "Provides insight about DS and Python")
    add_new_course("CS100", "3", "Introduction to Computer Science")
    
    # Add professors
    print("\n--- Adding Professors ---")
    add_new_professor("Paramdeep Saini", "paramdeep@sjsu.edu", "Senior Professor", "DATA200")
    add_new_professor("Jane Smith", "jane@sjsu.edu", "Associate Professor", "CS100")
    
    # Register users
    print("\n--- Registering Users ---")
    login_user.register("sam@sjsu.edu", "Welcome12#_", "student")
    login_user.register("john@sjsu.edu", "SecurePass123!", "student")
    
    # Add students
    print("\n--- Adding Students ---")
    add_new_student("Sam", "Carpenter", "sam@sjsu.edu", "DATA200", "A", 96)
    add_new_student("John", "Doe", "john@sjsu.edu", "DATA200", "B", 85)
    add_new_student("Jane", "Johnson", "jane.j@sjsu.edu", "CS100", "A", 92)
    
    # Enroll in additional course
    print("\n--- Enrolling Students in Courses ---")
    enroll_course("sam@sjsu.edu", "CS100", "A", 94)
    
    # Display records
    print("\n--- Displaying Records ---")
    students_dic["sam@sjsu.edu"]["student"].display_records()
    print()
    students_dic["john@sjsu.edu"]["student"].display_records()
    
    # Search
    print("\n--- Searching for Student ---")
    search_student_by_email("sam@sjsu.edu")
    
    # Sort
    print("\n--- Sorting Students ---")
    sorted_students = sort_students_by_last_name()
    print("Sorted by last name:")
    for student in sorted_students:
        print(f"  {student.FirstName} {student.LastName}")
    
    # Reports
    print("\n--- Course Report ---")
    report_by_course("DATA200")
    
    print("\n--- Professor Report ---")
    report_by_professor("paramdeep@sjsu.edu")
    
    print("\n--- Student Report ---")
    report_by_student("sam@sjsu.edu")
    
    print("\n" + "=" * 70)
    print("All data has been saved to CSV files.")
    print("=" * 70)