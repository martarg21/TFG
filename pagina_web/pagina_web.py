import sys, os
from flask import Flask, render_template, request, redirect, url_for, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from servidorLDAP import conexion_ldap_server,add_new_user, modify_user, search_user, delete_usergroup, archivo_usuario, add_ldap_group, modificar_dn, eliminar_info

app = Flask(__name__)


@app.route('/add', methods=['GET','POST'])
def addUser():
	if request.method == 'POST':
		name = request.form['name']
		last_name = request.form['last_name']
		email = request.form['email']
		userPassword = request.form['userPassword']
		grupo = request.form['grupo']

		ldap_conn = conexion_ldap_server()

		ldap_attr = {'cn': name, 'sn': last_name, 'mail': email, 'userPassword': userPassword}
		response = add_new_user(ldap_conn, name, f"cn={grupo},dc=tfgmarta,dc=es", ldap_attr)
		return redirect(url_for('exito'))
	else:
		return render_template('addUser.html')

@app.route('/exito')
def exito():
	return render_template('exito.html')
    
@app.route('/')
def signUp():
	return render_template('index.html')

@app.route('/page-top')
def pagetop():
	return render_template('index.html')

@app.route('/modify', methods=['GET','POST'])
def modifyUser():
	if request.method == 'POST':
		user_dn = request.form['user_dn']
		name = request.form['name']
		last_name = request.form['last_name']
		email = request.form['email']

		ldap_conn = conexion_ldap_server()

		ldap_attr = {'cn': name, 'sn': last_name, 'mail': email}
		response = modify_user(ldap_conn, user_dn, ldap_attr)
		return redirect(url_for('exito'))
	else:
		return render_template('modifyUser.html')

@app.route('/search', methods=['GET','POST'])
def searchUser():
	if request.method == 'POST':
		name = request.form['name']
		last_name = request.form['last_name']

		ldap_conn = conexion_ldap_server()
		user_dn = f"cn={name},cn={last_name},dc=tfgmarta,dc=es"

		response = search_user(ldap_conn, user_dn)
		response_procesada = []
		for entry in response:
			datos = {'cn': entry['attributes'].get('cn',''), 'sn': entry['attributes'].get('sn',''), 'mail': entry['attributes'].get('mail','')}
			response_procesada.append(datos)
		return render_template('responseSearch.html', response=response_procesada)
	else:
		return render_template('searchUser.html')
	
@app.route('/delete', methods=['GET','POST'])
def deleteUser():
	if request.method == 'POST':
		name = request.form['name']
		last_name = request.form['last_name']

		ldap_conn = conexion_ldap_server()
		user_dn = f"cn={name},cn={last_name},dc=tfgmarta,dc=es"
		
		response = delete_usergroup(ldap_conn, user_dn)
		return redirect(url_for('exito'))
	else:
		return render_template('deleteUser.html')

@app.route('/deleteGroup', methods=['GET','POST'])
def deleteGroup():
	if request.method == 'POST':
		group_name = request.form['name']

		ldap_conn = conexion_ldap_server()
		user_dn = f"cn={group_name},dc=tfgmarta,dc=es"

		response = delete_usergroup(ldap_conn, user_dn)
		return redirect(url_for('exito'))
	else:
		return render_template('deleteGroup.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/addGroup', methods=['GET','POST'])
def addGroup():
	if request.method == 'POST':
		group_name = request.form['name']

		ldap_conn = conexion_ldap_server()

		response = add_ldap_group(ldap_conn, group_name)
		return redirect(url_for('exito'))
	else:
		return render_template('addGroup.html')

@app.route('/deleteInfo', methods=['GET','POST'])
def deleteInfo():
	if request.method == 'POST':
		user_dn = request.form['user_dn']

		ldap_conn = conexion_ldap_server()

		response = eliminar_info(ldap_conn, user_dn)
		return redirect(url_for('exito'))
	else:
		return render_template('deleteInfo.html')

if __name__ == '__main__':
    app.run()
