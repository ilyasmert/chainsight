# bash scripts to create Django backend

1.    
        pip install django psycopg2-binary
Successfully installed asgiref-3.8.1 django-5.1.7 sqlparse-0.5.3
________________________________________________________________________________

2. 
        django-admin startproject database_backend_integration

        cd database_backend_integration

        python manage.py startapp inventory

________________________________________________________________________________

3.      python manage.py migrate

   - Operations to perform: Apply all migrations: admin, auth, contenttypes, sessions
   - Running migrations:

         Applying contenttypes.0001_initial... OK
         Applying auth.0001_initial... OK
         Applying admin.0001_initial... OK
         Applying admin.0002_logentry_remove_auto_add... OK
         Applying admin.0003_logentry_add_action_flag_choices... OK
         Applying contenttypes.0002_remove_content_type_name... OK
         Applying auth.0002_alter_permission_name_max_length... OK
         Applying auth.0003_alter_user_email_max_length... OK
         Applying auth.0004_alter_user_username_opts... OK
         Applying auth.0005_alter_user_last_login_null... OK
         Applying auth.0006_require_contenttypes_0002... OK
         Applying auth.0007_alter_validators_add_error_messages... OK
         Applying auth.0008_alter_user_username_max_length... OK
         Applying auth.0009_alter_user_last_name_max_length... OK
         Applying auth.0010_alter_group_name_max_length... OK
         Applying auth.0011_update_proxy_permissions... OK
         Applying auth.0012_alter_user_first_name_max_length... OK
         Applying sessions.0001_initial... OK


________________________________________________________________________________

4.      python manage.py inspectdb > inventory/models.py

        python manage.py shell

        Python 3.12.0 (v3.12.0:0fb18b02c8, Oct  2 2023, 09:45:56) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
        Type "help", "copyright", "credits" or "license" for more information.
        (InteractiveConsole)
              >>> from django.db import connection
              >>> print(connection.settings_dict['ENGINE'])
        django.db.backends.postgresql

________________________________________________________________________________

5.      python manage.py shell

        Python 3.12.0 (v3.12.0:0fb18b02c8, Oct  2 2023, 09:45:56) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
        Type "help", "copyright", "credits" or "license" for more information.
        (InteractiveConsole)
        >>> from inventory.models import *
        >>> from django.apps import apps
        >>> print(apps.get_models())
        [<class 'django.contrib.admin.models.LogEntry'>, <class 'django.contrib.auth.models.Permission'>, <class 'django.contrib.auth.models.Group'>, <class 'django.contrib.auth.models.User'>, <class 'django.contrib.contenttypes.models.ContentType'>, <class 'django.contrib.sessions.models.Session'>, <class 'inventory.models.AtpStock'>, <class 'inventory.models.AtpStockArchive'>, <class 'inventory.models.Intransit'>, <class 'inventory.models.IntransitArchive'>, <class 'inventory.models.PalletInfo'>, <class 'inventory.models.Ready'>, <class 'inventory.models.ReadyArchive'>, <class 'inventory.models.ReadyArchiveTest'>, <class 'inventory.models.Sales'>, <class 'inventory.models.SalesArchive'>, <class 'inventory.models.TestTable'>, <class 'inventory.models.ToBeProduced'>, <class 'inventory.models.ToBeProducedArchive'>, <class 'inventory.models.TransportationInfo'>, <class 'inventory.models.TransportationInfoArchive'>, <class 'inventory.models.UserRoles'>, <class 'inventory.models.Users'>]
        
________________________________________________________________________________

6.      python manage.py runserver

        Watching for file changes with StatReloader
        Performing system checks...
        
        System check identified no issues (0 silenced).
        
        You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
        Run 'python manage.py migrate' to apply them.
        March 11, 2025 - 18:47:28
        Django version 5.1.7, using settings 'database_backend_integration.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.


________________________________________________________________________________

7.      python manage.py migrate

        Operations to perform:
          Apply all migrations: admin, auth, contenttypes, sessions
        Running migrations:
          Applying contenttypes.0001_initial... OK
          Applying auth.0001_initial... OK
          Applying admin.0001_initial... OK
          Applying admin.0002_logentry_remove_auto_add... OK
          Applying admin.0003_logentry_add_action_flag_choices... OK
          Applying contenttypes.0002_remove_content_type_name... OK
          Applying auth.0002_alter_permission_name_max_length... OK
          Applying auth.0003_alter_user_email_max_length... OK
          Applying auth.0004_alter_user_username_opts... OK
          Applying auth.0005_alter_user_last_login_null... OK
          Applying auth.0006_require_contenttypes_0002... OK
          Applying auth.0007_alter_validators_add_error_messages... OK
          Applying auth.0008_alter_user_username_max_length... OK
          Applying auth.0009_alter_user_last_name_max_length... OK
          Applying auth.0010_alter_group_name_max_length... OK
          Applying auth.0011_update_proxy_permissions... OK
          Applying auth.0012_alter_user_first_name_max_length... OK
          Applying sessions.0001_initial... OK

________________________________________________________________________________

8.      python manage.py runserver

        Watching for file changes with StatReloader
        Performing system checks...
        
        System check identified no issues (0 silenced).
        March 11, 2025 - 18:49:48
        Django version 5.1.7, using settings 'database_backend_integration.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.

________________________________________________________________________________
9.  http://127.0.0.1:8000/api
10. http://127.0.0.1:8000/admin