"""
Student Performance Analysis System
Demonstrates: classes/objects, encapsulation, abstraction, inheritance,
polymorphism, method overriding, composition and flexible method interfaces.
"""

import csv
from abc import ABC, abstractmethod

SCHOLARSHIP_THRESHOLD = 85  # minimum average for scholarship eligibility


# ---------------------------------------------------------------------------
# TASK 2: The main student class that other student types build on

# ---------------------------------------------------------------------------
class Student(ABC):
    """Abstract base class. Cannot be instantiated directly."""

    SUBJECTS = ("Math", "English", "Science")

    def __init__(self, student_id, first_name, last_name, programme, marks):
        # the underscore tells other programmers not to touch these directly 
       # Use getters and setters below instead
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme
        self._marks = {}
        self.set_marks(marks)  # goes through validation

    # ---- Controlled access (getters/setters) ----
    @property
    def student_id(self):
        return self._student_id  # read-only: no setter on purpose

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def programme(self):
        return self._programme

    @programme.setter
    def programme(self, new_programme):
        if not new_programme.strip():
            raise ValueError("Programme cannot be empty.")
        self._programme = new_programme.strip().upper()

    @property
    def marks(self):
        return dict(self._marks)  # return a COPY so outside code can't alter it

    def set_mark(self, subject, value):
        """Update one subject mark after validating it."""
        if subject not in self.SUBJECTS:
            raise KeyError(f"Unknown subject '{subject}'.")
        self._validate_mark(value)
        self._marks[subject] = value

    def set_marks(self, marks):
        """Set all marks from a dict like {'Math': 75, ...}."""
        for subject in self.SUBJECTS:
            self.set_mark(subject, marks[subject])

    # ---- Validation + TASK 6: flexible interface ----
    @staticmethod
    def _validate_mark(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Mark must be a number, got {value!r}.")
        if not 0 <= value <= 100:
            raise ValueError(f"Mark must be between 0 and 100, got {value}.")

    @staticmethod
    def average_of(*marks):
        """Average of ANY number of marks (variable-length arguments)."""
        if len(marks) == 0:
            raise ValueError("At least one mark is required.")
        for mark in marks:
            Student._validate_mark(mark)
        return sum(marks) / len(marks)

    def calculate_average(self, *marks):
        """
        Flexible interface (Python's answer to overloading):
          - calculate_average()            -> average of the stored marks
          - calculate_average(70, 80, 90)  -> average of the marks supplied
          - calculate_average(60, 70)      -> any number of marks works
        """
        if marks:
            return self.average_of(*marks)
        return self.average_of(*self._marks.values())

    def get_grade(self):
        average = self.calculate_average()
        if average >= 80:
            return "A"
        if average >= 70:
            return "B"
        if average >= 60:
            return "C"
        if average >= 50:
            return "D"
        return "F"

    # ---- Abstract method: subclasses MUST implement ----
    @abstractmethod
    def get_status(self):
        """Describe the student's standing. Each student type decides how."""

    def eligibility_label(self):
        """Default: scholarship eligibility is not applicable."""
        return "N/A"

    def __str__(self):
        return f"{self._student_id} - {self.full_name} ({self._programme})"


# ---------------------------------------------------------------------------
# TASK 2: Concrete subclass
# ---------------------------------------------------------------------------
class AIUStudent(Student):
    """A regular AIU student. Implements the abstract method."""

    def get_status(self):
        return "Regular AIU student (no scholarship)"


# ---------------------------------------------------------------------------
# TASK 4: Inheritance + method overriding
# ---------------------------------------------------------------------------
class ScholarshipStudent(AIUStudent):
    """An AIU student who holds, or is being considered for, a scholarship."""

    def __init__(self, student_id, first_name, last_name, programme, marks,
                 scholarship_amount=0):
        # super() reuses the parent's constructor instead of repeating it
        super().__init__(student_id, first_name, last_name, programme, marks)
        self._scholarship_amount = 0
        self.scholarship_amount = scholarship_amount  # validated setter

    @property
    def scholarship_amount(self):
        return self._scholarship_amount

    @scholarship_amount.setter
    def scholarship_amount(self, amount):
        if amount < 0:
            raise ValueError("Scholarship amount cannot be negative.")
        self._scholarship_amount = amount

    def is_eligible(self):
        return self.calculate_average() >= SCHOLARSHIP_THRESHOLD

    # Overridden methods (same name as parent, different behaviour)
    def get_status(self):
        if self.is_eligible():
            return f"Scholarship holder (KES {self._scholarship_amount:,.0f})"
        return "Scholarship student: average below 85, under review"

    def eligibility_label(self):
        return "Eligible" if self.is_eligible() else "Not eligible"


# ---------------------------------------------------------------------------
# TASK 3: Composition
# ---------------------------------------------------------------------------
class PerformanceAnalyzer:
    """Works WITH student objects (has-a relationship); copies no data."""

    def __init__(self, students):
        if not students:
            raise ValueError("Analyzer needs at least one student.")
        self._students = students  # references to the same objects

    def highest_average(self):
        return max(self._students, key=lambda s: s.calculate_average())

    def lowest_average(self):
        return min(self._students, key=lambda s: s.calculate_average())

    def class_average(self):
        total = sum(s.calculate_average() for s in self._students)
        return total / len(self._students)

    # ---- TASK 7: report ----
    def generate_report(self):
        line = "=" * 92
        header = (f"{'ID':<8}{'Name':<18}{'Prog':<6}{'Math':>5}{'Eng':>5}"
                  f"{'Sci':>5}{'Avg':>8}{'Grade':>7}  {'Scholarship':<12}")
        rows = []
        for s in self._students:
            m = s.marks
            rows.append(
                f"{s.student_id:<8}{s.full_name:<18}{s.programme:<6}"
                f"{m['Math']:>5}{m['English']:>5}{m['Science']:>5}"
                f"{s.calculate_average():>8.2f}{s.get_grade():>7}  "
                f"{s.eligibility_label():<12}"
            )
        best, worst = self.highest_average(), self.lowest_average()
        summary = [
            "CLASS PERFORMANCE SUMMARY",
            f"Highest average : {best.full_name} ({best.calculate_average():.2f})",
            f"Lowest average  : {worst.full_name} ({worst.calculate_average():.2f})",
            f"Class average   : {self.class_average():.2f}",
        ]
        return "\n".join([line, "STUDENT PERFORMANCE REPORT", line, header,
                          "-" * 92, *rows, line, *summary, line])


# ---------------------------------------------------------------------------
# CSV loading (factory: picks the right class for each record)
# ---------------------------------------------------------------------------
def load_students(csv_path):
    students = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as file:
            for row_number, row in enumerate(csv.DictReader(file), start=2):
                try:
                    marks = {subject: float(row[subject])
                             for subject in Student.SUBJECTS}
                    args = (row["StudentID"], row["FName"], row["LName"],
                            row["Programme"], marks)
                    average = Student.average_of(*marks.values())
                    if average >= SCHOLARSHIP_THRESHOLD:
                        amount = 100000 if average >= 90 else 50000  # KES
                        students.append(ScholarshipStudent(*args, amount))
                    else:
                        students.append(AIUStudent(*args))
                except (KeyError, ValueError, TypeError) as error:
                    print(f"Skipping row {row_number}: {error}")
    except FileNotFoundError:
        print(f"Error: '{csv_path}' not found.")
    return students


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------
def main():
    students = load_students("students.csv")
    if not students:
        return

    # TASK 5: polymorphism, one list, mixed types, one method name
    print("POLYMORPHISM DEMO: get_status()")
    for student in students:
        print(f"  [{type(student).__name__:<18}] {student.full_name:<16}"
              f"-> {student.get_status()}")

    # TASK 6: flexible interface
    print("\nFLEXIBLE INTERFACE DEMO: calculate_average()")
    sample = students[0]
    print(f"  Stored marks        : {sample.calculate_average():.2f}")
    print(f"  Three marks         : {sample.calculate_average(70, 80, 90):.2f}")
    print(f"  Five marks          : {sample.calculate_average(60, 70, 80, 90, 100):.2f}")
    for bad_input in [(), (50, 150), (50, "abc")]:
        try:
            sample.average_of(*bad_input)
        except (ValueError, TypeError) as error:
            print(f"  Rejected {bad_input}: {error}")

    # Encapsulation demo: validated update
    print("\nENCAPSULATION DEMO")
    try:
        sample.set_mark("Math", 120)
    except ValueError as error:
        print(f"  Invalid update blocked: {error}")

    # Abstraction demo
    try:
        Student("00/000", "A", "B", "X", {})
    except TypeError as error:
        print(f"  Abstract class cannot be instantiated: {error}")

    # TASK 7: report
    print()
    print(PerformanceAnalyzer(students).generate_report())
if __name__ == "__main__":
    main()