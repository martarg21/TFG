from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE, BASE, Tls
from ldap3.core.exceptions import LDAPException, LDAPBindError
import ldif, base64, ssl, hashlib

# Conexión servidor
def conexion_ldap_server():

	try:

		server_uri = f"ldap://127.0.0.1:389"
		server = Server(server_uri, get_info=ALL)
		connection = Connection(server, user='cn=admin,dc=tfgmarta,dc=es', password='tfg24', auto_bind = True)
		return connection

	except LDAPBindError as e:
		print (e)

# Crear nuevo grupo
def add_ldap_group(ldap_conn, group_name):

	ldap_attr = {}
	ldap_attr['objectClass'] = ['top','posixGroup']
	ldap_attr['gidNumber'] = '500'

	try:
		response = ldap_conn.add(f'cn={group_name},dc=tfgmarta,dc=es',attributes=ldap_attr)
	except LDAPException as e:
		response = ("The error is ", e)
	return response

# Añadir nuevo usuario
def add_new_user(ldap_conn, nombre_usuario, path_grupo, ldap_attr):

	user_dn = f'cn={nombre_usuario},{path_grupo}'

	try:
		response = ldap_conn.add(dn=user_dn,object_class='inetOrgPerson',attributes=ldap_attr)
		print(response)
	except LDAPException as e:
		response = e
		print(response)
	return response

# Eliminar un usuario y un grupo
def delete_usergroup(ldap_conn, user_dn):
	try:
		response = ldap_conn.delete(dn=user_dn)
	except LDAPException as e:
		response = e
	return response

# Modificar usuarios
def modify_user(ldap_conn, user_dn, ldap_attr):

	try:
		response = ldap_conn.modify(user_dn,{'cn': [(MODIFY_REPLACE, [ldap_attr["cn"]])], 'sn': [(MODIFY_REPLACE, [ldap_attr["sn"]])], 'mail': [(MODIFY_REPLACE, [ldap_attr["mail"]])]})
	except LDAPException as e:
		response = e
	return response
 
# Buscar usuarios
def search_user(ldap_conn, user_dn):

	try:
		response = ldap_conn.search(search_base=user_dn, search_filter="(objectClass=inetOrgPerson)",search_scope=SUBTREE,attributes=['cn', 'sn', 'mail'])
	except LDAPException as e:
		response = e
	return ldap_conn.response

# Archivo usuarios
def archivo_usuario(ldap_conn):

	with open('archivo_usuario.ldif', 'r', encoding='utf-8') as f:
		parser = ldif.LDIFRecordList(f)
		parser.parse()
		records = parser.all_records
	for record in records:
		user_password = record[1].get('userPassword', '')
		print(user_password)
		hash_password = hashlib.sha256(user_password[0]).hexdigest()
		ldap_attr = {'sn': record[1].get('sn',''), 'mail': record[1].get('mail', ''), 'description': record[1].get('description', ''), 'employeeType': record[1].get('employeeType', ''), 'userPassword': hash_password}
		cn = record[1].get('cn')[0].decode('utf-8')
		add_new_user(ldap_conn, cn, "cn=grupo1,dc=tfgmarta,dc=es", ldap_attr)

# Borrar toda la info
def eliminar_info(ldap_conn, user_dn):
	usuarios = search_user(ldap_conn, user_dn)
	for user in usuarios:
		resultado = user['dn']
		delete_usergroup(ldap_conn, resultado)
		
def main():
	conn = conexion_ldap_server()
	print (conn)
if __name__ == "__main__":
	main()
