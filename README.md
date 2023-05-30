# Django-Blog-Website
A Blog Application made in Django Framework

A simple blog application with login-logout authentication, profile user images, post create-update-delete functionalities, Pagination, password-reset using email, and data visualization using integrated numpy, pandas and matplotlib graphs/ ML models 

## Setup Instructions

1. Run the server
   ```sh
   python manage.py runserver
   ```
2. Make Migrations
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Create a super user to access the admin page
   ```shell
   python manage.py createsuperuser
   ```
4. Interact with PostgreSQL using shell
   ```sh
   python manage.py shell 
   ```
   Eg.
   ```sh
   >>> from blog.models import Post 
   ```
   ```sh
   >>> User.objects.all()
   ```
   <QuerySet [<User: tusharjain>, <User: testuser>]>
   ```sh
   >>> user = User.objects.filter(username="tusharjain").first()
    >>> user.id
   ```
   1
   ```sh
   >>> post_1 = Post(title='Blog 1', content = 'First Post Content', author = user ) 
   >>> post_1.save()
   ```