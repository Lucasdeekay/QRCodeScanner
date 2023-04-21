from django.contrib import admin
from .models import Staff, Student, Faculty, Programme, Department, StudentAttendance, Course, CourseAttendance, \
    RegisteredStudent, Person, RegisteredCourses


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'is_staff')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_name',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'department_name')


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('department', 'programme_name')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('person', 'staff_id', 'department')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('person', 'matric_no', 'level', 'programme')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_code', 'course_unit', 'semester', 'department', 'lecturer')


class RegisteredCoursesAdmin(admin.ModelAdmin):
    list_display = ('student', 'session')


class RegisteredStudentsAdmin(admin.ModelAdmin):
    list_display = ('course', 'session')


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'is_present', 'date')


class CourseAttendanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date')


admin.site.register(Person, PersonAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(RegisteredCourses, RegisteredCoursesAdmin)
admin.site.register(RegisteredStudent, RegisteredStudentsAdmin)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(CourseAttendance, CourseAttendanceAdmin)