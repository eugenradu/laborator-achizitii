from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user 
from models import (db, ProceduraAchizitie, TipProcedura, Lot, Utilizator, ReferatNecesitate, StareReferat,
                    ProdusInLot, ProdusInReferat, Produs, Oferta, ArticolOferta, LotProcedura)
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from collections import defaultdict

proceduri_bp = Blueprint('proceduri', __name__, url_prefix='/proceduri')

@proceduri_bp.route('/')
@login_required
def list_proceduri():
    """Afișează lista tuturor procedurilor de achiziție."""
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 15

    # Interogare de bază
    query = db.session.query(ProceduraAchizitie, Utilizator)\
        .outerjoin(Utilizator, ProceduraAchizitie.ID_Utilizator_Creare == Utilizator.ID_Utilizator)

    if search_term:
        search_filter = or_(
            ProceduraAchizitie.Nume_Procedura.ilike(f'%{search_term}%'),
            ProceduraAchizitie.Stare.ilike(f'%{search_term}%'),
            Utilizator.Nume_Utilizator.ilike(f'%{search_term}%')
        )
        query = query.filter(search_filter)

    pagination = query.order_by(ProceduraAchizitie.Data_Creare.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    
    return render_template('proceduri.html', pagination=pagination, search_term=search_term)


@proceduri_bp.route('/adauga', methods=['GET', 'POST'])
@login_required
def adauga_procedura():
    """Gestionează crearea antetului unei noi proceduri de achiziție."""
    if request.method == 'POST':
        nume_procedura = request.form.get('nume_procedura')
        tip_procedura_str = request.form.get('tip_procedura')

        if not all([nume_procedura, tip_procedura_str]):
            flash('Numele și tipul procedurii sunt obligatorii.', 'danger')
            return redirect(url_for('proceduri.adauga_procedura'))

        new_procedura = ProceduraAchizitie(
            Nume_Procedura=nume_procedura,
            Tip_Procedura=TipProcedura[tip_procedura_str],
            Stare='In Desfasurare',
            ID_Utilizator_Creare=current_user.ID_Utilizator
        )
        db.session.add(new_procedura)
        db.session.commit()
        flash(f'Procedura "{nume_procedura}" a fost inițiată. Acum puteți adăuga loturi și produse.', 'success')
        return redirect(url_for('proceduri.detalii_procedura', procedura_id=new_procedura.ID_Procedura))

    return render_template('adauga_procedura.html', tipuri_procedura=TipProcedura)

@proceduri_bp.route('/<int:procedura_id>/detalii')
@login_required
def detalii_procedura(procedura_id):
    """Afișează panoul de control pentru o procedură, permițând managementul Super-Loturilor și analiza ofertelor."""
    procedura = ProceduraAchizitie.query.options(
        joinedload(ProceduraAchizitie.creator_procedura),
        joinedload(ProceduraAchizitie.loturi_procedura).joinedload(LotProcedura.articole_incluse).joinedload(ProdusInReferat.produs_generic_req),
        joinedload(ProceduraAchizitie.loturi_procedura).joinedload(LotProcedura.articole_incluse).joinedload(ProdusInReferat.referat_necesitate)
    ).get_or_404(procedura_id)

    # Găsim toate produsele din referate aprobate
    produse_aprobate_query = db.session.query(ProdusInReferat, Produs, ReferatNecesitate)\
        .join(Produs, ProdusInReferat.ID_Produs_Generic == Produs.ID_Produs)\
        .join(ReferatNecesitate, ProdusInReferat.ID_Referat == ReferatNecesitate.ID_Referat)\
        .filter(ReferatNecesitate.Stare == StareReferat.APROBAT)

    # Găsim ID-urile produselor deja alocate în această procedură
    produse_alocate_ids = {
        articol.ID_Produs_Referat
        for lot_proc in procedura.loturi_procedura
        for articol in lot_proc.articole_incluse
    }

    # Filtrăm pentru a obține doar produsele nealocate
    produse_disponibile = [
        (pir, prod, ref) for pir, prod, ref in produse_aprobate_query.all()
        if pir.ID_Produs_Referat not in produse_alocate_ids
    ]

    # --- NOU: Analiza ofertelor pe fiecare Super-Lot ---
    super_loturi_cu_oferte = {}
    for lot_proc in procedura.loturi_procedura:
        produse_in_lot_proc_ids = {articol.ID_Produs_Referat for articol in lot_proc.articole_incluse}

        if not produse_in_lot_proc_ids:
            oferte_si_valori = []
        else:
            # Interogare pentru a obține ofertele și valorile lor pentru acest Super-Lot
            oferte_si_valori = db.session.query(
                Oferta,
                db.func.sum(ArticolOferta.Pret_Unitar_Pachet * ProdusInReferat.Cantitate_Solicitata).label('valoare_lot'),
                db.func.count(ArticolOferta.ID_Articol_Oferta).label('numar_articole_ofertate')
            ).join(ArticolOferta, Oferta.ID_Oferta == ArticolOferta.ID_Oferta)\
             .join(ProdusInReferat, ArticolOferta.ID_Produs_Referat == ProdusInReferat.ID_Produs_Referat)\
             .filter(Oferta.ID_Procedura == procedura_id)\
             .filter(ArticolOferta.ID_Produs_Referat.in_(produse_in_lot_proc_ids))\
             .group_by(Oferta)\
             .order_by('valoare_lot')\
             .all()

        super_loturi_cu_oferte[lot_proc.ID_Lot_Procedura] = {
            'lot_obj': lot_proc,
            'numar_articole_total': len(produse_in_lot_proc_ids),
            'oferte_comparative': oferte_si_valori
        }

    oferte_asociate = Oferta.query.options(joinedload(Oferta.furnizor))\
        .filter_by(ID_Procedura=procedura_id)\
        .order_by(Oferta.Data_Oferta.desc()).all()

    return render_template('detalii_procedura.html', procedura=procedura, produse_disponibile=produse_disponibile,
                           super_loturi_cu_oferte=super_loturi_cu_oferte,
                           oferte_asociate=oferte_asociate)

@proceduri_bp.route('/<int:procedura_id>/adauga_super_lot', methods=['POST'])
@login_required
def adauga_super_lot(procedura_id):
    procedura = ProceduraAchizitie.query.get_or_404(procedura_id)
    nume_lot = request.form.get('nume_lot')
    descriere_lot = request.form.get('descriere_lot')

    if not nume_lot:
        flash('Numele lotului este obligatoriu.', 'danger')
    else:
        new_lot = LotProcedura(
            ID_Procedura=procedura.ID_Procedura,
            Nume_Lot=nume_lot,
            Descriere_Lot=descriere_lot
        )
        db.session.add(new_lot)
        db.session.commit()
        flash(f'Lotul "{nume_lot}" a fost adăugat în procedură.', 'success')
    
    return redirect(url_for('proceduri.detalii_procedura', procedura_id=procedura_id))

@proceduri_bp.route('/super_lot/<int:lot_procedura_id>/adauga_articole', methods=['POST'])
@login_required
def adauga_articole_super_lot(lot_procedura_id):
    lot_procedura = LotProcedura.query.get_or_404(lot_procedura_id)
    articole_ids = request.form.getlist('articole_selectate')

    if not articole_ids:
        flash('Nu ați selectat niciun articol de adăugat.', 'warning')
    else:
        articole_de_adaugat = ProdusInReferat.query.filter(ProdusInReferat.ID_Produs_Referat.in_(articole_ids)).all()
        lot_procedura.articole_incluse.extend(articole_de_adaugat)
        db.session.commit()
        flash(f'{len(articole_de_adaugat)} articol(e) au fost adăugate în lotul "{lot_procedura.Nume_Lot}".', 'success')

    return redirect(url_for('proceduri.detalii_procedura', procedura_id=lot_procedura.ID_Procedura))

@proceduri_bp.route('/super_lot/<int:lot_procedura_id>/sterge_articol/<int:produs_referat_id>', methods=['POST'])
@login_required
def sterge_articol_super_lot(lot_procedura_id, produs_referat_id):
    lot_procedura = LotProcedura.query.get_or_404(lot_procedura_id)
    articol_de_sters = ProdusInReferat.query.get_or_404(produs_referat_id)

    if articol_de_sters in lot_procedura.articole_incluse:
        lot_procedura.articole_incluse.remove(articol_de_sters)
        db.session.commit()
        flash('Articolul a fost scos din lot.', 'success')
    else:
        flash('Eroare: Articolul nu se află în acest lot.', 'danger')

    return redirect(url_for('proceduri.detalii_procedura', procedura_id=lot_procedura.ID_Procedura))

@proceduri_bp.route('/<int:procedura_id>/genereaza_documentatie')
@login_required
def genereaza_documentatie(procedura_id):
    """Generează un fișier .txt cu documentația completă a procedurii."""
    procedura = ProceduraAchizitie.query.get_or_404(procedura_id)

    # Construim conținutul text al documentului
    doc_text = f"DOCUMENTAȚIE PROCEDURĂ DE ACHIZIȚIE\n"
    doc_text += f"{'='*40}\n"
    doc_text += f"Nume Procedură: {procedura.Nume_Procedura}\n"
    doc_text += f"Tip: {procedura.Tip_Procedura.value}\n"
    doc_text += f"Data Inițiere: {procedura.Data_Creare.strftime('%d-%m-%Y')}\n"
    doc_text += f"Stare: {procedura.Stare}\n"
    doc_text += f"{'='*40}\n\n"
    doc_text += f"OBIECTUL ACHIZIȚIEI - LOTURI ȘI PRODUSE\n"
    doc_text += f"{'-'*40}\n"

    # Preluăm loturile și produsele pentru fiecare lot
    for lot_proc in procedura.loturi_procedura:
        doc_text += f"\nLOT #{lot_proc.ID_Lot_Procedura}: {lot_proc.Nume_Lot.upper()}\n"
        if lot_proc.Descriere_Lot:
            doc_text += f"Descriere Lot: {lot_proc.Descriere_Lot}\n"
        doc_text += "\n"

        articole_in_lot = lot_proc.articole_incluse.join(Produs).order_by(Produs.Nume_Generic).all()

        for i, pir in enumerate(articole_in_lot):
            produs = pir.produs_generic_req
            doc_text += f"  {i+1}. {produs.Nume_Generic} (din Ref. #{pir.ID_Referat})\n"
            doc_text += f"     - Cantitate solicitată: {pir.Cantitate_Solicitata} {produs.Unitate_Masura}\n"
            doc_text += f"     - Specificații tehnice minime obligatorii:\n       {produs.Specificatii_Tehnice or 'N/A'}\n\n"

    response = make_response(doc_text)
    response.headers["Content-Disposition"] = f"attachment; filename=documentatie_procedura_{procedura_id}.txt"
    response.headers["Content-type"] = "text/plain; charset=utf-8"
    return response