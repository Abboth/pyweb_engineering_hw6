import faker
from datetime import date, timedelta
from random import randint, choice


def generate_fake_data(count_students, count_teachers):
    students = []
    teachers = []
    fake = faker.Faker()

    for _ in range(count_students):
        students.append(fake.name())

    for _ in range(count_teachers):
        teachers.append(fake.name())

    return students, teachers


def prepared_data(students, teachers):
    students_list = [(student, randint(1, 4)) for student in students]
    teachers_list = [(teacher,) for teacher in teachers]
    subjects = [("Algebra",), ("Biology",), ("Drawing",), ("Chemistry",), ("Geography",), ("Geometry",),
                ("History",), ("Literature",), ("Mathematics",), ("Music",), ("Physical education",),
                ("Physics",), ("Technology",), ("Physical education",)]
    grades = [1, 2, 3, 4, 5]
    students_grades = []
    subjects_teachers = []
    groups = [(i,) for i in range(1, 5)]

    for _ in range(15):
        for i in range(1, randint(1, len(students))):
            random_date = date.today() - timedelta(days=randint(1, 365))
            students_grades.append((i, randint(1, len(subjects)),
                                    randint(1, len(teachers)), choice(grades),
                                    random_date.strftime("%Y-%m-%d")))

    for _ in subjects:
        subjects_teachers.append((randint(1, len(subjects)), randint(1, len(teachers)),))

    return students_grades, subjects_teachers, students_list, teachers_list, subjects, groups


def main():

    students_amount = randint(30, 50)
    teachers_amount = randint(5, 8)

    return prepared_data(*generate_fake_data(students_amount, teachers_amount))
