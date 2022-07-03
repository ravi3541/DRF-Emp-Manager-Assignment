from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import TokenRefreshView

from emp_man_api.views import (
   
    ChangePassword,
    DeleteEmployee,
    EmployeeList,
    EmployeeRegistration,
    ResetPassword,
    SendResetPasswordMail, 
    SuperManagerRegistration, 
    UserLogin,
    EmployeeProfile,
    UpdateEmployee,
    UserLogout,
    UsersList
    )


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/',SuperManagerRegistration.as_view(), name="register_super_manager"),
    path('employee/register/',EmployeeRegistration.as_view(), name="register_employee"),

    path('login/',UserLogin.as_view(), name="login"),
    path('employee/profile/',EmployeeProfile.as_view(), name="employee_profile"),

    path('employee/update/<pk>/',UpdateEmployee.as_view(), name="update_employee"),
    path('employee/delete/<pk>/',DeleteEmployee.as_view(), name="delete_employee"),
    path('employee/empList/',EmployeeList.as_view(), name="employee_List"),

    path('employee/usersList/',UsersList.as_view(), name="Users_List"),
    path('employee/logout/',UserLogout.as_view(), name="logout"),

    path('accounts/changepassword/',ChangePassword.as_view(),name="Change Password"),

    path('accounts/send-reset-mail/',SendResetPasswordMail.as_view(), name='send-password-reset-mail'),
    path('accounts/reset-password/<uid>/<token>',ResetPassword.as_view(), name='reset_password'),
    






]
