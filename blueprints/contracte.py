from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy.orm import joinedload
from models import (db, Contract, ArticolContractat, Oferta, Lot, ProceduraAchizitie, 
                    ArticolOferta, ProdusInReferat, Produs, VariantaComercialaProdus, TipContract,
                    proceduri_loturi_asociere, ComandaGeneral, DetaliiComandaProdus)

contracte_bp = Blueprint('contracte', __name__, url_prefix='/contracte')

@contracte_bp.route('/')
@login_required
def list_contracte():
    """Afișează lista tuturor contractelor."""
    contracte_list = Contract.query.options(
        joinedload(Contract.furnizor),
        joinedload(Contract.procedura_contract)
    ).order_by(Contract.Data_Semnare.desc()).all()
    
    return render_template('contracte.html', contracte=contracte_list)

@contracte_bp.route('/<int:contract_id>/detalii')
@login_required
def detalii_contract(contract_id):
    """Afișează detaliile unui contract."""
    contract = Contract.query.options(
        joinedload(Contract.furnizor),
        joinedload(Contract.procedura_contract),
        joinedload(Contract.creator_contract),
        joinedload(Contract.loturi_contractate),
        joinedload(Contract.articole_contractate).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload(VariantaComercialaProdus.produs_generic),
        joinedload(Contract.articole_contractate).joinedload(ArticolContractat.varianta_comerciala_contractata).joinedload(VariantaComercialaProdus.producator),
        joinedload(Contract.comenzi_rel)
    ).get_or_404(contract_id)
    
    return render_template('detalii_contract.html', contract=contract)

@contracte_bp.route('/adauga', methods=['GET', 'POST'])
@login_required
def adauga_contract():
    """Creează un nou contract consolidat, pre-populat pe baza unei oferte câștigătoare."""
    
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
        
        lot_ids = request.form.getlist('loturi_incluse')
        articol_oferta_ids = request.form.getlist('id_articol_oferta')
        cantitati_contractate = request.form.getlist('cantitate_contractata')

        if not all([tip_contract_str, numar_contract, data_semnare_str, pret_total_contract is not None, 
                    id_procedura, id_furnizor, lot_ids]):
            flash('Eroare: Datele din formular sunt incomplete. Vă rugăm reîncercați.', 'danger')
            return redirect(url_for('proceduri.list_proceduri'))

        # 2. Creare antet Contract
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

        # 3. Asociere Loturi
        loturi_selectate = Lot.query.filter(Lot.ID_Lot.in_(lot_ids)).all()
        new_contract.loturi_contractate.extend(loturi_selectate)

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
        db.session.flush() # Facem flush pentru a obține ID-urile pentru contract și articolele sale

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
                detaliu_comanda = DetaliiComandaProdus(
                    ID_Articol_Contractat=articol_contractat.ID_Articol_Contractat,
                    Cantitate_Comandata_Pachete=articol_contractat.Cantitate_Contractata_Pachete
                )
                new_comanda.detalii_produse_comanda_rel.append(detaliu_comanda)
            
            db.session.add(new_comanda)
            flash(f'Contractul ferm #{new_contract.ID_Contract} și comanda asociată au fost generate cu succes!', 'success')
        else:
            flash(f'Acordul-cadru #{new_contract.ID_Contract} a fost generat cu succes!', 'success')

        db.session.commit() # Commit final pentru contract și eventuala comandă
        return redirect(url_for('contracte.detalii_contract', contract_id=new_contract.ID_Contract))

    # --- Logica GET (Pregătirea formularului) ---
    oferta_id = request.args.get('oferta_id', type=int)
    lot_id_initial = request.args.get('lot_id', type=int)

    if not oferta_id or not lot_id_initial:
        flash('Lipsesc informațiile necesare pentru a genera un contract (ID Ofertă sau ID Lot).', 'danger')
        return redirect(url_for('proceduri.list_proceduri'))

    oferta = Oferta.query.options(joinedload(Oferta.furnizor)).get_or_404(oferta_id)
    lot_initial = Lot.query.get_or_404(lot_id_initial)
    procedura = ProceduraAchizitie.query.get_or_404(oferta.ID_Procedura)

    # Preluăm toate produsele solicitate în întreaga procedură
    produse_in_procedura_sq = db.session.query(ProdusInReferat.ID_Produs_Referat)\
        .join(ProdusInLot).join(Lot).join(proceduri_loturi_asociere)\
        .filter(proceduri_loturi_asociere.c.procedura_id == procedura.ID_Procedura).subquery()

    # Preluăm toate articolele din oferta selectată care corespund produselor din procedură
    articole_oferta_relevante = db.session.query(ArticolOferta, ProdusInReferat, Produs, VariantaComercialaProdus)\
        .join(ProdusInReferat, ArticolOferta.ID_Produs_Referat == ProdusInReferat.ID_Produs_Referat)\
        .join(VariantaComercialaProdus, ArticolOferta.ID_Varianta_Comerciala == VariantaComercialaProdus.ID_Varianta_Comerciala)\
        .join(Produs, ProdusInReferat.ID_Produs_Generic == Produs.ID_Produs)\
        .filter(ArticolOferta.ID_Oferta == oferta_id)\
        .filter(ArticolOferta.ID_Produs_Referat.in_(produse_in_procedura_sq))\
        .all()

    articole_de_contractat = []
    for ao, pir, prod, vc in articole_oferta_relevante:
        articole_de_contractat.append({
            'articol_oferta': ao,
            'produs_generic': prod,
            'varianta_comerciala': vc,
            'cantitate_solicitata': pir.Cantitate_Solicitata
        })

    # Găsim loturile suplimentare eligibile (acoperite de aceeași ofertă)
    loturi_acoperite_ids = {art.produs_referat_ofertat.lot_parinte.ID_Lot for art in oferta.articole if art.produs_referat_ofertat and art.produs_referat_ofertat.lot_parinte}
    loturi_suplimentare_eligibile = Lot.query.filter(
        Lot.ID_Lot.in_(loturi_acoperite_ids),
        Lot.ID_Lot != lot_id_initial
    ).all()

    return render_template('adauga_contract.html', 
                           procedura=procedura, 
                           oferta=oferta, 
                           lot_initial=lot_initial,
                           articole_de_contractat=articole_de_contractat,
                           loturi_suplimentare_eligibile=loturi_suplimentare_eligibile,
                           today=date.today().isoformat(),
                           tipuri_contract=TipContract)