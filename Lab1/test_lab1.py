import unittest
import time
import os
import sys

# Import the lab1 module
import lab1


class TestStudentOperations(unittest.TestCase):
    """Test cases for student-related operations."""
    
    def setUp(self):
        """Clear dictionaries and initialize before each test."""
        lab1.students_dic.clear()
        lab1.student_list = lab1.LinkedList()
        lab1.courses_dic.clear()
        lab1.professors_dic.clear()
        lab1.login_dic.clear()
        
        # Add test courses that tests depend on
        lab1.add_new_course("TEST101", "3", "Test Course", "For testing purposes")
        lab1.add_new_course("TEST102", "3", "Another Test Course", "For more testing")
    
    def tearDown(self):
        """Clean up after each test."""
        pass
    
    # ========================================================================
    # SECTION 1: STUDENT ADDITION/DELETION/MODIFICATION TESTS
    # ========================================================================
    
    def test_01_add_single_student(self):
        """Test adding a single student to the system."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        
        self.assertIn("john@test.edu", lab1.students_dic)
        student = lab1.students_dic["john@test.edu"]["student"]
        self.assertEqual(student.FirstName, "John")
        self.assertEqual(student.LastName, "Doe")
        self.assertEqual(student.email_address, "john@test.edu")
    
    def test_02_add_duplicate_student(self):
        """Test that duplicate email cannot be added."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        initial_size = len(lab1.students_dic)
        
        # Try to add student with same email
        lab1.add_new_student("Jane", "Smith", "john@test.edu", "TEST101", "B", "85")
        
        # Size should not change
        self.assertEqual(len(lab1.students_dic), initial_size)
    
    def test_03_add_student_nonexistent_course(self):
        """Test that student cannot be added to non-existent course."""
        initial_size = len(lab1.students_dic)
        lab1.add_new_student("John", "Doe", "john@test.edu", "FAKE999", "A", "95")
        
        # Student should not be added
        self.assertEqual(len(lab1.students_dic), initial_size)
    
    def test_04_delete_student(self):
        """Test deleting a student from the system."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        initial_size = len(lab1.students_dic)
        
        lab1.delete_student("john@test.edu")
        
        self.assertNotIn("john@test.edu", lab1.students_dic)
        self.assertEqual(len(lab1.students_dic), initial_size - 1)
    
    def test_05_delete_nonexistent_student(self):
        """Test deleting a student that doesn't exist."""
        initial_size = len(lab1.students_dic)
        lab1.delete_student("nonexistent@test.edu")
        
        # Size should not change
        self.assertEqual(len(lab1.students_dic), initial_size)
    
    def test_06_update_student_record(self):
        """Test updating a student's record (name, grades, marks)."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        
        lab1.update_student_record("john@test.edu", "TEST101", 
                                    FirstName="Jonathan", Grades="B", marks="85")
        
        student = lab1.students_dic["john@test.edu"]["student"]
        self.assertEqual(student.FirstName, "Jonathan")
        
        courses = lab1.students_dic["john@test.edu"]["courses"]
        self.assertEqual(courses[0]["Grades"], "B")
        self.assertEqual(courses[0]["marks"], "85")
    
    def test_07_enroll_student_in_course(self):
        """Test enrolling a student in an additional course."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        initial_courses = len(lab1.students_dic["john@test.edu"]["courses"])
        
        # Enroll in second course
        lab1.enroll_course("john@test.edu", "TEST102", "B", "88")
        
        self.assertEqual(len(lab1.students_dic["john@test.edu"]["courses"]), initial_courses + 1)
        self.assertTrue(any(c["Courses_id"] == "TEST102" 
                           for c in lab1.students_dic["john@test.edu"]["courses"]))
    
    def test_08_enroll_duplicate_course(self):
        """Test that student cannot enroll twice in same course."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        initial_course_count = len(lab1.students_dic["john@test.edu"]["courses"])
        
        lab1.enroll_course("john@test.edu", "TEST101", "B", "85")
        
        # Course count should not change
        self.assertEqual(len(lab1.students_dic["john@test.edu"]["courses"]), initial_course_count)
    
    # ========================================================================
    # SECTION 2: LARGE-SCALE STUDENT TESTING (1000+ RECORDS)
    # ========================================================================
    
    def test_10_add_1000_students(self):
        """
        SPECIFICATION REQUIREMENT: Test adding 1000 students and verify count.
        
        This test demonstrates the system's ability to handle large datasets
        with proper addition of 1000+ student records.
        """
        print("\n" + "="*70)
        print("TEST 10: ADDING 1000 STUDENTS")
        print("="*70)
        
        start_time = time.perf_counter()
        
        # Add 1000 students with varying data
        for i in range(1000):
            first_name = f"Student{i}"
            last_name = f"Last{i}"
            email = f"student{i}@test.edu"
            marks = str(50 + (i % 50))  # Marks between 50-99 as string
            grade = "A" if int(marks) >= 90 else "B" if int(marks) >= 80 else "C" if int(marks) >= 70 else "D"
            
            lab1.add_new_student(first_name, last_name, email, "TEST101", grade, marks)
        
        elapsed = time.perf_counter() - start_time
        
        # Verify all students were added
        self.assertEqual(len(lab1.students_dic), 1000)
        self.assertEqual(lab1.student_list.size(), 1000)
        
        print(f"✓ Successfully added 1000 students")
        print(f"✓ Time taken: {elapsed:.3f} seconds")
        print(f"✓ Average time per student: {elapsed/1000*1000:.3f} ms")
        print("="*70 + "\n")
    
    def test_11_verify_1000_students_accessible(self):
        """Verify that all 1000 students can be accessed from LinkedList."""
        # First add 1000 students
        for i in range(1000):
            lab1.add_new_student(f"Student{i}", f"Last{i}", 
                               f"student{i}@test.edu", "TEST101", "A", "90")
        
        # Convert linked list to regular list
        emails = lab1.student_list.to_list()
        
        # Verify we have exactly 1000 emails in the linked list
        self.assertEqual(len(emails), 1000)
        
        # Verify we can access each student (sample check)
        for i in range(0, 1000, 100):  # Check every 100th student
            email = f"student{i}@test.edu"
            self.assertIn(email, emails)
            self.assertIn(email, lab1.students_dic)
    
    # ========================================================================
    # SECTION 3: SEARCH FUNCTIONALITY WITH TIMING
    # ========================================================================
    
    def test_20_search_student_by_email_single(self):
        """Test searching for a student by email address."""
        lab1.add_new_student("John", "Doe", "john@test.edu", "TEST101", "A", "95")
        
        result = lab1.search_student_by_email("john@test.edu")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.FirstName, "John")
    
    def test_21_search_nonexistent_student(self):
        """Test searching for a non-existent student."""
        result = lab1.search_student_by_email("fake@test.edu")
        self.assertIsNone(result)
    
    def test_22_search_performance_1000_records_middle(self):
        """
        SPECIFICATION REQUIREMENT: Test search performance with 1000 records.
        Search for student in middle of dataset and print timing.
        """
        print("\n" + "="*70)
        print("TEST 22: SEARCH PERFORMANCE WITH 1000 RECORDS (MIDDLE)")
        print("="*70)
        
        # Add 1000 students
        for i in range(1000):
            lab1.add_new_student(f"Student{i}", f"Last{i}", 
                               f"student{i}@test.edu", "TEST101", "A", "90")
        
        # Search for student in the middle
        start_time = time.perf_counter()
        result = lab1.search_student_by_email("student500@test.edu")
        elapsed = time.perf_counter() - start_time
        
        self.assertIsNotNone(result)
        
        print(f"✓ Search for middle record (student500)")
        print(f"✓ Time taken: {elapsed:.6f} seconds")
        print(f"✓ Time in microseconds: {elapsed*1000000:.2f} µs")
        print("="*70 + "\n")
    
    def test_23_search_performance_1000_records_last(self):
        """
        SPECIFICATION REQUIREMENT: Test search for last student in 1000 records.
        Demonstrates O(1) performance even for worst-case scenario.
        """
        print("\n" + "="*70)
        print("TEST 23: SEARCH PERFORMANCE WITH 1000 RECORDS (LAST)")
        print("="*70)
        
        # Add 1000 students
        for i in range(1000):
            lab1.add_new_student(f"Student{i}", f"Last{i}", 
                               f"student{i}@test.edu", "TEST101", "A", "90")
        
        # Search for last student (worst case for linear search, but O(1) for dict)
        start_time = time.perf_counter()
        result = lab1.search_student_by_email("student999@test.edu")
        elapsed = time.perf_counter() - start_time
        
        self.assertIsNotNone(result)
        
        print(f"✓ Search for last record (student999)")
        print(f"✓ Time taken: {elapsed:.6f} seconds")
        print(f"✓ Time in microseconds: {elapsed*1000000:.2f} µs")
        print("="*70 + "\n")
    
    def test_24_search_performance_1000_records_first(self):
        """Test search for first student in 1000 records."""
        # Add 1000 students
        for i in range(1000):
            lab1.add_new_student(f"Student{i}", f"Last{i}", 
                               f"student{i}@test.edu", "TEST101", "A", "90")
        
        # Search for first student
        start_time = time.perf_counter()
        result = lab1.search_student_by_email("student0@test.edu")
        elapsed = time.perf_counter() - start_time
        
        self.assertIsNotNone(result)
        
        print(f"\n✓ Search for first record (student0)")
        print(f"✓ Time taken: {elapsed:.6f} seconds")
        print(f"✓ This demonstrates O(1) dictionary lookup performance")
    
    # ========================================================================
    # SECTION 4: SORT FUNCTIONALITY WITH TIMING
    # ========================================================================
    
    def test_30_sort_by_last_name_ascending(self):
        """Test sorting students by last name in ascending order."""
        lab1.add_new_student("Charlie", "Brown", "charlie@test.edu", "TEST101", "A", "90")
        lab1.add_new_student("Alice", "Adams", "alice@test.edu", "TEST101", "A", "95")
        lab1.add_new_student("Bob", "Baker", "bob@test.edu", "TEST101", "B", "85")
        
        sorted_students = lab1.sort_students_by_last_name()
        
        # Verify sorted order (Adams, Baker, Brown)
        self.assertEqual(sorted_students[0].LastName, "Adams")
        self.assertEqual(sorted_students[1].LastName, "Baker")
        self.assertEqual(sorted_students[2].LastName, "Brown")
    
    def test_31_sort_by_grade_ascending(self):
        """Test sorting students by grade (marks) in ascending order."""
        lab1.add_new_student("Charlie", "Brown", "charlie@test.edu", "TEST101", "A", "85")
        lab1.add_new_student("Alice", "Adams", "alice@test.edu", "TEST101", "A", "95")
        lab1.add_new_student("Bob", "Baker", "bob@test.edu", "TEST101", "B", "75")
        
        sorted_students = lab1.sort_students_by_grade("TEST101")
        
        # Verify sorted order by marks (75, 85, 95)
        marks_list = [float(lab1.students_dic[s.email_address]["courses"][0]["marks"]) 
                     for s in sorted_students]
        self.assertEqual(marks_list, sorted(marks_list))
    
    def test_32_sort_by_email_ascending(self):
        """Test sorting students by email address."""
        lab1.add_new_student("Charlie", "Brown", "charlie@test.edu", "TEST101", "A", "90")
        lab1.add_new_student("Alice", "Adams", "alice@test.edu", "TEST101", "A", "95")
        lab1.add_new_student("Bob", "Baker", "bob@test.edu", "TEST101", "B", "85")
        
        sorted_students = lab1.sort_students_by_email()
        
        # Verify sorted by email
        email_list = [s.email_address for s in sorted_students]
        self.assertEqual(email_list, sorted(email_list))
    
    def test_33_sort_1000_students_by_name_with_timing(self):
        """
        SPECIFICATION REQUIREMENT: Test sorting 1000 students by name.
        Include timing measurement in output.
        """
        print("\n" + "="*70)
        print("TEST 33: SORTING 1000 STUDENTS BY LAST NAME")
        print("="*70)
        
        # Add 1000 students with reverse-sorted names
        for i in range(1000):
            lab1.add_new_student(f"Student{i}", f"Last{1000-i}", 
                               f"student{i}@test.edu", "TEST101", "A", "90")
        
        # Sort by name
        start_time = time.perf_counter()
        sorted_students = lab1.sort_students_by_last_name()
        elapsed = time.perf_counter() - start_time
        
        self.assertEqual(len(sorted_students), 1000)
        
        # Verify sorted
        last_names = [s.LastName for s in sorted_students]
        self.assertEqual(last_names, sorted(last_names))
        
        print(f"✓ Successfully sorted 1000 students by last name")
        print(f"✓ Time taken: {elapsed:.3f} seconds")
        print(f"✓ Algorithm: O(n log n) - Python Timsort")
        print("="*70 + "\n")
    
    def test_34_sort_1000_students_by_marks_with_timing(self):
        """
        SPECIFICATION REQUIREMENT: Test sorting 1000 students by marks.
        Include timing measurement in output.
        """
        print("\n" + "="*70)
        print("TEST 34: SORTING 1000 STUDENTS BY MARKS (GRADE)")
        print("="*70)
        
        # Add 1000 students with varying marks
        for i in range(1000):
            marks = str(50 + (i % 50))  # Marks between 50-99
            lab1.add_new_student(f"Student{i}", f"Last{i}", 
                               f"student{i}@test.edu", "TEST101", "A", marks)
        
        # Sort by grade
        start_time = time.perf_counter()
        sorted_students = lab1.sort_students_by_grade("TEST101")
        elapsed = time.perf_counter() - start_time
        
        self.assertEqual(len(sorted_students), 1000)
        
        # Verify sorted
        marks_list = [float(lab1.students_dic[s.email_address]["courses"][0]["marks"]) 
                     for s in sorted_students]
        self.assertEqual(marks_list, sorted(marks_list))
        
        print(f"✓ Successfully sorted 1000 students by marks")
        print(f"✓ Time taken: {elapsed:.3f} seconds")
        print(f"✓ Algorithm: O(n log n) - Python Timsort")
        print("="*70 + "\n")
    
    def test_35_sort_1000_students_by_email_with_timing(self):
        """Test sorting 1000 students by email with timing."""
        # Add 1000 students
        for i in range(1000):
            lab1.add_new_student(f"Student{i}", f"Last{i}", 
                               f"student{i}@test.edu", "TEST101", "A", "90")
        
        # Sort by email
        start_time = time.perf_counter()
        sorted_students = lab1.sort_students_by_email()
        elapsed = time.perf_counter() - start_time
        
        self.assertEqual(len(sorted_students), 1000)
        
        print(f"\n✓ Sorted 1000 students by email")
        print(f"✓ Time taken: {elapsed:.3f} seconds")


class TestCourseOperations(unittest.TestCase):
    """Test cases for course-related operations."""
    
    def setUp(self):
        """Clear dictionaries before each test."""
        lab1.courses_dic.clear()
        lab1.students_dic.clear()
        lab1.student_list = lab1.LinkedList()
        lab1.professors_dic.clear()
    
    # ========================================================================
    # SECTION 5: COURSE OPERATIONS (Add/Delete/Modify)
    # ========================================================================
    
    def test_40_add_course(self):
        """Test adding a new course."""
        lab1.add_new_course("CS101", "3", "Introduction to CS", "Basic CS concepts")
        
        self.assertIn("CS101", lab1.courses_dic)
        course = lab1.courses_dic["CS101"]
        self.assertEqual(course.Course_id, "CS101")
        self.assertEqual(course.Course_name, "Introduction to CS")
    
    def test_41_add_duplicate_course(self):
        """Test that duplicate course ID cannot be added."""
        lab1.add_new_course("CS101", "3", "Introduction to CS")
        initial_size = len(lab1.courses_dic)
        
        lab1.add_new_course("CS101", "4", "Another CS Course")
        
        # Size should not change
        self.assertEqual(len(lab1.courses_dic), initial_size)
    
    def test_42_delete_course(self):
        """Test deleting a course."""
        lab1.add_new_course("CS101", "3", "Introduction to CS")
        initial_size = len(lab1.courses_dic)
        
        lab1.delete_course("CS101")
        
        self.assertNotIn("CS101", lab1.courses_dic)
        self.assertEqual(len(lab1.courses_dic), initial_size - 1)
    
    def test_43_delete_nonexistent_course(self):
        """Test deleting a course that doesn't exist."""
        initial_size = len(lab1.courses_dic)
        lab1.delete_course("FAKE999")
        
        # Size should not change
        self.assertEqual(len(lab1.courses_dic), initial_size)
    
    def test_44_update_course(self):
        """Test updating course details."""
        lab1.add_new_course("CS101", "3", "Introduction to CS")
        
        result = lab1.update_course("CS101", Credits="4", 
                                   Course_name="Advanced CS",
                                   description="Advanced concepts")
        
        self.assertTrue(result)
        course = lab1.courses_dic["CS101"]
        self.assertEqual(course.Credits, "4")
        self.assertEqual(course.Course_name, "Advanced CS")
    
    def test_45_update_nonexistent_course(self):
        """Test updating a course that doesn't exist."""
        result = lab1.update_course("FAKE999", Credits="4")
        self.assertFalse(result)
    
    def test_46_delete_course_cascading(self):
        """Test that deleting a course removes it from students and professors."""
        # Setup
        lab1.add_new_course("CS101", "3", "Introduction to CS")
        lab1.add_new_student("John", "Doe", "john@test.edu", "CS101", "A", "95")
        lab1.add_new_professor("Jane", "jane@test.edu", "Professor", "CS101")
        
        # Delete course
        lab1.delete_course("CS101")
        
        # Verify removed from student
        if "john@test.edu" in lab1.students_dic:
            self.assertEqual(len(lab1.students_dic["john@test.edu"]["courses"]), 0)
        
        # Verify removed from professor
        if "jane@test.edu" in lab1.professors_dic:
            self.assertEqual(len(lab1.professors_dic["jane@test.edu"]["courses"]), 0)


class TestProfessorOperations(unittest.TestCase):
    """Test cases for professor-related operations."""
    
    def setUp(self):
        """Clear dictionaries before each test."""
        lab1.professors_dic.clear()
        lab1.courses_dic.clear()
        lab1.students_dic.clear()
        lab1.student_list = lab1.LinkedList()
        
        # Add test course
        lab1.add_new_course("CS101", "3", "Introduction to CS")
    
    # ========================================================================
    # SECTION 6: PROFESSOR OPERATIONS (Add/Delete/Modify)
    # ========================================================================
    
    def test_50_add_professor(self):
        """Test adding a new professor."""
        lab1.add_new_professor("John", "john@test.edu", "Senior Professor", "CS101")
        
        self.assertIn("john@test.edu", lab1.professors_dic)
        professor = lab1.professors_dic["john@test.edu"]["professor"]
        self.assertEqual(professor.Name, "John")
        self.assertEqual(professor.Rank, "Senior Professor")
    
    def test_51_add_duplicate_professor(self):
        """Test that duplicate professor email cannot be added."""
        lab1.add_new_professor("John", "john@test.edu", "Senior Professor", "CS101")
        initial_size = len(lab1.professors_dic)
        
        lab1.add_new_professor("Jane", "john@test.edu", "Associate Professor", "CS101")
        
        # Size should not change
        self.assertEqual(len(lab1.professors_dic), initial_size)
    
    def test_52_delete_professor(self):
        """Test deleting a professor."""
        lab1.add_new_professor("John", "john@test.edu", "Senior Professor", "CS101")
        initial_size = len(lab1.professors_dic)
        
        lab1.delete_professor("john@test.edu")
        
        self.assertNotIn("john@test.edu", lab1.professors_dic)
        self.assertEqual(len(lab1.professors_dic), initial_size - 1)
    
    def test_53_delete_nonexistent_professor(self):
        """Test deleting a professor that doesn't exist."""
        initial_size = len(lab1.professors_dic)
        lab1.delete_professor("fake@test.edu")
        
        # Size should not change
        self.assertEqual(len(lab1.professors_dic), initial_size)
    
    def test_54_modify_professor_details(self):
        """Test modifying professor details (name and rank)."""
        lab1.add_new_professor("John", "john@test.edu", "Senior Professor", "CS101")
        
        lab1.modify_professor_details("john@test.edu", Name="Jonathan", Rank="Full Professor")
        
        professor = lab1.professors_dic["john@test.edu"]["professor"]
        self.assertEqual(professor.Name, "Jonathan")
        self.assertEqual(professor.Rank, "Full Professor")
    
    def test_55_modify_nonexistent_professor(self):
        """Test modifying a professor that doesn't exist."""
        initial_size = len(lab1.professors_dic)
        lab1.modify_professor_details("fake@test.edu", Name="Fake")
        
        # Size should not change
        self.assertEqual(len(lab1.professors_dic), initial_size)
    
    def test_56_assign_course_to_professor(self):
        """Test assigning a course to a professor."""
        # Add another course
        lab1.add_new_course("CS102", "3", "Data Structures")
        
        lab1.add_new_professor("John", "john@test.edu", "Senior Professor", "CS101")
        initial_courses = len(lab1.professors_dic["john@test.edu"]["courses"])
        
        # Assign second course
        lab1.assign_course_to_professor("john@test.edu", "CS102")
        
        self.assertEqual(len(lab1.professors_dic["john@test.edu"]["courses"]), initial_courses + 1)
        self.assertTrue(any(c["Courses_id"] == "CS102" 
                           for c in lab1.professors_dic["john@test.edu"]["courses"]))
    
    def test_57_delete_course_from_professor(self):
        """Test removing a course from a professor."""
        lab1.add_new_professor("John", "john@test.edu", "Senior Professor", "CS101")
        initial_courses = len(lab1.professors_dic["john@test.edu"]["courses"])
        
        lab1.delete_course_from_professor("john@test.edu", "CS101")
        
        self.assertEqual(len(lab1.professors_dic["john@test.edu"]["courses"]), initial_courses - 1)


class TestCSVPersistence(unittest.TestCase):
    """Test cases for CSV file persistence and loading."""
    
    def setUp(self):
        """Clear dictionaries before each test."""
        lab1.students_dic.clear()
        lab1.student_list = lab1.LinkedList()
        lab1.courses_dic.clear()
        lab1.professors_dic.clear()
        lab1.login_dic.clear()
    
    def test_60_csv_files_created_after_operations(self):
        """
        SPECIFICATION REQUIREMENT: Verify CSV files are created after operations.
        """
        print("\n" + "="*70)
        print("TEST 60: CSV FILE CREATION AND PERSISTENCE")
        print("="*70)
        
        # Add data
        lab1.add_new_course("CS101", "3", "CS Course")
        lab1.add_new_student("John", "Doe", "john@test.edu", "CS101", "A", "95")
        lab1.add_new_professor("Jane", "jane@test.edu", "Professor", "CS101")
        lab1.login_user.register("john@test.edu", "password123", "student")
        
        # Check that CSV files exist
        self.assertTrue(os.path.exists(lab1.STUDENTS_CSV), "students.csv not created")
        self.assertTrue(os.path.exists(lab1.COURSES_CSV), "courses.csv not created")
        self.assertTrue(os.path.exists(lab1.PROFESSORS_CSV), "professors.csv not created")
        self.assertTrue(os.path.exists(lab1.LOGIN_CSV), "login.csv not created")
        
        print(f"✓ All CSV files created successfully:")
        print(f"  - {lab1.STUDENTS_CSV}")
        print(f"  - {lab1.COURSES_CSV}")
        print(f"  - {lab1.PROFESSORS_CSV}")
        print(f"  - {lab1.LOGIN_CSV}")
        print("="*70 + "\n")
    
    def test_61_load_students_from_csv(self):
        """
        SPECIFICATION REQUIREMENT: Load data from CSV files saved in previous runs.
        """
        print("\n" + "="*70)
        print("TEST 61: LOADING DATA FROM CSV FILES")
        print("="*70)
        
        # First, add and save data
        lab1.add_new_course("CS101", "3", "CS Course")
        lab1.add_new_student("John", "Doe", "john@test.edu", "CS101", "A", "95")
        lab1.add_new_student("Jane", "Smith", "jane@test.edu", "CS101", "B", "85")
        
        # Clear dictionaries to simulate program restart
        original_count = len(lab1.students_dic)
        lab1.students_dic.clear()
        lab1.student_list = lab1.LinkedList()
        
        # Load from CSV
        lab1.load_students_from_csv()
        
        # Verify data was loaded
        self.assertEqual(len(lab1.students_dic), original_count)
        self.assertIn("john@test.edu", lab1.students_dic)
        self.assertIn("jane@test.edu", lab1.students_dic)
        
        print(f"✓ Data successfully loaded from CSV")
        print(f"✓ Students loaded: {len(lab1.students_dic)}")
        print("="*70 + "\n")


def run_all_tests_with_summary():
    """Run all tests and display summary with execution times."""
    print("\n" + "="*70)
    print("CHECKMYGRADE APPLICATION - COMPREHENSIVE UNIT TESTS")
    print("DATA 200 Lab 1 - Full Test Suite")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStudentOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCourseOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestProfessorOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVPersistence))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED")
    
    print("="*70 + "\n")
    
    return result


if __name__ == '__main__':
    # Run tests with summary
    result = run_all_tests_with_summary()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
