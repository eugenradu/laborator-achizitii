from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import (db, ProceduraAchizitie, TipProcedura, Lot, Utilizator, ReferatNecesitate, 
                    ProdusInLot, ProdusInReferat, Produs, Oferta)
from datetime import date
from sqlalchemy.orm import joinedload
from collections import defaultdict

proceduri_bp = Blueprint('proceduri', __name__, url_prefix='/proceduri')

@proceduri_bp.route('/')
@login_required
def list_proceduri():
    """Afișează lista tuturor procedurilor de achiziție."""
    proceduri_list = db.session.query(ProceduraAchizitie, Utilizator)\
        .outerjoin(Utilizator, ProceduraAchizitie.ID_Utilizator_Creare == Utilizator.ID_Utilizator)\
        .order_by(ProceduraAchizitie.Data_Creare.desc())\
        .all()
    # Vom crea template-ul 'proceduri.html' în pasul următor
    return render_template('proceduri.html', proceduri=proceduri_list)

@proceduri_bp.route('/adauga', methods=['GET', 'POST'])
@login_required
def adauga_procedura():
    """Gestionează crearea unei noi proceduri de achiziție."""
    if request.method == 'POST':
        nume_procedura = request.form.get('nume_procedura')
        tip_procedura_str = request.form.get('tip_procedura')
        lot_ids = request.form.getlist('loturi_incluse')

        if not all([nume_procedura, tip_procedura_str, lot_ids]):
            flash('Numele, tipul procedurii și selectarea a cel puțin unui lot sunt obligatorii.', 'danger')
            return redirect(url_for('proceduri.adauga_procedura'))

        # Creează noua procedură
        new_procedura = ProceduraAchizitie(
            Nume_Procedura=nume_procedura,
            Tip_Procedura=TipProcedura[tip_procedura_str],
            Stare='In Desfasurare',
            ID_Utilizator_Creare=current_user.ID_Utilizator
        )

        # Asociază loturile selectate
        loturi_selectate = Lot.query.filter(Lot.ID_Lot.in_(lot_ids)).all()
        new_procedura.loturi_incluse.extend(loturi_selectate)

        db.session.add(new_procedura)
        db.session.commit()
        flash(f'Procedura "{nume_procedura}" a fost creată cu succes!', 'success')
        return redirect(url_for('proceduri.list_proceduri'))

    # GET: Pregătește datele pentru formular
    # Preluăm loturile disponibile și le grupăm după referatul părinte
    loturi_disponibile = Lot.query.options(joinedload(Lot.referat_parinte))\
                                  .filter(~Lot.proceduri_asociate.any())\
                                  .order_by(Lot.ID_Referat, Lot.Nume_Lot).all()

    referate_cu_loturi = defaultdict(list)
    for lot in loturi_disponibile:
        # Cheia este obiectul ReferatNecesitate, valoarea este o listă de obiecte Lot
        referate_cu_loturi[lot.referat_parinte].append(lot)

    return render_template('adauga_procedura.html', tipuri_procedura=TipProcedura, referate_cu_loturi=referate_cu_loturi)

@proceduri_bp.route('/<int:procedura_id>/detalii')
@login_required
def detalii_procedura(procedura_id):
    """Afișează detaliile complete ale unei proceduri de achiziție."""
    procedura = ProceduraAchizitie.query.options(
        joinedload(ProceduraAchizitie.creator_procedura)
    ).get_or_404(procedura_id)

    # Preluăm loturile incluse în procedură
    loturi_incluse = procedura.loturi_incluse.order_by(Lot.Nume_Lot).all()

    # Preluăm detaliile pentru fiecare lot (produse)
    detalii_loturi = {}
    for lot in loturi_incluse:
        produse_in_lot = db.session.query(Produs, ProdusInReferat)\
            .join(ProdusInReferat, Produs.ID_Produs == ProdusInReferat.ID_Produs_Generic)\
            .join(ProdusInLot, ProdusInReferat.ID_Produs_Referat == ProdusInLot.ID_Produs_Referat)\
            .filter(ProdusInLot.ID_Lot == lot.ID_Lot)\
            .order_by(Produs.Nume_Generic).all()
        detalii_loturi[lot.ID_Lot] = { 'lot_obj': lot, 'produse': produse_in_lot }

    # Preluăm ofertele asociate cu această procedură
    oferte_asociate = Oferta.query.options(joinedload(Oferta.furnizor)).filter_by(ID_Procedura=procedura_id).all()

    return render_template('detalii_procedura.html', procedura=procedura, detalii_loturi=detalii_loturi, oferte_asociate=oferte_asociate)