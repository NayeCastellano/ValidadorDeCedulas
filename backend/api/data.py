usuarios = [
    { "email": "presidente@pucetec.com", "password": "presidente01", "cargo": "Presidente" },
    { "email": "regional@pucetec.com", "password": "regional01", "cargo": "Regional" },
    { "email": "secreazuay@pucetec.com", "password": "azuay01", "cargo": "Secretario" },
    { "email": "secrebolivar@pucetec.com", "password": "bolivar02", "cargo": "Secretario" },
]

def obtener_usuarios():
    return usuarios

def obtenerUsuario(email, password):
    print(email)
    print(password)
    usuarios=obtener_usuarios()
    usuarioEncontrado = None
    for usuario in usuarios:
        if usuario["email"]  == email  and usuario["password"] == password :
            usuarioEncontrado = usuario
    return usuarioEncontrado
      
#found = obtenerUsuario("secreextranjero@pucetec.com", "extranjero30")