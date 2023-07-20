import io
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import LoginForm, UpdatePasswordForm, RegisterForm, ForgotPasswordForm, CourseForm
from .functions import get_number_of_course_attendance_percentage, get_number_of_course_attendance_present, \
    get_number_of_course_attendance_absent
from .models import Staff, Course, CourseAttendance, Student, Person, RegisteredCourses, Department, Programme, \
    RegisteredStudent, StudentAttendance

session = '2022/2023'


# Create a login view
class LoginView(View):
    # Add template name
    template_name = 'Scanner/login.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Redirect back to dashboard if true
            return HttpResponseRedirect(reverse('Scanner:dashboard'))
        # Otherwise
        else:
            #  Get login form
            form = LoginForm()
            # load the page with the form
            return render(request, self.template_name, {'form': form})

    # Create post function to process te form on submission
    def post(self, request):
        # Get the submitted form
        form = LoginForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            # Process the input
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            # Authenticate the user login details
            user = authenticate(request, username=username, password=password)
            # Check if user exists
            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect to dashboard page
                return HttpResponseRedirect(reverse('Scanner:dashboard'))
            # If user does not exist
            else:
                # Create an error message
                messages.error(request, "Invalid login details")
                # Redirect back to the login page
                return HttpResponseRedirect(reverse('Scanner:login'))


# Create a forgot password view
class ForgotPasswordView(View):
    # Add template name
    template_name = 'Scanner/forgot_password.html'

    # Create get function
    def get(self, request):
        form = ForgotPasswordForm()
        # load the page with the form
        return render(request, self.template_name, {'form': form})

    # Create post function to process the form on submission
    def post(self, request):
        # Get the submitted form
        form = ForgotPasswordForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            user_id = form.cleaned_data['user_id'].strip()
            email = form.cleaned_data['email'].strip()

            try:
                user = User.objects.get(username=user_id)
            except Exception:
                messages.error(request, "User does not exist")
                return HttpResponseRedirect(reverse('Scanner:forgot_password'))

            try:
                person = Person.objects.get(email=email)
            except Exception:
                messages.error(request, "Email does not exist")
                return HttpResponseRedirect(reverse('Scanner:forgot_password'))

            if user.username == user_id and person.email == email:
                messages.success(request, "Recovery password has been successfully sent")

                # Redirect back to dashboard if true
                return HttpResponseRedirect(reverse('Scanner:password_retrieval', args=(user.id,)))

            else:
                messages.success(request, "Password does not match")

                # Redirect back to page
                return HttpResponseRedirect(reverse('Scanner:forgot_password'))


# Create an update password view
class UpdatePasswordView(View):
    template_name = 'Scanner/update_password.html'

    def get(self, request, user_id):
        form = UpdatePasswordForm()
        user = get_object_or_404(User, id=user_id)
        context = {'user': user, 'user_id': user_id, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        if request.method == 'POST':
            form = UpdatePasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password'].strip()
                password2 = form.cleaned_data['confirm_password'].strip()

                if password1 == "password":
                    messages.error(request, "Password cannot be 'password'")
                    return HttpResponseRedirect(reverse('Scanner:update_password', args=(user_id,)))

                else:
                    if password1 == password2:
                        user = User.objects.get(id=user_id)
                        user.set_password(password1)
                        user.save()

                        messages.success(request, 'Password successfully changed')
                        return HttpResponseRedirect(reverse('Scanner:login'))
                    else:
                        messages.error(request, "Password does not match")
                        return HttpResponseRedirect(reverse('Scanner:update_password', args=(user_id,)))


# Create a register view
class RegisterView(View):
    # Add template name
    template_name = 'Scanner/register.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Redirect back to dashboard if true
            return HttpResponseRedirect(reverse('Scanner:dashboard'))
        # Otherwise
        else:
            #  Get login form
            form = RegisterForm()
            # load the page with the form
            return render(request, self.template_name, {'form': form})

    # Create post function to process the form on submission
    def post(self, request):
        # Get the submitted form
        form = RegisterForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            # Process the input
            full_name = form.cleaned_data['full_name'].strip().upper()
            email = form.cleaned_data['email'].strip()
            user_id = form.cleaned_data['user_id'].strip().upper()
            level = request.POST.get('level').strip()
            prog = request.POST.get('programme').strip()
            dep = request.POST.get('department').strip()
            password = request.POST.get('password').strip()
            confirm_password = request.POST.get('confirm_password').strip()
            is_student = request.POST.get("user_type")

            if password == confirm_password:
                try:
                    user = User.objects.create_user(username=user_id, password=password)
                    user.save()

                    if is_student == "on":
                        programme = get_object_or_404(Programme, programme_name=prog)
                        person = Person.objects.create(user=user, full_name=full_name, email=email, is_staff=False)
                        student = Student.objects.create(person=person, matric_no=user_id, level=level, programme=programme)

                        # Create the qr code
                        qrcode_img = qrcode.make(f"{user_id}")
                        canvas = Image.new("RGB", (300, 300), "white")
                        ImageDraw.Draw(canvas)
                        canvas.paste(qrcode_img)
                        buffer = io.BytesIO()
                        canvas.save(buffer, "PNG")

                        student.qr_image.save(f"{user_id}", File(buffer), save=False)
                        canvas.close()

                        student.save()

                        messages.success(request, "Student successfully registered")
                    else:
                        department = get_object_or_404(Department, department_name=dep)
                        person = Person.objects.create(user=user, full_name=full_name, email=email, is_staff=True)
                        Staff.objects.create(person=person, staff_id=user_id, department=department)

                        messages.success(request, "Staff successfully registered")

                    # Redirect back to dashboard if true
                    return HttpResponseRedirect(reverse('Scanner:login'))
                except Exception:
                    messages.success(request, "User already exists")
                    # Redirect back to dashboard if true
                    return HttpResponseRedirect(reverse('Scanner:register'))

            else:
                messages.success(request, "Password does not match")

                # Redirect back to dashboard if true
                return HttpResponseRedirect(reverse('Scanner:register'))


# Create a dashboard view
class DashboardView(View):
    # Add template name
    template_name = 'Scanner/dashboard.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Check if user is a staff
        if person.is_staff:
            # Get the current logged in staff
            staff = get_object_or_404(Staff, person=person)
            # Create a dictionary of data to be accessed on the page
            context = {
                'user': staff,
                'person': person,
            }
        # Otherwise
        else:
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)

            # Create a dictionary of data to be accessed on the page
            context = {
                'user': student,
                'person': person,
            }
        # Load te page with the data
        return render(request, self.template_name, context)


# Create a register courses view
class CreateCourseView(View):
    # Add template name
    template_name = 'Scanner/add_course.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        #  Get login form
        form = CourseForm()
        # Create a dictionary of data to be accessed on the page
        context = {
            'form': form,
            'person': person,
        }
        # load the page with the form
        return render(request, self.template_name, context)

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create post function
    def post(self, request):
        # Get the submitted form
        form = CourseForm(request.POST)
        #  Check if the form is valid
        if form.is_valid():
            # Get the current person logged in
            person = get_object_or_404(Person, user=request.user)
            # Get the current logged in student
            staff = get_object_or_404(Staff, person=person)

            # Process the input
            course_title = form.cleaned_data['course_title'].strip().upper()
            course_code = form.cleaned_data['course_code'].strip().upper()
            course_unit = form.cleaned_data['course_unit']
            semester = form.cleaned_data['semester'].strip()
            department = form.cleaned_data['department'].strip()

            if Course.objects.filter(course_code=course_code).exists():
                messages.error(request, "Course already exists")
            else:
                department = get_object_or_404(Department, department_name=department)
                course = Course.objects.create(course_title=course_title, course_code=course_code, course_unit=course_unit,
                                      semester=semester, department=department, lecturer=staff)
                RegisteredStudent.objects.create(course=course)
                messages.success(request, "Course successfully created")

            return HttpResponseRedirect(reverse("Scanner:create_course"))


# Create a register courses view
class RegisterCoursesView(View):
    # Add template name
    template_name = 'Scanner/register_courses.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Create a dictionary of data to be accessed on the page
        context = {
            'person': person,
        }
        # Load te page with the data
        return render(request, self.template_name, context)

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create post function
    def post(self, request):
        # Check if request method is POST
        if request.method == "POST":
            # Get the user input
            semester = request.POST.get("semester")

            # Get the current person logged in
            person = get_object_or_404(Person, user=request.user)
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            # Get every courses in the students department
            courses = Course.objects.filter(semester=semester, department=student.programme.department)

            if RegisteredCourses.objects.filter(student=student).exists():
                # Get all the courses registered for by a student
                reg_courses = RegisteredCourses.objects.get(student=student)
            else:
                # Create object
                reg_courses = RegisteredCourses.objects.create(student=student)

            is_registered = []
            for course in courses:
                if course in reg_courses.courses.all():
                    is_registered.append(True)
                else:
                    is_registered.append(False)

            zipped = zip(courses, is_registered)

            # Create a dictionary of data to be returned to the page
            context = {
                'person': person,
                'student': student,
                'zipped': zipped,
            }

            # return data back to the page
            return render(request, self.template_name, context)


# Create function to add course to registered courses
def add_course(request):
    if request.method == "POST":
        course_code = request.POST.get("course_code")
        # Get the course
        course = get_object_or_404(Course, course_code=course_code)
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current logged in student
        student = get_object_or_404(Student, person=person)
        if RegisteredCourses.objects.filter(student=student).exists():
            reg_courses = get_object_or_404(RegisteredCourses, student=student)
        else:
            reg_courses = RegisteredCourses(student=student)

        # Get all the student registered for by a course
        reg_std = RegisteredStudent.objects.get(course=course)

        reg_courses.courses.add(course)
        reg_courses.save()

        reg_std.students.add(student)
        reg_std.save()

        # return data back to the page
        return JsonResponse({'course_code': course_code})


# Create function to remove course to registered courses
def remove_course(request):
    if request.method == "POST":
        course_code = request.POST.get("course_code")
        # Get the course
        course = get_object_or_404(Course, course_code=course_code)
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current logged in student
        student = get_object_or_404(Student, person=person)
        if RegisteredCourses.objects.filter(student=student).exists():
            reg_courses = get_object_or_404(RegisteredCourses, student=student)
        else:
            reg_courses = RegisteredCourses(student=student)

        if RegisteredStudent.objects.filter(course=course).exists():
            # Get all the courses registered for by a student
            reg_std = RegisteredStudent.objects.get(course=course)
        else:
            # Create object
            reg_std = RegisteredStudent.objects.create(course=course)

        reg_courses.courses.remove(course)
        reg_courses.save()

        reg_std.students.remove(student)
        reg_std.save()

        # return data back to the page
        return JsonResponse({'course_code': course_code})


# Create a registered courses view
class RegisteredCoursesView(View):
    # Add template name
    template_name = 'Scanner/registered_courses.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Create a dictionary of data to be accessed on the page
        context = {
            'person': person,
        }
        # Load te page with the data
        return render(request, self.template_name, context)

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create post function
    def post(self, request):
        # Check if request method is POST
        if request.method == "POST":
            # Get the user input
            semester = request.POST.get("semester")

            # Get the current person logged in
            person = get_object_or_404(Person, user=request.user)
            # Get the current logged in student
            student = get_object_or_404(Student, person=person)
            # Get every courses in the students department
            reg_courses = RegisteredCourses.objects.get(student=student)
            courses = reg_courses.courses.filter(semester=semester)

            # Create a dictionary of data to be returned to the page
            context = {
                'person': person,
                'student': student,
                'courses': courses,
            }

            # return data back to the page
            return render(request, self.template_name, context)


# Create a attendance register view
class AttendanceRegisterView(View):
    # Add template name
    template_name = 'Scanner/attendance_register.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current logged in staff
        current_staff = get_object_or_404(Staff, person=person)
        #  Filter all the courses taken by the staff
        courses = Course.objects.filter(lecturer=current_staff)
        # Create a dictionary of data to be accessed on the page
        context = {
            'person': person,
            'courses': courses,
        }
        return render(request, self.template_name, context)

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create post function
    def post(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current logged in staff
        current_staff = get_object_or_404(Staff, person=person)
        #  Filter all the courses taken by the staff
        courses = Course.objects.filter(lecturer=current_staff)
        # Check if request method is POST
        if request.method == "POST":
            # Get user input
            course_code = request.POST.get('course_code')
            date_input = request.POST.get('date')

            # Get the course using the course code
            course = get_object_or_404(Course, course_code=course_code)
            # split the date input and convert to datetime object
            user_date = date_input.split('-')
            user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

            # use a try block
            if CourseAttendance.objects.filter(**{'course':course, 'date':user_date}).exists():
                # Get the required course attendance using the course and converted date
                course_attendance = get_object_or_404(CourseAttendance, course=course, date=user_date)
                # Get a list of all the ids of students in the course attendance
                student_attendance = course_attendance.student_attendance.all().order_by('id')
                # Create a dictionary of data to be returned to the page
                context = {
                    'person': person,
                    'course_attendance': course_attendance,
                    'student_attendance': student_attendance,
                    'courses': courses,
                }
            # if course attendance does not exist
            else:
                # Create the required course attendance using the course and converted date
                course_attendance = CourseAttendance.objects.create(course=course, date=user_date)
                # Get all the student registered for by a course
                reg_std = RegisteredStudent.objects.get(course=course)
                for student in reg_std.students.all():
                    std_att = StudentAttendance.objects.create(student=student, date=user_date)
                    std_att.save()
                    course_attendance.student_attendance.add(std_att)
                    course_attendance.save()
                # Get a list of all the ids of students in the course attendance
                student_attendance = course_attendance.student_attendance.all().order_by('id')
                # Create a dictionary of data to be returned to the page
                context = {
                    'person': person,
                    'course_attendance': course_attendance,
                    'student_attendance': student_attendance,
                    'courses': courses,
                }
            # return data back to the page
            return render(request, self.template_name, context)


# Create function to mark attendance
def take_attendance(request):
    if request.method == "POST":
        course_att = request.POST.get("course_att")
        matric_no = request.POST.get("matric_no")

        # Get student attendance
        course_attendance = get_object_or_404(CourseAttendance, id=course_att)
        # Get student
        student = get_object_or_404(Student, matric_no=matric_no)
        std_att = course_attendance.student_attendance.filter(student=student)
        # Cancel attendance
        std_att.is_present = True
        std_att.save()

        # return data back to the page
        return JsonResponse({'att_id': std_att.id, 'matric_no': matric_no})


# Create an attendance sheet view
class AttendanceSheetView(View):
    # Add template name
    template_name = 'Scanner/attendance_sheet.html'

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current logged in staff
        current_staff = get_object_or_404(Staff, person=person)
        #  Filter all the courses taken by the staff
        courses = Course.objects.filter(lecturer=current_staff)
        # Create a dictionary of data to be accessed on the page
        context = {
            'person': person,
            'courses': courses,
        }
        return render(request, self.template_name, context)

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create post function
    def post(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)
        # Get the current logged in staff
        current_staff = get_object_or_404(Staff, person=person)
        #  Filter all the courses taken by the staff
        courses = Course.objects.filter(lecturer=current_staff)
        # Check if request method is POST
        if request.method == "POST":
            # Get user input
            course_code = request.POST.get('course_code')
            date_input = request.POST.get('date')

            # Get the course using the course code
            course = get_object_or_404(Course, course_code=course_code)
            # split the date input and convert to datetime object
            user_date = date_input.split('-')
            user_date = datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2]))

            # use a try block
            try:
                # Get the required course attendance using the course and converted date
                course_attendance = get_object_or_404(CourseAttendance, course=course, date=user_date)
                # Get a list of all the ids of students in the course attendance
                student_attendance = course_attendance.student_attendance.all().order_by('id')
                # Create a dictionary of data to be returned to the page
                context = {
                    'person': person,
                    'student_attendance': student_attendance,
                    'courses': courses,
                }
            # if course attendance does not exist
            except Exception:
                context = {
                    'person': person,
                    'courses': courses,
                }
            # return data back to the page
            return render(request, self.template_name, context)


class StatisticsView(View):
    # Add template name
    template_name = 'Scanner/statistics.html'

    # Create get function
    def get(self, request):
        # Get the current person logged in
        person = get_object_or_404(Person, user=request.user)

        # Get the current logged in student
        student = get_object_or_404(Student, person=person)

        if RegisteredStudent.objects.filter(session=session).exists():
            # Get all the registered courses by the student
            reg_students = RegisteredStudent.objects.filter(session=session)

            courses = [
                reg_std.course for reg_std in reg_students if student in reg_std.students.all()
            ]
            course_codes = [
                reg_std.course.course_code for reg_std in reg_students if student in reg_std.students.all()
            ]
            course_attendance_present = [
                get_number_of_course_attendance_present(reg_std.course, student) for reg_std in reg_students if
                student in reg_std.students.all()
            ]
            course_attendance_absent = [
                get_number_of_course_attendance_absent(reg_std.course, student) for reg_std in reg_students if
                student in reg_std.students.all()
            ]
            course_attendance_percentage = [
                get_number_of_course_attendance_percentage(reg_std.course, student) for reg_std in reg_students if
                student in reg_std.students.all()
            ]
            no_of_eligible_courses = []
            no_of_ineligible_courses = []
            for percentage in course_attendance_percentage:
                if percentage >= 75:
                    no_of_eligible_courses.append(percentage)
                else:
                    no_of_ineligible_courses.append(percentage)

            zipped = zip(course_codes, course_attendance_present, course_attendance_absent,
                         course_attendance_percentage)
        else:
            courses = {}
            zipped = []

        # Create a dictionary of data to be accessed on the page
        context = {
            'user': student,
            'zipped': zipped,
            'courses': courses,
        }
        # Load te page with the data
        return render(request, self.template_name, context)


# Create a logout view
class LogoutView(View):

    # Add a method decorator to make sure user is logged in
    @method_decorator(login_required())
    # Create get function
    def get(self, request):
        # logout user
        logout(request)
        # redirect to login page
        return HttpResponseRedirect(reverse('Scanner:login'))
