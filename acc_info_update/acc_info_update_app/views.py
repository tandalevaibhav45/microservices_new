from django.shortcuts import render,redirect
from django.db import connection
cursor = connection.cursor()

def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]
        
def get_update_info(request,pk=0):
    if request.method == 'GET':
        cursor = connection.cursor()
        query = (f"SELECT * FROM demo.user_reg WHERE id ={pk}")
        cursor.execute(query)

        data_all = dictfetchall(cursor)
        return render(request, 'update_acc_info.html', {'data': data_all[0]})
    


def do_update(request, pk=0):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_add = request.POST.get('email_add')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            query = f"""
                UPDATE demo.user_reg
                SET first_name = '{first_name}', last_name = '{last_name}', Contact = {contact},email_add = '{email_add}', Password={password}
                WHERE id = {pk};
            """
            cursor.execute(query) 
        return render(request, 'update_acc_info.html')
    return render(request, 'update_acc_info.html')