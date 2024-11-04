class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def is_passed(self):
        average = sum(self.marks) / len(self.marks)
        return average > 50


student1 = Student("Patryk", [60, 70, 80])
student2 = Student("Ania", [40, 45, 50])

print(f"Czy {student1.name} zdał? {student1.is_passed()}")
print(f"Czy {student2.name} zdała? {student2.is_passed()}")