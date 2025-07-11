from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Furnizor
from sqlalchemy.exc import IntegrityError

furnizori_bp = Blueprint('furnizori', __name__, url_prefix='/furnizori')

@furnizori_bp.route('/')
@login_required
def list_furnizori():
    """Afișează lista tuturor furnizorilor."""
    furnizori_list = Furnizor.query.order_by(Furnizor.Nume_Furnizor).all()
    return render_template('furnizori.html', furnizori=furnizori_list)

@furnizori_bp.route('/adauga', methods=['GET', 'POST'])
@login_required
def adauga_furnizor():
    """Gestionează adăugarea unui nou furnizor."""
    if request.method == 'POST':
        nume_furnizor = request.form.get('nume_furnizor', '').strip()
        cui = request.form.get('cui', '').strip() or None
        adresa = request.form.get('adresa', '').strip() or None
        persoana_contact = request.form.get('persoana_contact', '').strip() or None
        email_contact = request.form.get('email_contact', '').strip() or None
        telefon_contact = request.form.get('telefon_contact', '').strip() or None

        if not nume_furnizor:
            flash('Numele furnizorului este obligatoriu.', 'danger')
            return render_template('adauga_furnizor.html', form_data=request.form)

        new_furnizor = Furnizor(
            Nume_Furnizor=nume_furnizor,
            CUI=cui,
            Adresa=adresa,
            Persoana_Contact=persoana_contact,
            Email_Contact=email_contact,
            Telefon_Contact=telefon_contact
        )
        db.session.add(new_furnizor)
        try:
            db.session.commit()
            flash(f'Furnizorul "{nume_furnizor}" a fost adăugat cu succes!', 'success')
            return redirect(url_for('furnizori.list_furnizori'))
        except IntegrityError:
            db.session.rollback()
            flash('Un furnizor cu acest nume sau CUI există deja.', 'danger')

    return render_template('adauga_furnizor.html', form_data={})

@furnizori_bp.route('/edit/<int:furnizor_id>', methods=['GET', 'POST'])
@login_required
def edit_furnizor(furnizor_id):
    """Gestionează editarea unui furnizor existent."""
    furnizor = Furnizor.query.get_or_404(furnizor_id)

    if request.method == 'POST':
        furnizor.Nume_Furnizor = request.form.get('nume_furnizor', '').strip()
        furnizor.CUI = request.form.get('cui', '').strip() or None
        furnizor.Adresa = request.form.get('adresa', '').strip() or None
        furnizor.Persoana_Contact = request.form.get('persoana_contact', '').strip() or None
        furnizor.Email_Contact = request.form.get('email_contact', '').strip() or None
        furnizor.Telefon_Contact = request.form.get('telefon_contact', '').strip() or None

        if not furnizor.Nume_Furnizor:
            flash('Numele furnizorului este obligatoriu.', 'danger')
        else:
            try:
                db.session.commit()
                flash('Datele furnizorului au fost actualizate cu succes!', 'success')
                return redirect(url_for('furnizori.list_furnizori'))
            except IntegrityError:
                db.session.rollback()
                flash('Un alt furnizor cu acest nume sau CUI există deja.', 'danger')
    
    return render_template('edit_furnizor.html', furnizor=furnizor)

@furnizori_bp.route('/sterge/<int:furnizor_id>', methods=['POST'])
@login_required
def sterge_furnizor(furnizor_id):
    """Gestionează ștergerea unui furnizor."""
    furnizor = Furnizor.query.get_or_404(furnizor_id)

    if furnizor.oferte or furnizor.contracte:
        flash(f'Furnizorul "{furnizor.Nume_Furnizor}" nu poate fi șters deoarece are oferte sau contracte asociate.', 'danger')
    else:
        db.session.delete(furnizor)
        db.session.commit()
        flash(f'Furnizorul "{furnizor.Nume_Furnizor}" a fost șters cu succes.', 'success')
    
    return redirect(url_for('furnizori.list_furnizori'))