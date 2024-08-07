def generate_model_code(db_name, table_name, columns, data_types):
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    model_code = f"from django.db import models\n\n\n"
    model_code += f"class {class_name}(models.Model):\n"
    seen_columns = set()

    for column, data_type in zip(columns, data_types):
        column_name = column.strip()
        if column_name in seen_columns:
            continue
        seen_columns.add(column_name)

        # Corrected conditionals for data type
        if data_type in ['int']:
            field_type = "IntegerField()"
        elif data_type in ['float']:
            field_type = "FloatField()"
        elif data_type in ['date']:
            field_type = "DateField()"
        elif data_type in ['varchar']:
            field_type = "CharField(max_length=255)"
        else:
            field_type = "TextField(max_length=255)"  # Default field type
        # print(data_type)

        model_code += f"    {column_name} = models.{field_type}\n"

    model_code += f"\n    def __str__(self):\n"
    model_code += f"        return str(self.{columns[0].strip()})\n"

    return model_code


def generate_views_code(db_name, table_name, columns):
    class_name = ''.join(word.capitalize() for word in table_name.split('_'))
    views_code = f"from django.shortcuts import render, redirect\n"
    views_code += f"from .models import {class_name}\n"
    views_code += f"from django.contrib import messages\n\n"

    # Index view
    views_code += f"def index(request):\n"
    views_code += f"    data = {class_name}.objects.all()\n"
    views_code += f"    context = {{'data': data}}\n"
    views_code += f"    return render(request, 'index.html', context)\n\n"
    
    # Insert view
    views_code += f"def insertData(request):\n"
    views_code += f"    if request.method == 'POST':\n"
    for column in columns:
        views_code += f"        {column} = request.POST.get('{column}')\n"
    views_code += f"        query = {class_name}({', '.join(f'{column}={column}' for column in columns)})\n"
    views_code += f"        query.save()\n"
    views_code += f"        messages.info(request, 'Data Inserted Successfully')\n"
    views_code += f"        return redirect('/')\n"
    views_code += f"    return render(request, 'index.html')\n\n"
    
    # Update view
    views_code += f"def updateData(request, id):\n"
    views_code += f"    if request.method == 'POST':\n"
    for column in columns:
        views_code += f"        {column} = request.POST['{column}']\n"
    views_code += f"        edit = {class_name}.objects.get(id=id)\n"
    for column in columns:
        views_code += f"        edit.{column} = {column}\n"
    views_code += f"        edit.save()\n"
    views_code += f"        messages.warning(request, 'Data Updated Successfully')\n"
    views_code += f"        return redirect('/')\n"
    views_code += f"    d = {class_name}.objects.get(id=id)\n"
    views_code += f"    context = {{'d': d}}\n"
    views_code += f"    return render(request, 'edit.html', context)\n\n"
    
    # Delete view
    views_code += f"def deleteData(request, id):\n"
    views_code += f"    d = {class_name}.objects.get(id=id)\n"
    views_code += f"    d.delete()\n"
    views_code += f"    messages.error(request, 'Data Deleted Successfully')\n"
    views_code += f"    return redirect('/')\n" 
    
    return views_code

def generate_index_html_code(table_name, columns):
    index_html_code = f"<!DOCTYPE html>\n"
    index_html_code += f"<html lang=\"en\">\n"
    index_html_code += f"  <head>\n"
    index_html_code += f"    <meta charset=\"UTF-8\">\n"
    index_html_code += f"    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
    index_html_code += f"    <title>CRUD MINI PROJECT</title>\n"
    index_html_code += f"    <!-- Bootstrap CSS -->\n"
    index_html_code += f"    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css\" integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\" crossorigin=\"anonymous\">\n"
    index_html_code += f"    <!-- Optional JavaScript -->\n"
    index_html_code += f"    <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n"
    index_html_code += f"    <script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script>\n"
    index_html_code += f"    <script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js\" integrity=\"sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1\" crossorigin=\"anonymous\"></script>\n"
    index_html_code += f"    <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js\" integrity=\"sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM\" crossorigin=\"anonymous\"></script>\n"
    index_html_code += f"  </head>\n"
    index_html_code += f"  <body>\n"
    index_html_code += f"    <nav class=\"navbar navbar-expand-lg navbar-dark bg-dark\">\n"
    index_html_code += f"      <div class=\"container\">\n"
    index_html_code += f"        <a class=\"navbar-brand\" href=\"#\">CRUD MINI PROJECT</a>\n"
    index_html_code += f"      </div>\n"
    index_html_code += f"    </nav>\n"
    index_html_code += f"    <div class=\"container mt-5\">\n"
    index_html_code += f"      <div class='row'>\n"
    index_html_code += f"        <div class='col-md-4'>\n"
    index_html_code += f"          <h2 class='text-white bg-dark text-center p-3'>Insert {table_name.capitalize()} Details</h2>\n"
    index_html_code += f"          <br>\n"
    index_html_code += f"          <form action='/insert' method='post'>\n"
    index_html_code += f"           {{% csrf_token %}}\n"

    for column in columns:
        index_html_code += f"            <div class='form-group'>\n"
        index_html_code += f"              <input type='text' class='form-control' placeholder='Enter the {column.capitalize().replace('_', ' ')}' name='{column}' required>\n"
        index_html_code += f"            </div>\n"

    index_html_code += f"            <div class=\"form-group\">\n"
    index_html_code += f"              <button class=\"btn btn-success btn-block mt-2\" type=\"submit\">Submit</button>\n"
    index_html_code += f"            </div>\n"
    index_html_code += f"          </form>\n"
    index_html_code += f"        </div>\n"
    index_html_code += f"        <div class='col-md-8'>\n"
    index_html_code += f"          <h2 class='text-center text-white bg-dark p-3'>{table_name.capitalize()} Details</h2>\n"
    index_html_code += f"          {{% for message in messages %}}\n"
    index_html_code += f"          <div class=\"alert alert-{{{{ message.tags }}}} alert-dismissible fade show\" role=\"alert\">\n"
    index_html_code += f"            <strong>{{{{ message }}}}</strong>\n"
    index_html_code += f"            <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">\n"
    index_html_code += f"              <span aria-hidden=\"true\">&times;</span>\n"
    index_html_code += f"            </button>\n"
    index_html_code += f"          </div>\n"
    index_html_code += f"          {{% endfor %}}\n"
    index_html_code += f"          <table class=\"table\">\n"
    index_html_code += f"            <thead>\n"
    index_html_code += f"              <tr>\n"

    for column in columns:
        index_html_code += f"                <th scope=\"col\">{column.capitalize().replace('_', ' ')}</th>\n"

    index_html_code += f"                <th scope=\"col\">Edit</th>\n"
    index_html_code += f"                <th scope=\"col\">Delete</th>\n"
    index_html_code += f"              </tr>\n"
    index_html_code += f"            </thead>\n"
    index_html_code += f"            <tbody>\n"
    index_html_code += f"              {{% for d in data %}}\n"
    index_html_code += f"              <tr>\n"

    for column in columns:
        # index_html_code += f"                <th scope=\"row\">{{{{ d.id }}}}</th>\n"
        index_html_code += f"                <td>{{{{ d.{column} }}}}</td>\n"

    index_html_code += f"                <td><a type=\"button\" href='/update/{{{{ d.id }}}}' class=\"btn btn-outline-primary\">Edit</a></td>\n"
    index_html_code += f"                <td><a type=\"button\" href='/delete/{{{{ d.id }}}}' class=\"btn btn-outline-danger\">Delete</a></td>\n"
    index_html_code += f"              </tr>\n"
    index_html_code += f"              {{% endfor %}}\n"
    index_html_code += f"            </tbody>\n"
    index_html_code += f"          </table>\n"
    index_html_code += f"        </div>\n"
    index_html_code += f"      </div>\n"
    index_html_code += f"    </div>\n"
    index_html_code += f"  </body>\n"
    index_html_code += f"</html>\n"

    return index_html_code


def generate_edit_html_code(table_name, columns):
    edit_html_code = f"<!doctype html>\n"
    edit_html_code += f"<html lang=\"en\">\n"
    edit_html_code += f"  <head>\n"
    edit_html_code += f"    <!-- Required meta tags -->\n"
    edit_html_code += f"    <meta charset=\"utf-8\">\n"
    edit_html_code += f"    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">\n"
    edit_html_code += f"\n"
    edit_html_code += f"    <!-- Bootstrap CSS -->\n"
    edit_html_code += f"    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css\" integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\" crossorigin=\"anonymous\">\n"
    edit_html_code += f"\n"
    edit_html_code += f"    <title>CRUD MINI PROJECT</title>\n"
    edit_html_code += f"  </head>\n"
    edit_html_code += f"  <body>\n"
    edit_html_code += f"    <nav class=\"navbar navbar-expand-lg navbar-dark bg-dark\">\n"
    edit_html_code += f"      <div class=\"container\">\n"
    edit_html_code += f"        <a class=\"navbar-brand\" href=\"#\">CRUD MINI PROJECT UPDATE</a>\n"
    edit_html_code += f"      </div>\n"
    edit_html_code += f"    </nav>\n"
    edit_html_code += f"\n"
    edit_html_code += f"    <div class=\"container mt-5\">\n"
    edit_html_code += f"      <div class='row'>\n"
    edit_html_code += f"        <div class='col-md-4'>\n"
    edit_html_code += f"          <h2 class='text-white bg-info text-center p-3'>Update {table_name.capitalize()} Details</h2>\n"
    edit_html_code += f"          <br>\n"
    edit_html_code += f"          <form action='/update/{{{{ d.id }}}}' method='post'>\n"
    edit_html_code += f"             {{% csrf_token %}}\n"

    for column in columns:
        edit_html_code += f"            <div class='form-group'>\n"
        edit_html_code += f"              <input type='text' class='form-control' placeholder='Enter the {column.capitalize().replace('_', ' ')}' name='{column}' value=\"{{{{ d.{column} }}}}\" required>\n"
        edit_html_code += f"            </div>\n"

    edit_html_code += f"            <div class=\"form-group\">\n"
    edit_html_code += f"              <button class=\"btn btn-success btn-block mt-2\" type=\"submit\">Update</button>\n"
    edit_html_code += f"            </div>\n"
    edit_html_code += f"          </form>\n"
    edit_html_code += f"        </div>\n"
    edit_html_code += f"      </div>\n"
    edit_html_code += f"    </div>\n"
    edit_html_code += f"\n"
    edit_html_code += f"    <script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script>\n"
    edit_html_code += f"    <script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js\" integrity=\"sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1\" crossorigin=\"anonymous\"></script>\n"
    edit_html_code += f"    <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js\" integrity=\"sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM\" crossorigin=\"anonymous\"></script>\n"
    edit_html_code += f"  </body>\n"
    edit_html_code += f"</html>\n"
    
    return edit_html_code
