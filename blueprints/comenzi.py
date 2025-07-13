from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from models import (db, Contract, ArticolContractat, ComandaGeneral, DetaliiComandaProdus, 
                    TipContract, VariantaComercialaProdus, Furnizor, Utilizator)

comenzi_bp = Blueprint('comenzi', __name__, url_prefix='/comenzi')

@comenzi_bp.route('/')
@login_required
def list_comenzi():
    """Afișează lista tuturor comenzilor, cu căutare și paginare."""
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 15

    # Interogare de bază
    query = db.session.query(ComandaGeneral, Contract, Furnizor)\
        .join(Contract, ComandaGeneral.ID_Contract == Contract.ID_Contract)\
        .join(Furnizor, Contract.ID_Furnizor == Furnizor.ID_Furnizor)

    if search_term:
        search_filter = or_(
            ComandaGeneral.Numar_Comanda.ilike(f'%{search_term}%'),
            ComandaGeneral.Stare_Comanda.ilike(f'%{search_term}%'),
            Contract.Numar_Contract.ilike(f'%{search_term}%'),
            Furnizor.Nume_Furnizor.ilike(f'%{search_term}%')
        )
        query = query.filter(search_filter)

    pagination = query.order_by(ComandaGeneral.Data_Comanda.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    
    return render_template('comenzi.html', pagination=pagination, search_term=search_term)

@comenzi_bp.route('/<int:comanda_id>/detalii')
@login_required
def detalii_comanda(comanda_id):
    """Afișează detaliile unei comenzi."""
    comanda = ComandaGeneral.query.options(
        joinedload(ComandaGeneral.contract_comanda).joinedload(Contract.furnizor),
        joinedload(ComandaGeneral.detalii_produse_comanda_rel).joinedload(DetaliiComandaProdus.articol_contractat_rel).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload(VariantaComercialaProdus.produs_generic),
        joinedload(ComandaGeneral.detalii_produse_comanda_rel).joinedload(DetaliiComandaProdus.articol_contractat_rel).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload(VariantaComercialaProdus.producator)
    ).get_or_404(comanda_id)
    
    return render_template('detalii_comanda.html', comanda=comanda)

@comenzi_bp.route('/adauga/<int:contract_id>', methods=['GET', 'POST'])
@login_required
def adauga_comanda(contract_id):
    """Creează o nouă comandă subsecventă în baza unui Acord-Cadru."""
    contract = Contract.query.options(
        joinedload(Contract.furnizor),
        joinedload(Contract.articole_contractate).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload('produs_generic'),
        joinedload(Contract.comenzi_rel).joinedload(ComandaGeneral.detalii_produse_comanda_rel)
    ).get_or_404(contract_id)

    if contract.Tip_Contract != TipContract.ACORD_CADRU:
        flash('Se pot plasa comenzi subsecvente doar pentru Acorduri-Cadru.', 'danger')
        return redirect(url_for('contracte.detalii_contract', contract_id=contract.ID_Contract))

    # Calculăm cantitățile deja comandate pentru fiecare articol
    cantitati_deja_comandate = {}
    for comanda in contract.comenzi_rel:
        for detaliu in comanda.detalii_produse_comanda_rel:
            articol_id = detaliu.ID_Articol_Contractat
            cantitati_deja_comandate[articol_id] = cantitati_deja_comandate.get(articol_id, 0) + detaliu.Cantitate_Comandata_Pachete

    # Pregătim datele pentru template, calculând cantitatea rămasă
    articole_disponibile = []
    for articol in contract.articole_contractate:
        comandat = cantitati_deja_comandate.get(articol.ID_Articol_Contractat, 0)
        ramas = articol.Cantitate_Contractata_Pachete - comandat
        if ramas > 0: # Afișăm doar articolele care mai pot fi comandate
            articole_disponibile.append({
                'articol_obj': articol,
                'cantitate_contractata': articol.Cantitate_Contractata_Pachete,
                'cantitate_comandata': comandat,
                'cantitate_ramasa': ramas
            })

    if request.method == 'POST':
        numar_comanda = request.form.get('numar_comanda')
        data_comanda_str = request.form.get('data_comanda')

        if not numar_comanda or not data_comanda_str:
            flash('Numărul și data comenzii sunt obligatorii.', 'danger')
            return redirect(url_for('comenzi.adauga_comanda', contract_id=contract_id))

        new_comanda = ComandaGeneral(
            ID_Contract=contract_id,
            Numar_Comanda=numar_comanda,
            Data_Comanda=date.fromisoformat(data_comanda_str),
            Stare_Comanda='Emisa',
            ID_Utilizator_Creare=current_user.ID_Utilizator
        )

        has_items = False
        for articol_info in articole_disponibile:
            articol_id = articol_info['articol_obj'].ID_Articol_Contractat
            cantitate_comandata_str = request.form.get(f'cantitate_{articol_id}')
            
            if cantitate_comandata_str and int(cantitate_comandata_str) > 0:
                cantitate_comandata = int(cantitate_comandata_str)
                if cantitate_comandata > articol_info['cantitate_ramasa']:
                    flash(f"Cantitatea comandată pentru {articol_info['articol_obj'].varianta_comerciala_contractata.produs_generic.Nume_Generic} depășește cantitatea rămasă în contract.", 'danger')
                    return render_template('adauga_comanda.html', contract=contract, articole_disponibile=articole_disponibile, today=date.today().isoformat())

                new_comanda.detalii_produse_comanda_rel.append(DetaliiComandaProdus(ID_Articol_Contractat=articol_id, Cantitate_Comandata_Pachete=cantitate_comandata))
                has_items = True
        
        if not has_items:
            flash('Comanda trebuie să conțină cel puțin un articol cu o cantitate mai mare ca zero.', 'warning')
            return redirect(url_for('comenzi.adauga_comanda', contract_id=contract_id))

        db.session.add(new_comanda)
        db.session.commit()
        flash(f'Comanda #{new_comanda.ID_Comanda_General} a fost creată cu succes.', 'success')
        return redirect(url_for('contracte.detalii_contract', contract_id=contract_id))

    return render_template('adauga_comanda.html', contract=contract, articole_disponibile=articole_disponibile, today=date.today().isoformat())