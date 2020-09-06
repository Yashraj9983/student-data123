from flask import render_template, make_response, request, Flask, redirect, url_for, session
import sqlite3
import os
app = Flask(__name__)
app.secret_key = os.urandom(24) # for security

@app.route('/',methods = ['GET', 'POST'])  
def login(): 
 

    if not (session.get('user')):
        if not request.cookies.get('rollno'):
            if request.method == 'POST':
                uname=request.form.get('uname')  
                passwrd=request.form.get('pass') 
                if uname==passwrd:    
                   roll = str(request.form['roll'])
                   response = make_response("Setting your Cookie and Session! Please refresh the page to see the results - ")
                # make_response binds a certain event, in this case a string , to the formation of a cookie. You may find
                # this function to include redirects or even render templates in other examples. 
                   response.set_cookie('rollno', roll)
                   session['user'] = str(request.form['uname'])
                   return response
        else:
            response = make_response(render_template('home5.html', cookie = str(request.cookies.get('rollno')), user = (str(session.get('user'))),my_string="hey there:",
                            my_list=['one','two','three','four','five']))
            return response
            
    else:
        return render_template('home5.html', cookie = str(request.cookies.get('rollno')), user = (str(session.get('user'))),my_string="hey there:",
                            my_list=['one','two','three','four','five'])

    return render_template('index5.html')
   
  
@app.route('/home', methods=['GET', 'POST'])
def index():
    
    if not (session.get('user')):
        if not request.cookies.get('rollno'):
            if request.method == 'POST':
                uname=request.form.get('uname')  
                passwrd=request.form.get('pass') 
                if uname==passwrd:    
                   roll = str(request.form['roll'])
                   response = make_response("Setting your Cookie and Session! Please refresh the page to see the results - ")
                # make_response binds a certain event, in this case a string , to the formation of a cookie. You may find
                # this function to include redirects or even render templates in other examples. 
                   response.set_cookie('rollno', roll)
                   session['user'] = str(request.form['uname'])
                   return response
        else:
            response = make_response(render_template('home5.html', cookie = str(request.cookies.get('rollno')), user = (str(session.get('user'))),my_string="hey there:",
                            my_list=['one','two','three','four','five']))
            return response
            
    else:
        return render_template('home5.html', cookie = str(request.cookies.get('rollno')), user = (str(session.get('user'))),my_string="hey there:",
                            my_list=['one','two','three','four','five'])


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    connection = sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db')
    cursor = connection.cursor()
    cursor.execute('select * from details')
    all_rows = cursor.fetchall()
    if request.method == 'POST':
        branch = str(request.form['branch'])
        name = str(request.form['name'])
        sem = str(request.form['sem'])
        marks = str(request.form['marks'])
        with sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db') as connection: # This is a context manager!
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO details (name, branch,sem,marks) VALUES (?,?,?,?)", (name, branch,sem,marks))
                connection.commit()
            except Exception as ex:
                message = f"An exception of type {type(ex).__name__} occurred. \nArguments: {ex.args}"
                replacements = [',', '(', ')']
                for _ in replacements:
                    message = message.replace(_, '')
                print(message)

                connection.rollback()
            finally:
                print('Something happened in def insert()')
                return redirect(url_for('insert'))

    return render_template('insert5.html', all_rows = all_rows)

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    with sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select * from details')
        all_rows = cursor.fetchall()
        cursor.execute('select name from details')
        name_rows = cursor.fetchall()
    if request.method == 'POST':
        try:
            with sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db') as connection:
                 branch = str(request.form['branch'])
                 name = str(request.form['name'])
                 sem = str(request.form['sem'])
                 marks = str(request.form['marks'])
                 cursor = connection.cursor()
                 cursor.execute('UPDATE details SET branch = ? , sem = ?,marks=? WHERE name = ?', (branch, sem,marks, name))
                 connection.commit()
        except Exception as ex:
            message = f"An exception of type {type(ex).__name__} occurred. \nArguments: {ex.args}"
            replacements = [',', '(', ')']
            for _ in replacements:
                message = message.replace(_, '')
            print(message)
            connection.rollback()
        finally:
            print('Something happened in def edit()')
            return redirect(url_for('edit'))

    return render_template('edit5.html', name_rows = name_rows, all_rows = all_rows)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    with sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('select * from details')
        all_rows = cursor.fetchall()
    if request.method == 'POST':
        to_delete = request.form['name']
        print(to_delete)
        with sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db') as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM details WHERE name = ?", (to_delete,))
                connection.commit()
            except Exception as ex:
                message = f"An exception of type {type(ex).__name__} occurred. \nArguments: {ex.args}"
                replacements = [',', '(', ')']
                for _ in replacements:
                    message = message.replace(_, '')
                print(message)
                connection.rollback()
            finally:
                print('Something happened in def delete()')
                return redirect(url_for('delete'))

    return render_template('delete5.html', all_rows = all_rows)


@app.route('/results', methods=['GET', 'POST'])
def results():
    connection = sqlite3.connect(r'C:\Users\Admin\Desktop\pybox\demoapp2\database.db')
    cursor = connection.cursor()
    cursor.execute('select * from details')
    all_rows = cursor.fetchall()
    connection.close()
    return render_template('result5.html', all_rows = all_rows)

if __name__ == '__main__':
    app.run(debug=True)











# with sqlite3.connect(r'07Database\SQLite\database.db') as connection:
#             colour = str(request.form['colour'])
#             opinion = str(request.form['opinion'])
#             name = str(request.form['name'])
#             cursor = connection.cursor()
#             cursor.execute('UPDATE details SET colour = ? , opinion = ? WHERE name = ?', (colour, opinion, name))
#             connection.commit()
#             return redirect(url_for('edit'))











 # checked = list(request.form['hidden'])
        # print(checked)
        # name_list = []
        # for row in checked:
        #     if request.form[row]:
        #         print(str(row))
                # name_list.append(str(request.form[str(row[0])]))


        #         for name in name_list:

                # message = "That worked!"
        #         # return redirect(url_for('results'))


        #         message = "That didn't work!"
        #         # return '''<p>That didn't work!</p><p><a href="{{url_for('results')}}">Please click on this link to see the full table</p>'''

        #         # return redirect(url_for('results'))
        #         return render_template('confirmation.html', message = message)
