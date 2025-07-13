from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import (db, Produs, VariantaComercialaProdus, Producator, Furnizor,
                    LivrareComanda, DocumentLivrare, DetaliiComandaProdus, ArticolContractat)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/produse_by_categorie/<int:categorie_id>')
@login_required
def get_produse_by_categorie(categorie_id):
    """Returnează o listă de produse (JSON) filtrate după o anumită categorie."""
    produse = Produs.query.filter_by(ID_Categorie=categorie_id).order_by(Produs.Nume_Generic).all()
    
    produse_list = [
        {'id': produs.ID_Produs, 'nume': produs.Nume_Generic, 'unitate_masura': produs.Unitate_Masura}
        for produs in produse
    ]
    
    return jsonify(produse_list)

@api_bp.route('/variante_comerciale/adauga', methods=['POST'])
@login_required
def api_adauga_varianta_comerciala():
    """Endpoint API pentru a adăuga o nouă variantă comercială dinamic."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Date JSON invalide'}), 400

    # Validare câmpuri obligatorii (verificăm și că nu sunt goale)
    required_fields = ['id_produs_generic', 'id_producator', 'cod_catalog', 'descriere_ambalare', 'cantitate_standard_ambalare']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Lipsesc câmpuri obligatorii.'}), 400

    # Verificăm unicitatea codului de catalog
    cod_catalog_curatat = data['cod_catalog'].strip()
    if VariantaComercialaProdus.query.filter_by(Cod_Catalog=cod_catalog_curatat).first():
        return jsonify({'error': f'Codul de catalog "{cod_catalog_curatat}" există deja.'}), 409 # Conflict

    try:
        new_variant = VariantaComercialaProdus(
            ID_Produs_Generic=int(data['id_produs_generic']),
            ID_Producator=int(data['id_producator']),
            Cod_Catalog=cod_catalog_curatat,
            Descriere_Ambalare=data['descriere_ambalare'].strip(),
            Cantitate_Standard_Ambalare=int(data['cantitate_standard_ambalare']),
            Nume_Comercial_Extins=data.get('nume_comercial_extins', '').strip() or None
        )
        db.session.add(new_variant)
        db.session.commit()

        producator = Producator.query.get(new_variant.ID_Producator)
        produs_generic = Produs.query.get(new_variant.ID_Produs_Generic)
        text_pentru_option = f"{producator.Nume_Producator} - {produs_generic.Nume_Generic} - {new_variant.Descriere_Ambalare} (Cod: {new_variant.Cod_Catalog})"
        return jsonify({'id': new_variant.ID_Varianta_Comerciala, 'text': text_pentru_option}), 201 # Created
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Eroare la salvarea în baza de date: {str(e)}'}), 500

@api_bp.route('/furnizori/adauga', methods=['POST'])
@login_required
def api_adauga_furnizor():
    """Endpoint API pentru a adăuga un nou furnizor dinamic."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Date JSON invalide'}), 400

    nume_furnizor = data.get('nume_furnizor', '').strip()
    if not nume_furnizor:
        return jsonify({'error': 'Numele furnizorului este obligatoriu.'}), 400

    new_furnizor = Furnizor(
        Nume_Furnizor=nume_furnizor,
        CUI=data.get('cui', '').strip() or None,
        Adresa=data.get('adresa', '').strip() or None
    )
    db.session.add(new_furnizor)
    try:
        db.session.commit()
        return jsonify({'id': new_furnizor.ID_Furnizor, 'text': new_furnizor.Nume_Furnizor}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Un furnizor cu acest nume sau CUI există deja.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Eroare la salvarea în baza de date: {str(e)}'}), 500

@api_bp.route('/producatori/adauga', methods=['POST'])
@login_required
def api_adauga_producator():
    """Endpoint API pentru a adăuga un nou producător dinamic."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Date JSON invalide'}), 400

    nume_producator = data.get('nume_producator', '').strip()
    if not nume_producator:
        return jsonify({'error': 'Numele producătorului este obligatoriu.'}), 400

    try:
        # Verificăm unicitatea
        if Producator.query.filter_by(Nume_Producator=nume_producator).first():
            return jsonify({'error': f'Producătorul "{nume_producator}" există deja.'}), 409 # Conflict

        new_producator = Producator(Nume_Producator=nume_producator)
        db.session.add(new_producator)
        db.session.commit()
        return jsonify({'id': new_producator.ID_Producator, 'text': new_producator.Nume_Producator}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Eroare la salvarea în baza de date: {str(e)}'}), 500

@api_bp.route('/variante_by_produs/<int:produs_id>')
@login_required
def get_variante_by_produs(produs_id):
    """Returnează o listă de variante comerciale (JSON) filtrate după un produs generic."""
    variante = db.session.query(VariantaComercialaProdus, Producator)\
        .join(Producator)\
        .filter(VariantaComercialaProdus.ID_Produs_Generic == produs_id)\
        .order_by(Producator.Nume_Producator, VariantaComercialaProdus.Cod_Catalog).all()
    
    variante_list = []
    for varianta, producator in variante:
        text_option = f"{producator.Nume_Producator} - {varianta.Descriere_Ambalare} (Cod: {varianta.Cod_Catalog})"
        variante_list.append({'id': varianta.ID_Varianta_Comerciala, 'text': text_option})
    
    return jsonify(variante_list)

@api_bp.route('/livrari/<int:livrare_id>')
@login_required
def get_livrare_details(livrare_id):
    """Returnează detaliile complete ale unei livrări în format JSON."""
    livrare = LivrareComanda.query.options(
        joinedload(LivrareComanda.detalii_comanda_rel)
            .joinedload(DetaliiComandaProdus.articol_contractat_rel)
            .joinedload(ArticolContractat.varianta_comerciala_contractata)
            .joinedload(VariantaComercialaProdus.produs_generic),
        joinedload(LivrareComanda.detalii_comanda_rel)
            .joinedload(DetaliiComandaProdus.articol_contractat_rel)
            .joinedload(ArticolContractat.varianta_comerciala_contractata)
            .joinedload(VariantaComercialaProdus.producator),
        joinedload(LivrareComanda.documente_asociate)
    ).get_or_404(livrare_id)

    # Extragem datele necesare
    detaliu_comanda = livrare.detalii_comanda_rel
    articol_contractat = detaliu_comanda.articol_contractat_rel
    varianta_comerciala = articol_contractat.varianta_comerciala_contractata
    produs_generic = varianta_comerciala.produs_generic

    # Construim lista de documente
    documente_list = [
        {
            'tip_document': doc.Tip_Document.value,
            'numar_document': doc.Numar_Document,
            'data_document': doc.Data_Document.isoformat() if doc.Data_Document else None,
            'link_scan_pdf': doc.Link_Scan_PDF
        } for doc in livrare.documente_asociate
    ]

    # Construim răspunsul JSON
    response_data = {
        'id_livrare': livrare.ID_Livrare,
        'data_livrare': livrare.Data_Livrare.isoformat(),
        'cantitate_livrata': livrare.Cantitate_Livrata_Pachete,
        'lot_producator': livrare.Numar_Lot_Producator,
        'data_expirare': livrare.Data_Expirare.isoformat() if livrare.Data_Expirare else None,
        'sursa_intrare': f"Livrare #{livrare.ID_Livrare} / Comanda #{detaliu_comanda.ID_Comanda_General}",
        'produs': {
            'id_varianta_comerciala': varianta_comerciala.ID_Varianta_Comerciala,
            'cod_catalog': varianta_comerciala.Cod_Catalog,
            'nume_produs_generic': produs_generic.Nume_Generic,
            'descriere_ambalare': varianta_comerciala.Descriere_Ambalare,
            'producator': varianta_comerciala.producator.Nume_Producator
        },
        'documente': documente_list
    }

    return jsonify(response_data)