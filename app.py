import os
from flask import Flask
from config import Config
from models import db, Utilizator
from flask_login import LoginManager
from datetime import date

# --- Import Blueprints ---
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.produse import produse_bp
from blueprints.referate import referate_bp
from blueprints.oferte import oferte_bp
# Următoarele vor fi create și importate în pașii viitori
from blueprints.furnizori import furnizori_bp
# from blueprints.licitatii import licitatii_bp
# from blueprints.contracte import contracte_bp
from blueprints.api import api_bp

print("--- app.py (re)loaded by Flask reloader ---")

# --- Inițializare Aplicație & Extensii ---
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Punctează către ruta de login din blueprint

# --- Înregistrare Blueprints ---
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(produse_bp)
app.register_blueprint(referate_bp)
app.register_blueprint(oferte_bp)
app.register_blueprint(furnizori_bp)
# app.register_blueprint(licitatii_bp)
# app.register_blueprint(contracte_bp)
app.register_blueprint(api_bp)

# --- User Loader pentru Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return Utilizator.query.get(int(user_id))

# --- Comandă CLI pentru Inițializarea Bazei de Date ---
@app.cli.command("init-db")
def init_db_command():
    """Creează tabelele bazei de date și inițializează un utilizator admin."""
    with app.app_context():
        db.create_all()
        print("Tabelele bazei de date au fost create (sau verificate).")
        
        if not Utilizator.query.filter_by(Nume_Utilizator='admin').first():
            admin_user = Utilizator(Nume_Utilizator='admin', Email='admin@example.com', Data_Creare=date.today())
            admin_user.set_password('adminpass')
            db.session.add(admin_user)
            db.session.commit()
            print("Utilizator 'admin' implicit creat (Nume: admin, Parola: adminpass).")
        else:
            print("Utilizator 'admin' există deja.")
    print("Baza de date a fost inițializată cu succes.")

# ==============================================================================
# TOATE RUTELE AU FOST MUTATE SAU VOR FI MUTATE ÎN BLUEPRINT-URI.
# ACEST FIȘIER VA RĂMÂNE CURAT, DOAR CU LOGICA DE INIȚIALIZARE.
# ==============================================================================

# --- Execuția Principală ---
if __name__ == '__main__':
    # Pentru a asigura reîncărcarea automată, monitorizăm toate fișierele relevante.
    # O abordare dinamică este mai robustă decât o listă hardcodată.
    extra_files = []
    # Adaugă toate template-urile
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                extra_files.append(os.path.join(root, file))
    # Adaugă toate fișierele python din blueprints
    for root, dirs, files in os.walk('blueprints'):
        for file in files:
            if file.endswith('.py'):
                extra_files.append(os.path.join(root, file))
    # Adaugă fișierele principale și CSS
    extra_files.extend(['app.py', 'models.py', 'config.py', 'static/css/style.css'])
    
    app.run(debug=True, extra_files=list(set(extra_files)))
