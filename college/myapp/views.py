from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from . models import Course,Student,Teacher
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django . contrib . auth import login,authenticate
from django.contrib.auth.decorators import login_required
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.

# landing page
def landingpage(request):
    return render(request,'landingpage.html')

# signup
def signup(request):
    return render(request,'signup.html')

# create user
def usercreate(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_name = request.POST['uname']
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        email = request.POST['mail']
        age = request.POST['age']
        phone = request.POST['phone']
        address=request.POST['address']
        image=request.FILES.get('image') 
        if password == cpassword:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'This username already exists')
                return redirect('signup')
            if not re.fullmatch(r'\d{10}', phone):
                messages.error(request, "Phone number must be 10 digits!")
                return render(request, 'signup.html')
            if len(password) < 6:
                messages.error(request, "Password must be at least 6 characters long!")
                return render(request, 'signup.html')
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('signup')
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messages.error(request, 'Invalid email format')
                return redirect('signup')
 
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=user_name,
                    password=password,
                    email=email
                )
                user.save()

                # Assign default course (first one)
                course = Course.objects.first()  # optional, or use specific logic

                # Create associated Teacher profile
                teacher = Teacher(
                    age=age, 
                    phone=phone,
                    user=user,
                    course=course,
                    address=address,  
                    image=image  
                )
                teacher.save()

                messages.success(request, 'User account and teacher profile created successfully!')
                return redirect('loginpage')
        else:
            messages.info(request, 'Password does not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

# login page
def loginpage(request):
    return render(request, 'loginpage.html')

# for log in given mam

# def loginfun(request):
#     if request.method == 'POST':
#         username = request.POST['usname']
#         password = request.POST['passd']
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_authenticated:  # Check if the user is authenticated
#                 if user.is_staff:
#                     login(request, user)
#                     request.session['user'] = user.username  # Set user session variable
#                     messages.success(request, "Login successfully!")
#                     return redirect('adminhome')
#                 else:
#                     login(request, user)
#                     request.session['user'] = user.username  # Set user session variable
#                     messages.info(request, f'Welcome {user}')
#                     return redirect('userhome')  # Redirect to techhome after login
            
#         else:
#             messages.info(request, 'Invalid Username or Password')
#             return redirect('loginpage')
#     return render(request, 'loginpage.html')

def loginfun(request):
    if request.method == 'POST':
        username = request.POST['usname']
        password = request.POST['passd']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user'] = user.username
            messages.success(request, "Login successfully!")

            # Wait on login page briefly, then redirect using JS
            if user.is_staff:
                return render(request, 'loginpage.html', {'redirect': 'adminhome'})
            else:
                return render(request, 'loginpage.html', {'redirect': 'userhome'})
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('loginpage')

    return render(request, 'loginpage.html')



 # log out
def logoutfun(request):
    auth.logout(request)
    return redirect('loginpage')


def home(request):
    return render(request,'home.html')

# admin homepage
@login_required(login_url='loginpage')
def adminhome(request):
    return render(request,'adminhome.html')

# user home page
@login_required(login_url='loginpage')
def userhome(request):
    return render(request,'userhome.html')

# user-show student table
def userstudent(request):
    st = Student.objects.all()
    return render(request, 'userstudent.html', {'stud': st}) 

# user-show course table
def usercourse(request):
     cour = Course.objects.all()
     return render(request,'usercourse.html', {'courses': cour}) 
 
def teacherprofile(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'teacherprofile.html', {'teacher': teacher})
 
@login_required
# def editprofile(request):
#     teacher = Teacher.objects.get(user=request.user)
#     user=request.user
#     if request.method == 'POST':
#         teacher.phone = request.POST.get('phone')
#         teacher.age = request.POST.get('age')
#         teacher.address = request.POST.get('address')
#         teacher.course_id = request.POST.get('course')  # assuming course is a FK
#         if request.FILES.get('image'):
#             teacher.image = request.FILES['image']
        
#         teacher.save()
#         new_username = request.POST.get('username')
#         new_email = request.POST.get('email')
#         if new_username and new_username != user.username:
#             user.username = new_username
#         if new_email and new_email != user.email:
#             user.email = new_email
#         user.save()
#         return redirect('teacherprofile')

#     courses = Course.objects.all()  # assuming Course model exists
#     return render(request, 'editprofile.html', {'teacher': teacher, 'courses': courses})


# update teacher

def editprofile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    user = request.user

    if request.method == 'POST':
        # Get values from POST
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')
        course_id = request.POST.get('course')
        image = request.FILES.get('image')
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Validation flags
        errors = []

        # Phone validation: must be 10 digits
        if not phone or not phone.isdigit() or len(phone) != 10:
            errors.append("Phone number must be 10 digits.")

       
        # Email validation
        if new_email and new_email != user.email:
            try:
                validate_email(new_email)
                if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                    errors.append("This email is already in use.")
            except ValidationError:
                errors.append("Enter a valid email address.")

        # Username validation
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                errors.append("This username is already taken.")

        # If any errors, re-render the form with messages
        if errors:
            for error in errors:
                messages.error(request, error)
            courses = Course.objects.all()
            return render(request, 'editprofile.html', {
                'teacher': teacher,
                'courses': courses
            })

        # No validation errors, so update and save
        teacher.phone = phone
        teacher.age = age
        teacher.address = address
        teacher.course_id = course_id if course_id else None
        if image:
            teacher.image = image
        teacher.save()

        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        user.save()

        # messages.success(request, "Profile updated successfully.")
        return redirect('teacherprofile')

    # For GET request
    courses = Course.objects.all()
    return render(request, 'editprofile.html', {
        'teacher': teacher,
        'courses': courses
    })


  
# admin-course model
# admin-add course
def addcourse(request):
    return render(request,'addcourse.html')

# admin-adding course details
def addcoursedetails(request):
    if request.method=='POST':
        c1=request.POST['coursename']
        c2=request.POST['fees']
        cou=Course(coursename=c1,fees=c2)
        cou.save()
        messages.success(request, "Course added successfully!")
        return redirect('addcourse')
    return redirect('addcourse')

# admin-show course
def ad_showcourse(request):
    cour = Course.objects.all()
    return render(request, 'ad_showcourse.html', {'courses': cour})

# admin-edit course
def editcourse(request,s):
    a=Course.objects.get(id=s)
    return render(request,'editcourse.html',{'co':a})

# admin-updating course
def editcoursedet(request,s):
    a=Course.objects.get(id=s)
    if request.method=='POST':
        # a=Course.objects.get(id=s)
        a.coursename=request.POST['coursename']
        a.fees=request.POST['fees']
        a.save()
        messages.success(request, "Course updated successfully!")
        return render(request, 'editcourse.html', {'co': a, 'redirect': True})
        # return redirect('showcourse')
    else:
        return redirect('editcourse')
    
# admin-delete course
def deletecourse(request,s):
    co=Course.objects.get(id=s)
    co.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('ad_showcourse')

# admin-student model

# admin-add student
def addstudent(request):
    cou=Course.objects.all()
    return render(request,'addstudent.html',{'cour':cou})

# admin-adding student details
def addstudentdetails(request):
    if request.method=='POST':
        s1=request.POST['coursename']
        s2=request.POST['studentname']
        s3=request.POST['address']
        s4=request.POST['age']
        s5=request.POST['joiningdate']
        cs=Course.objects.get(id=s1)
        stud=Student(studentname=s2,address=s3,age=s4,joiningdate=s5,course=cs)
        stud.save()
        messages.success(request, "Stdent details added successfully!")
        return redirect('addstudent')
    return redirect('addstudent')

# admin-show student
def ad_showstudent(request):
    st = Student.objects.all()
    return render(request, 'ad_showstudent.html', {'stud': st})

# admin- edit student
def editstudent(request,s):
    a=Student.objects.get(id=s)
    c=Course.objects.all()
    return render(request,'editstudent.html',{'st':a,'cou':c})

# admin-updating student
def editstudentdet(request,s):
    if request.method=='POST':
        b=Student.objects.get(id=s)
        b.studentname=request.POST['studentname']
        b.address=request.POST['address']
        b.age=request.POST['age']
        b.joiningdate=request.POST['joiningdate']
        c=request.POST['coursename']
        co=Course.objects.get(id=c)
        b.course=co
        b.save()
        messages.success(request, "Student details updated successfully!")
        return render(request, 'editstudent.html', {'st': b, 'redirect': True})
        return redirect('showstudent')
    else:
        return redirect('editstudent')

# admin-delete student    
def deletestudent(request,s):
    st=Student.objects.get(id=s)
    st.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('ad_showstudent') 

# admin-teacher model
# admin -show teacher
def ad_showteacher(request):
    st = Teacher.objects.all()
    return render(request, 'ad_showteacher.html', {'stud': st}) 

def showteacher(request):
    st = Teacher.objects.all()
    return render(request, 'showteacher.html', {'stud': st}) 






def showcourse(request):
    cour = Course.objects.all()
    return render(request, 'showcourse.html', {'courses': cour})

def showstudent(request):
    st = Student.objects.all()
    return render(request, 'showstudent.html', {'stud': st}) 
 

def addteacher(request):
    cou=Course.objects.all()
    # tea=Teacher.objects.all()
    u=User.objects.all()
    # return render(request,'addteacher.html',{'us':u,'cour':cou})
    return render(request, 'addteacher.html', {'users': u, 'cour': cou})

def addteacherdetails(request):
    if request.method=='POST':
        s1=request.POST['age']
        s2=request.POST['address']
        s3=request.POST['phone']
        s4=request.FILES.get('image')
        s5=request.POST['coursename']
        s6=request.POST['user']
        cs=Course.objects.get(id=s5)
        us=User.objects.get(id=s6)
        teach=Teacher(age=s1,address=s2,phone=s3,image=s4,course=cs,user=us)
        teach.save()
        messages.success(request, "Teacher details added successfully!")
        return redirect('addteacher')
    return redirect('addteacher')





def editteacher(request, s):
    te = Teacher.objects.get(id=s)
    courses = Course.objects.all()
    users = User.objects.all()
    return render(request, 'editteacher.html', {'te': te, 'courses': courses, 'users': users})

def editteacherdet(request,s):
    if request.method=='POST':
        b=Teacher.objects.get(id=s)
        b.age=request.POST['age']
        b.address=request.POST['address']
        b.phone=request.POST['phone']
        if 'image' in request.FILES:
            b.image = request.FILES['image']
        # b.image=request.POST['image']
        c=request.POST['coursename']
        co=Course.objects.get(id=c)
        b.course=co
        u=request.POST['user']
        us=User.objects.get(id=u)
        b.user=us

        b.save()
        return redirect('showteacher')
    else:
        return redirect('editteacher')
    
# def deleteteacher(request, s):
#     teacher = Teacher.objects.get(id=s)
#     user=teacher.user    
#     teacher.delete()
#     user.delete()
#     return redirect('showteacher')
def deleteteacher(request, s):
    teacher = Teacher.objects.get(id=s)
    user_id = teacher.user.id  # store user ID before deleting teacher
    teacher.delete()
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "Teacher and user deleted successfully!")
    return redirect('showteacher')
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Teacher  # adjust path if needed
from django.contrib.auth.models import User

@login_required
def delete_profile(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        user = request.user
        teacher.delete()
        user.delete()  # also delete the user account
        return redirect('loginpage')  # or wherever you'd like
    except Teacher.DoesNotExist:
        return redirect('teacherprofile')  # or show an error





