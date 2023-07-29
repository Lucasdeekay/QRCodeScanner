# function returns the total amount of times a student is present for a course
from Scanner.models import CourseAttendance, RegisteredStudent


session = '2022/2023'


def get_total_number_of_students(course):
    if RegisteredStudent.objects.filter(course=course, session=session).exists():
        all_students = RegisteredStudent.objects.get(course=course, session=session).students.all()
        return len(all_students)
    else:
        return 0


def get_number_of_course_attendance_present(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course)
    present = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if student_att.is_present:
                present += 1
        except Exception:
            pass
    return present


# function returns the total amount of times a student is absent for a course
def get_number_of_course_attendance_absent(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course)
    absent = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if not student_att.is_present:
                absent += 1
        except Exception:
            pass
    return absent


# function returns the percentage a student is present for a course
def get_number_of_course_attendance_percentage(course, student):
    all_attendance = CourseAttendance.objects.filter(course=course)
    present = 0
    absent = 0
    for att in all_attendance:
        try:
            student_att = att.student_attendance.get(student=student)
            if student_att.is_present:
                present += 1
            else:
                absent += 1
        except Exception:
            pass
    if (present + absent) == 0:
        return 0
    else:
        return round((present / (present + absent)) * 100, 2)

