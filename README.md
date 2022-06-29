Create a Custom user model with 3 roles (superuser, manager,employee)
● Email and mobile no. fields should be unique.
● Superuser should be created only through API.
● Manager can register himself through signup API.
● Manager should create the employee, and upon successful registration, employee should get system generated welcome mail with his credentials(email & randomly generated password).
● Manager can perform crud operations for employee.
● Employee cannot register himself.
● Employee can use his credentials to login and get his profile details only, i.e. employee should not be allowed to access any other part of API.
● Functionality for forgot password, login
● Jwt authentication, employee and manager custom permissions
● Create a logout API to blacklist user.
● Use class based views and Generic Views only
