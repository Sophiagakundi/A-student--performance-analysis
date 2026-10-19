# Student Perfomance Analysis Sytem

A Python OOP program that loads student records from a CSV file, calculates
averages and grades, identifies scholarship-eligible students (average of 85
or more) and prints a performance report with a class summary.

## How to run
Keep student_performance.py and students.csv in the same folder, then run:

python student_performance.py

## OOP concepts used
- Encapsulation: protected attributes, properties and validated setters in Student
- Abstraction: Student is an abstract class with the abstract method get_status()
- Inheritance: AIUStudent inherits from Student; ScholarshipStudent inherits from AIUStudent using super()
- Method overriding and polymorphism: get_status() behaves differently for each student type
- Composition: PerformanceAnalyzer works with the student objects directly
- Flexible interface: calculate_average(*marks) accepts any number of marks

## Reflection
The part I found the hardest was understanding the difference between abstraction and 
inheritance. Python also has no true method overloading, so I used the `*marks`
to let one method accept any number of values. I also had to fix file name
mismatches, learn to run Python from the VS Code terminal and push the
project to GitHub.

## AI Use Declaration
I used Claude to generate the initial code and dataset and to
explain the concepts and help fix errors. I ran and tested the program,
and I reworded some of the comments in my own words.