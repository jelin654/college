
from django.urls import path,include
from . import views

urlpatterns = [
   path('', views.landingpage, name='landingpage'),
    path('signup/', views.signup, name='signup'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('loginfun/', views.loginfun, name='loginfun'),
    path('usercreate/', views.usercreate, name='usercreate'),
    path('logoutfun',views.logoutfun,name='logoutfun'),

    path('home',views.home,name='home'),

    path('adminhome',views.adminhome,name='adminhome'),

    path('addcourse',views.addcourse,name='addcourse'),
    path('addcoursedetails',views.addcoursedetails,name='addcoursedetails'),
    path('ad_showcourse',views.ad_showcourse,name='ad_showcourse'),

    path('addstudent',views.addstudent,name='addstudent'),
    path('addstudentdetails',views.addstudentdetails,name='addstudentdetails'),
    path('ad_showstudent',views.ad_showstudent,name='ad_showstudent'),
    path('ad_showteacher',views.ad_showteacher,name='ad_showteacher'),

    path('userhome',views.userhome,name='userhome'),
    path('userstudent',views.userstudent,name='userstudent'),
    path('usercourse',views.usercourse,name='usercourse'),
    path('teacherprofile',views.teacherprofile,name='teacherprofile'),
    path('editprofile',views.editprofile,name='editprofile'),



    path('showcourse', views.showcourse, name='showcourse'),
    path('editcourse/<int:s>',views.editcourse,name='editcourse'),
    path('editcoursedet/<int:s>',views.editcoursedet,name='editcoursedet'),
    path('deletecourse/<int:s>',views.deletecourse,name='deletecourse'),

   
    path('showstudent', views.showstudent, name='showstudent'),
    path('editstudent/<int:s>',views.editstudent,name='editstudent'),
    path('editstudentdet/<int:s>',views.editstudentdet,name='editstudentdet'),
    path('deletestudent/<int:s>',views.deletestudent,name='deletestudent'),

    path('addteacher',views.addteacher,name='addteacher'),
    path('addteacherdetails',views.addteacherdetails,name='addteacherdetails'),
    path('showteacher', views.showteacher, name='showteacher'),
    path('editteacher/<int:s>',views.editteacher,name='editteacher'),
    path('editteacherdet/<int:s>',views.editteacherdet,name='editteacherdet'),
    path('deleteteacher/<int:s>/', views.deleteteacher, name='deleteteacher'),

path('teacher/delete/', views.delete_profile, name='deleteprofile'),



    
]
