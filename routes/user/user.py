from flask import Blueprint,request,jsonify,render_template,redirect
from sqlalchemy import exc 
from models import User
from app import db,bcrypt
from auth import tokenCheck,verificar


appuser=Blueprint('appuser',__name__,template_folder="templates")

@appuser.route("/")
def index():
    return render_template("index.html")

@appuser.route("/auth/registro",methods=["POST"])
def registro():
    user = request.get_json()
    userExists=User.query.filter_by(email=user['email']).first()
    if not userExists:
        usuario=User(email=user['email'],password=user['password'])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario Creado"
        except exc.SQLAlchemyError as e:
            mensaje="ERROR "+e
    return jsonify({"message":mensaje})

@appuser.route('/auth/login',methods=["POST"])
def login():
    user = request.get_json()
    usuario = User(email=user['email'],password=user['password'])
    searchUser = User.query.filter_by(email=usuario.email).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,user["password"])
        if validation:
            auth_token=usuario.encode_auth_token(user_id=searchUser.id)
            response = {
                'status':'success',
                'message':'Login exitoso',
                'auth_token':auth_token
            }
            return jsonify(response)
    return jsonify({"message":"Datos incorrectos"})

@appuser.route('/usuarios',methods=['GET'])
@tokenCheck
def getUsers(usuario):
    print(usuario)
    print(usuario['admin'])
    if usuario['admin']:
        output=[]
        usuarios=User.query.all()
        for usuario in usuarios:
            usuarioData={}
            usuarioData['id']=usuario.id
            usuarioData['email']=usuario.email
            usuarioData['password']=usuario.password
            usuarioData['registered_on']=usuario.registered_on
            output.append(usuarioData)
        return jsonify({'usuarios':output})
    else:
        return jsonify({'Error':"No tienes permisos"})
    
@appuser.route('/main')
def main():
    return render_template('main.html')

@appuser.route('/login',methods=["GET","POST"])
def login_post():
    if(request.method=="GET"):
        token = request.args.get('token')
        if token:
            info = verificar(token)
            if(info['status']!="fail"):
                responseObject={
                    'status':"success",
                    'message':'valid token',
                    'info':info
                }
                return jsonify(responseObject)
        return render_template('login.html')
    else:
        email =request.json['email']
        password=request.json['password']
        print(request.json)
        usuario = User(email=email,password=password)
        searchUser = User.query.filter_by(email=email).first()
        if searchUser:
            validation = bcrypt.check_password_hash(searchUser.password,password)
            if validation:
                auth_token = usuario.encode_auth_token(user_id=searchUser.id)
                responseObject={
                    'status':"success",
                    'login':'Loggin exitoso',
                    'auth_token':auth_token
                }
                return jsonify(responseObject)
        return jsonify({'message':"Datos incorrectos"})
    
@appuser.route('/sign',methods=["GET","POST"])
def logint_post():
    if request.method=="GET":
        return render_template('register.html')
    else:
        email=request.json['email']
        password=request.json['password']
        usuario = User(email=email,password=password)
        userExists = User.query.filter_by(email=email).first()
        if not userExists:
            try:
                db.session.add(usuario)
                db.session.commit()
                responseObject={
                    'status':'success',
                    'message':"Registro exitoso"
                }
            except exc.SQLAlchemyError as e:
                responseObject={
                    'status':'error',
                    'message':e
                }
        else:
            responseObject={
                'status':'error',
                'message':'usuario existente'
            }
        return jsonify(responseObject)