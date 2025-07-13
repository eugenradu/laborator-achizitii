from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from models import (db, Contract, ArticolContractat, Oferta, LotProcedura, ProceduraAchizitie, ArticolOferta, 
                    ProdusInReferat, Produs, VariantaComercialaProdus, TipContract, Utilizator, Furnizor, ComandaGeneral, DetaliiComandaProdus)

contracte_bp = Blueprint('contracte', __name__, url_prefix='/contracte')

@contracte_bp.route('/')
@login_required
def list_contracte():
    """Afișează lista tuturor contractelor, cu căutare și paginare."""
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 15

    # Interogare de bază
    query = db.session.query(Contract, Utilizator, Furnizor)\
        .join(Furnizor, Contract.ID_Furnizor == Furnizor.ID_Furnizor)\
        .outerjoin(Utilizator, Contract.ID_Utilizator_Creare == Utilizator.ID_Utilizator)

    if search_term:
        search_filter = or_(
            Contract.Numar_Contract.ilike(f'%{search_term}%'),
            Furnizor.Nume_Furnizor.ilike(f'%{search_term}%'),
            Utilizator.Nume_Utilizator.ilike(f'%{search_term}%')
        )
        query = query.filter(search_filter)

    pagination = query.order_by(Contract.Data_Semnare.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    
    return render_template('contracte.html', pagination=pagination, search_term=search_term)

@contracte_bp.route('/<int:contract_id>/detalii')
@login_required
def detalii_contract(contract_id):
    """Afișează detaliile unui contract."""
    contract = Contract.query.options(
        joinedload(Contract.furnizor),
        joinedload(Contract.procedura_contract),
        joinedload(Contract.loturi_procedura_contractate),
        joinedload(Contract.articole_contractate).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload(VariantaComercialaProdus.produs_generic),
        joinedload(Contract.articole_contractate).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload(VariantaComercialaProdus.producator),
        joinedload(Contract.comenzi_rel)
    ).get_or_404(contract_id)
    
    return render_template('detalii_contract.html', contract=contract)

@contracte_bp.route('/adauga', methods=['GET', 'POST'])
@login_required
def adauga_contract():
    """Creează un nou contract, pre-populat pe baza unei oferte câștigătoare pentru unul sau mai multe Super-Loturi."""
    
    # --- Logica POST (Salvarea formularului) ---
    if request.method == 'POST':
        # 1. Preluare date formular
        tip_contract_str = request.form.get('tip_contract')
        numar_contract = request.form.get('numar_contract')
        data_semnare_str = request.form.get('data_semnare')
        pret_total_contract = request.form.get('pret_total_contract', type=float)
        id_procedura = request.form.get('id_procedura', type=int)
        id_furnizor = request.form.get('id_furnizor', type=int)
        moneda = request.form.get('moneda', 'RON')
        
        lot_procedura_ids = request.form.getlist('loturi_procedura_incluse')
        articol_oferta_ids = request.form.getlist('id_articol_oferta')
        cantitati_contractate = request.form.getlist('cantitate_contractata')

        if not all([tip_contract_str, numar_contract, data_semnare_str, pret_total_contract is not None, 
                    id_procedura, id_furnizor, lot_procedura_ids]):
            flash('Eroare: Datele din formular sunt incomplete. Vă rugăm reîncercați.', 'danger')
            return redirect(url_for('proceduri.list_proceduri'))

        # 2. Creare antet Contract
        try:
            new_contract = Contract(
                Numar_Contract=numar_contract,
                Data_Semnare=date.fromisoformat(data_semnare_str),
                Tip_Contract=TipContract[tip_contract_str],
                Pret_Total_Contract=pret_total_contract,
                Moneda=moneda,
                ID_Procedura=id_procedura,
                ID_Furnizor=id_furnizor,
                ID_Utilizator_Creare=current_user.ID_Utilizator,
                Numar_Inregistrare_Document=request.form.get('numar_inregistrare'),
                Data_Inregistrare_Document=date.fromisoformat(request.form.get('data_inregistrare')) if request.form.get('data_inregistrare') else None,
                Link_Scan_PDF=request.form.get('link_scan_pdf')
            )

            # 3. Asociere Loturi de Procedură
            loturi_selectate = LotProcedura.query.filter(LotProcedura.ID_Lot_Procedura.in_(lot_procedura_ids)).all()
            new_contract.loturi_procedura_contractate.extend(loturi_selectate)

            # 4. Creare Articole Contractate
            articole_map = dict(zip(articol_oferta_ids, cantitati_contractate))
            for articol_id, cantitate_str in articole_map.items():
                cantitate = int(cantitate_str)
                if cantitate > 0:
                    articol_oferta = ArticolOferta.query.get(articol_id)
                    if articol_oferta:
                        new_articol_contractat = ArticolContractat(
                            ID_Produs_Referat=articol_oferta.ID_Produs_Referat,
                            ID_Varianta_Comerciala=articol_oferta.ID_Varianta_Comerciala,
                            Cantitate_Contractata_Pachete=cantitate,
                            Pret_Unitar_Pachet_Contract=articol_oferta.Pret_Unitar_Pachet
                        )
                        new_contract.articole_contractate.append(new_articol_contractat)
            
            db.session.add(new_contract)
            db.session.flush() # Obținem ID-urile pentru contract și articolele sale

            # 5. Generare automată comandă pentru Contract Ferm
            if new_contract.Tip_Contract == TipContract.CONTRACT_FERM:
                new_comanda = ComandaGeneral(
                    ID_Contract=new_contract.ID_Contract,
                    Numar_Comanda=f"CMD-AUT-{new_contract.Numar_Contract}",
                    Stare_Comanda="Generata Automat",
                    ID_Utilizator_Creare=current_user.ID_Utilizator
                )
                # Adăugăm articolele în comandă, copiind cantitățile din contract
                for articol_contractat in new_contract.articole_contractate:
                    detaliu_comanda = DetaliiComandaProdus(ID_Articol_Contractat=articol_contractat.ID_Articol_Contractat, Cantitate_Comandata_Pachete=articol_contractat.Cantitate_Contractata_Pachete)
                    new_comanda.detalii_produse_comanda_rel.append(detaliu_comanda)
                db.session.add(new_comanda)

            db.session.add(new_contract)
            db.session.commit()
            flash(f'Contractul #{new_contract.ID_Contract} a fost generat cu succes!', 'success')
            return redirect(url_for('contracte.detalii_contract', contract_id=new_contract.ID_Contract))

        except Exception as e:
            db.session.rollback()
            flash(f'A apărut o eroare la salvarea contractului: {str(e)}', 'danger')
            return redirect(url_for('proceduri.detalii_procedura', procedura_id=id_procedura))

    # --- Logica GET (Pregătirea formularului) ---
    oferta_id = request.args.get('oferta_id', type=int)
    lot_procedura_id_initial = request.args.get('lot_procedura_id', type=int)

    if not oferta_id or not lot_procedura_id_initial:
        flash('Lipsesc informațiile necesare pentru a genera un contract (ID Ofertă sau ID Lot Procedură).', 'danger')
        return redirect(url_for('proceduri.list_proceduri'))

    oferta = Oferta.query.options(joinedload(Oferta.furnizor)).get_or_404(oferta_id)
    lot_procedura_initial = LotProcedura.query.get_or_404(lot_procedura_id_initial)
    procedura = ProceduraAchizitie.query.get_or_404(oferta.ID_Procedura)

    # Preluăm articolele din oferta câștigătoare care corespund lotului inițial
    articole_in_lot_ids = {art.ID_Produs_Referat for art in lot_procedura_initial.articole_incluse}
    
    articole_oferta_relevante = db.session.query(ArticolOferta, ProdusInReferat, Produs, VariantaComercialaProdus)\
        .join(ProdusInReferat, ArticolOferta.ID_Produs_Referat == ProdusInReferat.ID_Produs_Referat)\
        .join(VariantaComercialaProdus, ArticolOferta.ID_Varianta_Comerciala == VariantaComercialaProdus.ID_Varianta_Comerciala)\
        .join(Produs, ProdusInReferat.ID_Produs_Generic == Produs.ID_Produs)\
        .filter(ArticolOferta.ID_Oferta == oferta_id)\
        .filter(ArticolOferta.ID_Produs_Referat.in_(articole_in_lot_ids))\
        .all()

    articole_de_contractat = []
    for ao, pir, prod, vc in articole_oferta_relevante:
        articole_de_contractat.append({
            'articol_oferta': ao,
            'produs_generic': prod,
            'varianta_comerciala': vc,
            'cantitate_solicitata': pir.Cantitate_Solicitata
        })

    # TODO: Logica pentru a găsi loturi suplimentare eligibile poate fi adăugată aici dacă se dorește.
    # Pentru moment, se va crea contract doar pentru lotul selectat.

    return render_template('adauga_contract.html', 
                           procedura=procedura, 
                           oferta=oferta, 
                           lot_initial=lot_procedura_initial,
                           articole_de_contractat=articole_de_contractat,
                           loturi_suplimentare_eligibile=[], # Lăsat gol momentan
                           today=date.today().isoformat(),
                           tipuri_contract=TipContract)
