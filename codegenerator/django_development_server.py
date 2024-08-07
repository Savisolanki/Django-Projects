import os
from subprocess import call
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .code_gen import *


@csrf_exempt
def create_django_project_view(request):
    if request.method == 'POST':
        db_name = request.POST.get('db_name')
        table_name = request.POST.get('table_name')
        columns = request.POST.getlist('columns[]')
        data_types = request.POST.getlist('data_type[]')
        print(f"dataTypes- {data_types}")

        source_folder = 'C:/Users/savis/Desktop/Django CRUD Operations/new_project'


        if not db_name or not table_name or not source_folder:
            return JsonResponse({'message': 'Invalid data received'}, status=400)

        try:
            create_django_project(db_name, table_name, columns, data_types, source_folder)
            return JsonResponse({'message': 'Django project created successfully'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

def create_django_project(db_name, table_name, columns, data_types, source_folder):
    # Create directory structure
    folder_path = source_folder
    os.makedirs(folder_path, exist_ok=True)

    project_path = os.path.join(source_folder, db_name)
    print(source_folder)
    os.chdir(source_folder)
    call(['django-admin', 'startproject', db_name])
    
    # Navigate into the project directory
    os.chdir(project_path)
    
    # Step 2: Create Django App
    call(['python', 'manage.py', 'startapp', table_name])

    # Define paths for the app and templates
    app_path = os.path.join(project_path, table_name)
    templates_path = os.path.join(project_path, 'templates')
    os.makedirs(templates_path, exist_ok=True)

    # Create directories and files for the app
    for filename in ['models.py', 'views.py', 'urls.py']:
        with open(os.path.join(app_path, filename), 'w') as f:
            if filename == 'models.py':
                model_code = generate_model_code(db_name, table_name, columns, data_types)
                print('code generated')
                f.write(model_code)
                f.close()
            elif filename == 'views.py':
                views_code = generate_views_code(db_name, table_name, columns)
                f.write(views_code)
                f.close()
            elif filename == 'urls.py':
                urls_code = f"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='home'),
]
"""
                f.write(urls_code)

    # Create index.html in the templates directory
    index_html_code = generate_index_html_code(table_name, columns)
    with open(os.path.join(templates_path, 'index.html'), 'w') as f:
        f.write(index_html_code)

    #Create edit.html in the templates directory
    edit_html_code = generate_edit_html_code(table_name,columns)
    with open(os.path.join(templates_path,'edit.html'),'w') as f:
        f.write(edit_html_code)

    # Append a view to render index.html
    with open(os.path.join(app_path, 'views.py'), 'a') as f:
        f.write(f"""
from django.shortcuts import render
from .models import {table_name.capitalize()}

def my_view(request):
    data = {table_name.capitalize()}.objects.all()
    return render(request, 'index.html', {{'data': data}})
""")

    # Define the path to the urls.py file
    urls_path = os.path.join(project_path, db_name, 'urls.py')

    # Read the existing content of urls.py
    with open(urls_path, 'r') as f:
        urls_content = f.read()

    # Ensure the import statement is present
    if "from django.urls import path, include" not in urls_content:
        urls_content = "from django.urls import path, include\n" + urls_content

    # Insert the new path into the urlpatterns list
    urlpatterns_start = urls_content.find('urlpatterns')
    urlpatterns_list_start = urls_content.find('[', urlpatterns_start) + 1
    urlpatterns_list_end = urls_content.find(']', urlpatterns_list_start)

    new_path = f"\n    path('', include('{table_name}.urls')),"

    if new_path not in urls_content:
        urls_content = (
            urls_content[:urlpatterns_list_start] +
            new_path +
            urls_content[urlpatterns_list_start:]
        )

    # Write the updated content back to urls.py
    with open(urls_path, 'w') as f:
        f.write(urls_content)

    settings_path = os.path.join(project_path, db_name, 'settings.py')

    with open(settings_path, 'r') as f:
        settings_content = f.read()

    # Update INSTALLED_APPS
    installed_apps_index = settings_content.find('INSTALLED_APPS')
    start_index = settings_content.find('[', installed_apps_index) + 1
    end_index = settings_content.find(']', start_index)

    apps_list = settings_content[start_index:end_index].strip()
    if f"'{table_name}'" not in apps_list:
        updated_apps_list = apps_list.rstrip(',') + f",\n    '{table_name}',"
        settings_content = (
            settings_content[:start_index] +
            updated_apps_list +
            settings_content[end_index:]
        )

    # Update TEMPLATES
    templates_index = settings_content.find('TEMPLATES')
    dirs_index = settings_content.find('DIRS', templates_index)

    dirs_start_index = settings_content.find('[', dirs_index)
    dirs_end_index = settings_content.find(']', dirs_start_index)

    dirs_content = settings_content[dirs_start_index:dirs_end_index].strip()
    if "'templates'" not in dirs_content:
        updated_dirs_content = dirs_content.rstrip(']') + "'templates'"
        settings_content = (
            settings_content[:dirs_start_index] +
            updated_dirs_content +
            settings_content[dirs_end_index:]
        )

    # Append MESSAGE_TAGS configuration
    additional_settings = """
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.ERROR: 'danger'
}
    """

# Write updated settings content back to file
    with open(settings_path, 'w') as f:
        f.write(settings_content)
        f.write(additional_settings)

    admins_path=os.path.join(project_path,table_name,'admin.py')
    with open(admins_path,'a') as f:
        f.write(f"""
 
from .models import {table_name}\n 
admin.site.register({table_name})
""")
        
        # Define the path to the table_name's urls.py file
    table_urls_path = os.path.join(project_path, table_name, 'urls.py')

    # Ensure the directory exists and create the urls.py file if it does not exist
    os.makedirs(os.path.dirname(table_urls_path), exist_ok=True)
    if not os.path.exists(table_urls_path):
        with open(table_urls_path, 'w') as f:
            f.write("from django.urls import path\nfrom . import views\n\nurlpatterns = []\n")

    # Read the existing content of urls.py
    with open(table_urls_path, 'r') as f:
        table_urls_content = f.read()

    # Remove the specific line if it exists
    lines = table_urls_content.split('\n')
    lines = [line for line in lines if "path('', views.my_view, name='home')" not in line]
    table_urls_content = '\n'.join(lines)

    # Define the new URL patterns
    new_urls = """    path('', views.index, name='index'),
        path('insert', views.insertData, name='insertData'),
        path('update/<int:id>', views.updateData, name='updateData'),
        path('delete/<int:id>', views.deleteData, name='deleteData'),\n"""

    # Find the position of 'urlpatterns' and the start and end of the list
    urls_start = table_urls_content.find('urlpatterns')
    url_list_start = table_urls_content.find('[', urls_start) + 1
    url_list_end = table_urls_content.find(']', url_list_start)

    # Insert the new URL patterns if not already present
    if new_urls not in table_urls_content:
        table_urls_content = (
            table_urls_content[:url_list_start] +
            new_urls +
            table_urls_content[url_list_start:]
        )

    # Write the updated content back to urls.py
    with open(table_urls_path, 'w') as f:
        f.write(table_urls_content)

    call(['python', 'manage.py', 'makemigrations'])

        # Step 7: Migrate the database
    call(['python', 'manage.py', 'migrate'])

        # Step 8: Run the Django server
    print("Starting the Django development server...")
    call(['python', 'manage.py', 'runserver'])


# Make sure to adjust the following paths and the view for your Django application
if __name__ == "__main__":
    create_django_project('my_db', 'my_table', 'new_project/my_db/my_table')
