from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import date
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import or_
from models import (db, Oferta, ArticolOferta, VariantaComercialaProdus, Produs,
                    ProceduraAchizitie, Furnizor, LotProcedura, ProdusInReferat, ReferatNecesitate)

oferte_bp = Blueprint('oferte', __name__, url_prefix='/oferte')

@oferte_bp.route('/')
@login_required
def list_oferte():
    """Afișează o listă cu toate ofertele înregistrate, cu căutare și paginare."""
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 15
    query = Oferta.query.options(joinedload(Oferta.furnizor))
    if search_term:
        query = query.join(Furnizor).filter(
            or_(
                Furnizor.Nume_Furnizor.ilike(f'%{search_term}%'),
                Oferta.Numar_Inregistrare.ilike(f'%{search_term}%')
            )
        )
    pagination = query.order_by(Oferta.Data_Oferta.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    return render_template('oferte.html', oferte=pagination.items, pagination=pagination, search_term=search_term)

@oferte_bp.route('/adauga', methods=['GET', 'POST'])
@oferte_bp.route('/adauga/<string:context>/<int:context_id>', methods=['GET', 'POST'])
@login_required
def adauga_oferta(context=None, context_id=None):
    """Gestionează adăugarea unei oferte, flexibil: procedură, referat sau spontană."""

    # --- Validare context
    if context and context not in ['procedura', 'referat']:
        flash('Context invalid pentru adăugarea ofertei.', 'danger')
        return redirect(url_for('main.index'))  # Sau altă pagină relevantă

    # --- Logica POST ---
    if request.method == 'POST':
        id_furnizor = request.form.get('id_furnizor', type=int)
        data_oferta_str = request.form.get('data_oferta')
        numar_inregistrare = request.form.get('numar_inregistrare')
        data_inregistrare_str = request.form.get('data_inregistrare')
        moneda = request.form.get('moneda', 'RON')

        if not id_furnizor or not data_oferta_str:
            flash('Furnizorul și data ofertei sunt obligatorii.', 'danger')
            return redirect(request.referrer)

        new_oferta = Oferta(
            ID_Furnizor=id_furnizor,
            Data_Oferta=date.fromisoformat(data_oferta_str),
            Numar_Inregistrare=numar_inregistrare,
            Data_Inregistrare=date.fromisoformat(data_inregistrare_str) if data_inregistrare_str else None,
            Moneda=moneda,
        )

        if context == 'procedura':
            new_oferta.ID_Procedura = context_id
        elif context == 'referat':
            new_oferta.ID_Referat = context_id

        db.session.add(new_oferta)
        db.session.commit()

        # Articole
        produse_ids = request.form.getlist('id_produs_referat[]')
        variante_ids = request.form.getlist('id_varianta_comerciala[]')
        preturi = request.form.getlist('pret_unitar_pachet[]')
        observatii_list = request.form.getlist('observatii[]')

        for i in range(len(produse_ids)):
            if  produse_ids[i] and variante_ids[i] and preturi[i]:
                new_articol = ArticolOferta(
                    ID_Oferta=new_oferta.ID_Oferta,
                    ID_Produs_Referat=int(produse_ids[i]),
                    ID_Varianta_Comerciala=int(variante_ids[i]),
                    Pret_Unitar_Pachet=float(preturi[i]),
                    Observatii=observatii_list[i]
                )
                db.session.add(new_articol)

        db.session.commit()
        flash('Oferta a fost adăugată cu succes!', 'success')
        if context == 'procedura':
            return redirect(url_for('proceduri.detalii_procedura', procedura_id=context_id))
        elif context == 'referat':
            return redirect(url_for('referate.detalii_referat', referat_id=context_id))
        else:
            return redirect(url_for('oferte.list_oferte'))

    # --- Logica GET ---
    furnizori = Furnizor.query.order_by(Furnizor.Nume_Furnizor).all()
    variante_comerciale = VariantaComercialaProdus.query.options(joinedload(VariantaComercialaProdus.produs_generic), joinedload(VariantaComercialaProdus.producator)).all()

    if context == 'procedura':
        procedura = ProceduraAchizitie.query.options(selectinload(ProceduraAchizitie.loturi_procedura)
                                                    .selectinload(LotProcedura.articole_incluse)
                                                    .joinedload(ProdusInReferat.produs_generic_req)
                                                    .selectinload(Produs.variante_comerciale)).get_or_404(context_id)
        return render_template('adauga_oferta.html', furnizori=furnizori, today=date.today().isoformat(), variante_comerciale=variante_comerciale, procedura=procedura)

    elif context == 'referat':
        referat = ReferatNecesitate.query.options(selectinload(ReferatNecesitate.produse_in_referate)
                                                  .joinedload(ProdusInReferat.produs_generic_req)
                                                  .selectinload(Produs.variante_comerciale)).get_or_404(context_id)
        return render_template('adauga_oferta.html', furnizori=furnizori, referat=referat, today=date.today().isoformat(), variante_comerciale=variante_comerciale)
    else:
        return render_template('adauga_oferta.html', furnizori=furnizori, today=date.today().isoformat(), variante_comerciale=variante_comerciale)

@oferte_bp.route('/<int:oferta_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_oferta(oferta_id):
    """Gestionează editarea unei oferte existente."""
    oferta = Oferta.query.options(selectinload(Oferta.articole)).get_or_404(oferta_id)
    furnizori = Furnizor.query.order_by(Furnizor.Nume_Furnizor).all()
    variante_comerciale = VariantaComercialaProdus.query.options(joinedload(VariantaComercialaProdus.produs_generic), joinedload(VariantaComercialaProdus.producator)).all()

    if request.method == 'POST':
        oferta.ID_Furnizor = request.form.get('id_furnizor', type=int)
        oferta.Data_Oferta = date.fromisoformat(request.form.get('data_oferta'))
        oferta.Numar_Inregistrare = request.form.get('numar_inregistrare')
        oferta.Data_Inregistrare = date.fromisoformat(request.form.get('data_inregistrare')) if request.form.get('data_inregistrare') else None
        oferta.Moneda = request.form.get('moneda')

        # Articole
        articole_existente_map = {art.ID_Produs_Referat: art for art in oferta.articole}
        produse_ids = request.form.getlist('id_produs_referat[]')
        variante_ids = request.form.getlist('id_varianta_comerciala[]')
        preturi = request.form.getlist('pret_unitar_pachet[]')
        observatii_list = request.form.getlist('observatii[]')

        for i in range(len(produse_ids)):
            produs_id = int(produse_ids[i])
            if variante_ids[i] and preturi[i]:
                if produs_id in articole_existente_map:
                    articol = articole_existente_map[produs_id]
                    articol.ID_Varianta_Comerciala = int(variante_ids[i])
                    articol.Pret_Unitar_Pachet = float(preturi[i])
                    articol.Observatii = observatii_list[i]
                else:
                    new_articol = ArticolOferta(
                        ID_Oferta=oferta.ID_Oferta,
                        ID_Produs_Referat=produs_id,
                        ID_Varianta_Comerciala=int(variante_ids[i]),
                        Pret_Unitar_Pachet=float(preturi[i]),
                        Observatii=observatii_list[i]
                    )
                    db.session.add(new_articol)
            elif produs_id in articole_existente_map:
                db.session.delete(articole_existente_map[produs_id])

        db.session.commit()
        flash('Oferta a fost actualizată cu succes!', 'success')
        return redirect(url_for('oferte.detalii_oferta', oferta_id=oferta.ID_Oferta))

    # Context pentru editare: procedură, referat sau generic (niciunul)
    if oferta.ID_Procedura:
        procedura = ProceduraAchizitie.query.options(selectinload(ProceduraAchizitie.loturi_procedura)
                                                    .selectinload(LotProcedura.articole_incluse)
                                                    .joinedload(ProdusInReferat.produs_generic_req)
                                                    .selectinload(Produs.variante_comerciale)).get_or_404(oferta.ID_Procedura)
    elif oferta.ID_Referat:
        referat = ReferatNecesitate.query.options(selectinload(ReferatNecesitate.produse_in_referate)
                                                  .joinedload(ProdusInReferat.produs_generic_req)
                                                  .selectinload(Produs.variante_comerciale)).get_or_404(oferta.ID_Referat)

    articole_oferite_map = {art.ID_Produs_Referat: art for art in oferta.articole}
    
    return render_template('edit_oferta.html',
                           oferta=oferta,
                           furnizori=furnizori,
                           variante_comerciale=variante_comerciale,
                           articole_oferite_map=articole_oferite_map,
                           procedura=procedura if oferta.ID_Procedura else None,
                           referat=referat if oferta.ID_Referat else None)

@oferte_bp.route('/<int:oferta_id>/sterge', methods=['POST'])
@login_required
def sterge_oferta(oferta_id):
    """Șterge o ofertă și articolele asociate."""
    oferta = Oferta.query.get_or_404(oferta_id)
    
    if oferta.ID_Procedura:
        id_redirectionare = oferta.ID_Procedura
        endpoint_redirect = 'proceduri.detalii_procedura'
    elif oferta.ID_Referat:
        id_redirectionare = oferta.ID_Referat
        endpoint_redirect = 'referate.detalii_referat'
    else:
        id_redirectionare = None
        endpoint_redirect = 'oferte.list_oferte'
    
    db.session.delete(oferta)
    db.session.commit()
    flash(f'Oferta #{oferta_id} a fost ștearsă.', 'success')

    if id_redirectionare:
        return redirect(url_for(endpoint_redirect, **{'context_id': id_redirectionare} if endpoint_redirect != 'oferte.list_oferte' else {})) 
    else:
        return redirect(url_for(endpoint_redirect))
    

@oferte_bp.route('/<int:oferta_id>/detalii')
@login_required
def detalii_oferta(oferta_id):
    """Afișează detaliile complete ale unei oferte."""
    oferta = Oferta.query.options(
        joinedload(Oferta.furnizor),
        selectinload(Oferta.articole)
            .joinedload(ArticolOferta.varianta_comerciala_ofertata)
            .joinedload(VariantaComercialaProdus.produs_generic),
        selectinload(Oferta.articole)
            .joinedload(ArticolOferta.varianta_comerciala_ofertata)
            .joinedload(VariantaComercialaProdus.producator),
        joinedload(Oferta.procedura_parinte),
        joinedload(Oferta.referat_asociat)
    ).get_or_404(oferta_id)
    
    return render_template('detalii_oferta.html', oferta=oferta)
