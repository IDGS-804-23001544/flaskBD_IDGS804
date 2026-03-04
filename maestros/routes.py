from . import maestros
from flask import render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from maestros.routes import maestros, maestros
from models import db
from models import Maestros
from forms import MaestroForm
 
@maestros.route("/maestros/nuevo", methods=['GET', 'POST'])
def nuevo():
    form = MaestroForm()

    if form.validate_on_submit():

        maestro = Maestros(
            matricula=form.matricula.data,
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )

        db.session.add(maestro)
        db.session.commit()

        return redirect(url_for('maestros.index'))

    return render_template("maestros/crear.html", form=form)


@maestros.route("/maestros/detalles/<int:matricula>")
def detalles(matricula):
    maestro = Maestros.query.get_or_404(matricula)

    return render_template(
        "maestros/detalles.html",
        matricula=maestro.matricula,
        nombre=maestro.nombre,
        apellidos=maestro.apaterno,  
        especialidad=maestro.especialidad,
        email=maestro.email
    )


@maestros.route("/maestros/editar/<int:matricula>", methods=['GET', 'POST'])
def editar(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    form = MaestroForm(obj=maestro)  # Prellenamos con los datos existentes

    if form.validate_on_submit():  # Usamos validate_on_submit() de FlaskForm
        maestro.matricula = form.matricula.data
        maestro.nombre = form.nombre.data
        maestro.apaterno = form.apaterno.data  # CAMBIO aquí
        maestro.especialidad = form.especialidad.data
        maestro.email = form.email.data

        db.session.commit()
        return redirect(url_for('maestros.index'))

    return render_template("maestros/editar.html", form=form)


@maestros.route("/maestros/eliminar/<int:matricula>", methods=['GET', 'POST'])
def eliminar(matricula):
    # Busca el maestro o devuelve 404 si no existe
    maestro = Maestros.query.get_or_404(matricula)
    
    # Crea el formulario con los datos del maestro
    form = forms.MaestroForm(request.form, obj=maestro)

    if request.method == 'POST':
        # Elimina el registro y guarda cambios
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for('maestros.index'))

    # Renderiza la plantilla de confirmación con estilo
    return render_template("maestros/eliminar.html", form=form)


 
@maestros.route("/maestros",methods=['GET','POST'])
@maestros.route("/index")
def index():
    create_form=forms.UserForm(request.form)
    maestros=Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form,maestros=maestros)
 
 
@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"
