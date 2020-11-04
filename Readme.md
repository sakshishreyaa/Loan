Authentication is based on email instead of username using JWT authentication system.
The roles are saved in the users table in database referenced by integers ;that is - 1 for `admin` ,2 for `agent` and 3 for `customers`. the is_staff and is_superuser is set to true for admin to create superuser instance through django.
The admin user can change any user details including roles .Since,the default role is customer after user registration admin can change that role to agent .
T0 build the image  run `docker-compose build` then to execute the image run `docker-compose up`.
To create a super user run *`docker-compose exec web python manage.py createsuperuser`*  in another terminal
as server is running in previous terminal.
To run the test cases user run *`docker-compose exec web python manage.py test`*  
