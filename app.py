from pickle import GET

from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate


from flask_wtf import FlaskForm
import forms
from models import db
from models import Alumnos
from maestros.routes import maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
migrate=Migrate(app,db)

csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

@app.route("/", methods=['GET', 'POST'])
@app.route("/index")	
def index():
	create_form=forms.UserForm(request.form)
	alumno=Alumnos.query.all()
	return render_template("index.html", form=create_form,alumno=alumno)

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
	create_form=forms.UserForm(request.form)
	if request.method == 'POST':
		alum=Alumnos(nombre=create_form.nombre.data,
			   		 apaterno=create_form.apaterno.data,
				     email=create_form.email.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("Alumnos.html", form=create_form)

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
	create_form=forms.UserForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=alum.nombre
		create_form.apaterno.data=alum.apaterno
		create_form.email.data=alum.email

	if request.method == 'POST':
		id=create_form.id.data
		alum=Alumnos.query.get(id)
		db.session.delete(alum)
		db.session.commit()

		return redirect(url_for('index'))
	return render_template("eliminar.html", form=create_form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum = Alumnos.query.get(id)

        if alum:
            create_form.nombre.data = alum.nombre
            create_form.apaterno.data = alum.apaterno
            create_form.email.data = alum.email

        return render_template("modificar.html", form=create_form)

    if request.method == 'POST':
        id = request.args.get('id')
        alum = Alumnos.query.get(id)

        if alum:
            alum.nombre = create_form.nombre.data
            alum.apaterno = create_form.apaterno.data
            alum.email = create_form.email.data
            db.session.commit()

        return redirect(url_for('index'))


@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alum1.nombre
		apaterno=alum1.apaterno
		email=alum1.email
		return render_template("detalles.html", nombre=nombre,
						 apaterno=apaterno, email=email)

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()