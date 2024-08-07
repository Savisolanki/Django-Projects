import os
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .django_development_server import create_django_project_view
from .code_gen import *
import os
from django.shortcuts import render

def generate_code(request):
    if request.method == 'POST':
        db_name = request.POST.get('db_name')
        table_name = request.POST.get('table_name')
        columns = request.POST.getlist('columns[]')
        data_types = request.POST.getlist('data_types[]')

        # Generate code
        model_code = generate_model_code(db_name, table_name, columns, data_types)
        views_code = generate_views_code(db_name, table_name, columns)
        index_html_code = generate_index_html_code(table_name, columns)
        edit_html_code = generate_edit_html_code(table_name,columns)


        context = {
            'db_name': db_name,
            'table_name': table_name,
            'columns': columns,
            'data_type': data_types,
            'model_code': model_code,
            'views_code': views_code,
            'index_html_code': index_html_code,
            'edit_html_code':edit_html_code,
            # 'folder_path': folder_path,  # Include the folder path in context
        }

        return render(request, 'codegenerator/show_code.html', context)

    return render(request, 'codegenerator/generate_code.html')
