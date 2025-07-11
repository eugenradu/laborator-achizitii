from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# 1. Model pentru Utilizatori
class Utilizator(db.Model, UserMixin):
    __tablename__ = 'Utilizatori'
    ID_Utilizator = db.Column(db.Integer, primary_key=True)
    Nume_Utilizator = db.Column(db.Text, unique=True, nullable=False)
    Email = db.Column(db.Text, unique=True, nullable=False)
    Parola_Hash = db.Column(db.Text, nullable=False)
    Data_Creare = db.Column(db.Date, nullable=False, default=date.today)
    Este_Activ = db.Column(db.Boolean, nullable=False, default=True)

    # Relații inverse
    referate_create = db.relationship('ReferatNecesitate', backref='creator_referat', lazy=True)
    licitatii_create = db.relationship('Licitatie', backref='creator_licitatie', lazy=True)
    contracte_create = db.relationship('Contract', backref='creator_contract', lazy=True)
    comenzi_create = db.relationship('ComandaGeneral', backref='creator_comanda', lazy=True)
    livrari_inregistrate = db.relationship('LivrareComanda', backref='inregistrator_livrare', lazy=True)
    consumuri_inregistrate = db.relationship('ConsumStoc', backref='inregistrator_consum', lazy=True)
    
    def set_password(self, password):
        self.Parola_Hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Parola_Hash, password)

    def get_id(self):
        return str(self.ID_Utilizator)

    def is_active(self):
        return self.Este_Activ

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"<Utilizator {self.Nume_Utilizator}>"

# 2. Model pentru Categorii de Produse
class Categorie(db.Model):
    __tablename__ = 'Categorii'
    ID_Categorie = db.Column(db.Integer, primary_key=True)
    Nume_Categorie = db.Column(db.Text, unique=True, nullable=False)

    # Relație inversă pentru a accesa produsele dintr-o categorie
    produse = db.relationship('Produs', backref='categorie', lazy=True)

    def __repr__(self):
        return f"<Categorie {self.Nume_Categorie}>"

# 3. Model pentru Producători
class Producator(db.Model):
    __tablename__ = 'Producatori'
    ID_Producator = db.Column(db.Integer, primary_key=True)
    Nume_Producator = db.Column(db.Text, unique=True, nullable=False)
    variante_comerciale = db.relationship('VariantaComercialaProdus', backref='producator', lazy=True)

    def __repr__(self):
        return f"<Producator {self.Nume_Producator}>"

# Model nou pentru Furnizori/Distribuitori
class Furnizor(db.Model):
    __tablename__ = 'Furnizori'
    ID_Furnizor = db.Column(db.Integer, primary_key=True)
    Nume_Furnizor = db.Column(db.Text, unique=True, nullable=False)
    CUI = db.Column(db.Text, unique=True)
    Adresa = db.Column(db.Text)
    Persoana_Contact = db.Column(db.Text)
    Email_Contact = db.Column(db.Text)
    Telefon_Contact = db.Column(db.Text)

    # Relații inverse
    oferte = db.relationship('Oferta', backref='furnizor', lazy=True)
    contracte = db.relationship('Contract', backref='furnizor', lazy=True)

    def __repr__(self):
        return f"<Furnizor {self.Nume_Furnizor}>"

# 4. Model pentru Produse (Generic Products)
class Produs(db.Model):
    __tablename__ = 'Produse'
    ID_Produs = db.Column(db.Integer, primary_key=True)
    Nume_Generic = db.Column(db.Text, nullable=False)
    Specificatii_Tehnice = db.Column(db.Text)
    Unitate_Masura = db.Column(db.Text)
    ID_Categorie = db.Column(db.Integer, db.ForeignKey('Categorii.ID_Categorie'), nullable=False)

    # Relații
    variante_comerciale = db.relationship('VariantaComercialaProdus', backref='produs_generic', lazy=True)
    produse_in_referate = db.relationship('ProdusInReferat', backref='produs_generic_req', lazy=True)

    def __repr__(self):
        return f"<Produs {self.Nume_Generic}>"

# 5. Model pentru Variante_Comerciale_Produs (Commercial Product Variants / Catalog Items)
class VariantaComercialaProdus(db.Model):
    __tablename__ = 'Variante_Comerciale_Produs'
    ID_Varianta_Comerciala = db.Column(db.Integer, primary_key=True)
    ID_Produs_Generic = db.Column(db.Integer, db.ForeignKey('Produse.ID_Produs'), nullable=False)
    ID_Producator = db.Column(db.Integer, db.ForeignKey('Producatori.ID_Producator'), nullable=False)
    Cod_Catalog = db.Column(db.Text, unique=True, nullable=False)
    Nume_Comercial_Extins = db.Column(db.Text)
    Descriere_Ambalare = db.Column(db.Text, nullable=False)
    Cantitate_Standard_Ambalare = db.Column(db.Integer, nullable=False)

    # Relații
    articole_oferta = db.relationship('ArticolOferta', backref='varianta_comerciala_ofertata', lazy=True)
    articole_contractate = db.relationship('ArticolContractatInLot', backref='varianta_comerciala_contractata', lazy=True)
    loturi_stoc = db.relationship('LotStoc', backref='varianta_comerciala_stoc', lazy=True)

    def __repr__(self):
        return f"<VariantaComercialaProdus {self.Cod_Catalog}>"


# 6. Model pentru Referate_Necesitate
class ReferatNecesitate(db.Model):
    __tablename__ = 'Referate_Necesitate'
    ID_Referat = db.Column(db.Integer, primary_key=True)
    Data_Creare = db.Column(db.Date, nullable=False, default=date.today)
    Stare = db.Column(db.Text, nullable=False, default='Ciorna')
    Numar_Referat = db.Column(db.Text)
    Numar_Inregistrare_Document = db.Column(db.Text)
    Data_Inregistrare_Document = db.Column(db.Date)
    Link_Scan_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator')) # NULLABLE as per DATA_MODEL.md
    Observatii = db.Column(db.Text)

    # Relații
    loturi = db.relationship('Lot', backref='referat_parinte', lazy=True)
    produse_in_referate = db.relationship('ProdusInReferat', backref='referat_necesitate', lazy=True)
    oferte = db.relationship('Oferta', backref='referat_asociat', lazy=True)

    def __repr__(self):
        return f"<ReferatNecesitate {self.Numar_Referat or self.ID_Referat}>"

# 7. Model pentru Loturi (Lots for Tenders)
class Lot(db.Model):
    __tablename__ = 'Loturi'
    ID_Lot = db.Column(db.Integer, primary_key=True)
    ID_Referat = db.Column(db.Integer, db.ForeignKey('Referate_Necesitate.ID_Referat'), nullable=False)
    Nume_Lot = db.Column(db.Text, nullable=False)
    Descriere_Lot = db.Column(db.Text)

    # Relații
    produse_in_loturi = db.relationship('ProdusInLot', backref='lot_parinte', lazy=True)
    contracte = db.relationship('Contract', backref='lot_contract', lazy=True)

    def __repr__(self):
        return f"<Lot {self.Nume_Lot}>"

# 8. Model pentru Produse_In_Referate (Products in Necessity Requests)
class ProdusInReferat(db.Model):
    __tablename__ = 'Produse_In_Referate'
    ID_Produs_Referat = db.Column(db.Integer, primary_key=True)
    ID_Referat = db.Column(db.Integer, db.ForeignKey('Referate_Necesitate.ID_Referat'), nullable=False)
    ID_Produs_Generic = db.Column(db.Integer, db.ForeignKey('Produse.ID_Produs'), nullable=False)
    Cantitate_Solicitata = db.Column(db.Integer, nullable=False)

    # Relații
    produse_in_loturi = db.relationship('ProdusInLot', backref='produs_referat_alloc', lazy=True)
    articole_oferta = db.relationship('ArticolOferta', backref='produs_referat_ofertat', lazy=True)
    articole_contractate = db.relationship('ArticolContractatInLot', backref='produs_referat_contractat', lazy=True)

    def __repr__(self):
        return f"<ProdusInReferat {self.ID_Produs_Referat} (Ref: {self.ID_Referat})>"

# 9. Model pentru Produse_In_Loturi (Products in Lots)
class ProdusInLot(db.Model):
    __tablename__ = 'Produse_In_Loturi'
    ID_Produs_Lot = db.Column(db.Integer, primary_key=True)
    ID_Lot = db.Column(db.Integer, db.ForeignKey('Loturi.ID_Lot'), nullable=False)
    ID_Produs_Referat = db.Column(db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), nullable=False)
    
    # Adaugăm o constrângere UNIQUE pentru a asigura că un ProdusInReferat este într-un singur ProdusInLot per Lot
    __table_args__ = (db.UniqueConstraint('ID_Lot', 'ID_Produs_Referat', name='_lot_produs_referat_uc'),)

    def __repr__(self):
        return f"<ProdusInLot {self.ID_Produs_Lot} (Lot: {self.ID_Lot}, ProdRef: {self.ID_Produs_Referat})>"

# Tabela de legătură pentru many-to-many între Licitatii și Loturi
# O Licitatie poate include mai multe Loturi, iar un Lot poate fi inclus în mai multe Licitatii
licitatii_loturi_asociere = db.Table(
    'licitatii_loturi_asociere',
    db.Column('licitatie_id', db.Integer, db.ForeignKey('Licitatii.ID_Licitatie'), primary_key=True),
    db.Column('lot_id', db.Integer, db.ForeignKey('Loturi.ID_Lot'), primary_key=True)
)

# 11. Model pentru Licitatii
class Licitatie(db.Model):
    __tablename__ = 'Licitatii'
    ID_Licitatie = db.Column(db.Integer, primary_key=True)
    Data_Creare = db.Column(db.Date, nullable=False, default=date.today)
    Nume_Licitatie = db.Column(db.Text, nullable=False)
    Stare = db.Column(db.Text, nullable=False, default='In Desfasurare')
    Numar_Inregistrare_Caiet_Sarcini = db.Column(db.Text)
    Data_Inregistrare_Caiet_Sarcini = db.Column(db.Date)
    Link_Scan_Caiet_Sarcini_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relații Many-to-Many cu Loturi
    loturi_incluse = db.relationship(
        'Lot',
        secondary=licitatii_loturi_asociere,
        backref=db.backref('licitatii_asociate', lazy='dynamic'), # backref='licitatii_asociate' in Lot model
        lazy='dynamic'
    )
    oferte = db.relationship('Oferta', backref='licitatie_parinte', lazy=True)
    contracte_rel = db.relationship('Contract', backref='licitatie_contract', lazy=True)

    def __repr__(self):
        return f"<Licitatie {self.Nume_Licitatie}>"

# 12. Model nou pentru Oferte (Antet)
class Oferta(db.Model):
    __tablename__ = 'Oferte'
    ID_Oferta = db.Column(db.Integer, primary_key=True)
    ID_Furnizor = db.Column(db.Integer, db.ForeignKey('Furnizori.ID_Furnizor'), nullable=False)
    Data_Oferta = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Inregistrare = db.Column(db.Text)
    Data_Inregistrare = db.Column(db.Date)
    Moneda = db.Column(db.Text, nullable=False, default='RON')
    
    # Legături opționale către alte module
    ID_Licitatie = db.Column(db.Integer, db.ForeignKey('Licitatii.ID_Licitatie'), nullable=True)
    ID_Referat = db.Column(db.Integer, db.ForeignKey('Referate_Necesitate.ID_Referat'), nullable=True)
    
    # Relație către articolele din ofertă
    articole = db.relationship('ArticolOferta', backref='oferta_parinte', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Oferta {self.ID_Oferta} de la {self.furnizor.Nume_Furnizor if self.furnizor else 'N/A'}>"

# Model nou pentru Articolele dintr-o Ofertă (Linii)
class ArticolOferta(db.Model):
    __tablename__ = 'Articole_Oferta'
    ID_Articol_Oferta = db.Column(db.Integer, primary_key=True)
    ID_Oferta = db.Column(db.Integer, db.ForeignKey('Oferte.ID_Oferta'), nullable=False)
    ID_Varianta_Comerciala = db.Column(db.Integer, db.ForeignKey('Variante_Comerciale_Produs.ID_Varianta_Comerciala'), nullable=False)
    ID_Produs_Referat = db.Column(db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), nullable=True)
    Pret_Unitar_Pachet = db.Column(db.Float, nullable=False)
    Observatii = db.Column(db.Text)

    def __repr__(self):
        return f"<ArticolOferta {self.ID_Articol_Oferta} (Oferta: {self.ID_Oferta})>"


# 13. Model pentru Contracte
class Contract(db.Model):
    __tablename__ = 'Contracte'
    ID_Contract = db.Column(db.Integer, primary_key=True)
    ID_Licitatie = db.Column(db.Integer, db.ForeignKey('Licitatii.ID_Licitatie'), nullable=False)
    ID_Lot = db.Column(db.Integer, db.ForeignKey('Loturi.ID_Lot'), nullable=False)
    ID_Furnizor = db.Column(db.Integer, db.ForeignKey('Furnizori.ID_Furnizor'), nullable=False)
    Pret_Total_Contract = db.Column(db.Float, nullable=False)
    Data_Semnare = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Contract = db.Column(db.Text, nullable=False)
    Numar_Inregistrare_Document = db.Column(db.Text)
    Data_Inregistrare_Document = db.Column(db.Date)
    Link_Scan_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relații
    articole_contractate_rel = db.relationship('ArticolContractatInLot', backref='contract_parinte', lazy=True)
    comenzi_rel = db.relationship('ComandaGeneral', backref='contract_comanda', lazy=True)

    def __repr__(self):
        return f"<Contract {self.Numar_Contract}>"

# 14. Model pentru Articole_Contractate_In_Lot
class ArticolContractatInLot(db.Model):
    __tablename__ = 'Articole_Contractate_In_Lot'
    ID_Articol_Contractat = db.Column(db.Integer, primary_key=True)
    ID_Contract = db.Column(db.Integer, db.ForeignKey('Contracte.ID_Contract'), nullable=False)
    ID_Produs_Referat = db.Column(db.Integer, db.ForeignKey('Produse_In_Referate.ID_Produs_Referat'), nullable=False)
    ID_Varianta_Comerciala = db.Column(db.Integer, db.ForeignKey('Variante_Comerciale_Produs.ID_Varianta_Comerciala'), nullable=False)
    Cantitate_Contractata_Pachete = db.Column(db.Integer, nullable=False)
    Pret_Unitar_Pachet_Contract = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<ArticolContractat {self.ID_Articol_Contractat}>"

# 15. Model pentru Comanda_General
class ComandaGeneral(db.Model):
    __tablename__ = 'Comanda_General'
    ID_Comanda_General = db.Column(db.Integer, primary_key=True)
    ID_Contract = db.Column(db.Integer, db.ForeignKey('Contracte.ID_Contract'), nullable=False)
    Data_Comanda = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Comanda = db.Column(db.Text)
    Stare_Comanda = db.Column(db.Text, nullable=False, default='Emisa')
    Numar_Inregistrare_Document = db.Column(db.Text)
    Data_Inregistrare_Document = db.Column(db.Date)
    Link_Scan_PDF = db.Column(db.Text)
    ID_Utilizator_Creare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relații
    detalii_produse_comanda_rel = db.relationship('DetaliiComandaProdus', backref='comanda_parinte', lazy=True)

    def __repr__(self):
        return f"<ComandaGeneral {self.Numar_Comanda or self.ID_Comanda_General}>"

# 16. Model pentru Detalii_Comanda_Produs
class DetaliiComandaProdus(db.Model):
    __tablename__ = 'Detalii_Comanda_Produs'
    ID_Detalii_Comanda_Produs = db.Column(db.Integer, primary_key=True)
    ID_Comanda_General = db.Column(db.Integer, db.ForeignKey('Comanda_General.ID_Comanda_General'), nullable=False)
    ID_Articol_Contractat = db.Column(db.Integer, db.ForeignKey('Articole_Contractate_In_Lot.ID_Articol_Contractat'), nullable=False)
    Cantitate_Comandata_Pachete = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<DetaliiComandaProdus {self.ID_Detalii_Comanda_Produs}>"

# 17. Model pentru Livrare_Comenzi
class LivrareComanda(db.Model):
    __tablename__ = 'Livrare_Comenzi'
    ID_Livrare = db.Column(db.Integer, primary_key=True)
    ID_Detalii_Comanda_Produs = db.Column(db.Integer, db.ForeignKey('Detalii_Comanda_Produs.ID_Detalii_Comanda_Produs'), nullable=False)
    Cantitate_Livrata_Pachete = db.Column(db.Integer, nullable=False)
    Data_Livrare = db.Column(db.Date, nullable=False, default=date.today)
    Numar_Factura = db.Column(db.Text)
    Link_Scan_Factura_PDF = db.Column(db.Text)
    Numar_Aviz_Livrare = db.Column(db.Text)
    Link_Scan_Aviz_Livrare_PDF = db.Column(db.Text)
    ID_Utilizator_Inregistrare = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))

    # Relații
    loturi_stoc_rel = db.relationship('LotStoc', backref='livrare_sursa', lazy=True)

    def __repr__(self):
        return f"<LivrareComanda {self.ID_Livrare}>"

# 18. Model pentru Locatii_Depozitare
class LocatieDepozitare(db.Model):
    __tablename__ = 'Locatii_Depozitare'
    ID_Locatie = db.Column(db.Integer, primary_key=True)
    Nume_Locatie = db.Column(db.Text, unique=True, nullable=False)
    Tip_Locatie = db.Column(db.Text, nullable=False)
    Descriere = db.Column(db.Text)

    # Relații
    loturi_stoc_rel = db.relationship('LotStoc', backref='locatie_stoc', lazy=True)

    def __repr__(self):
        return f"<LocatieDepozitare {self.Nume_Locatie}>"

# 19. Model pentru Loturi_Stoc
class LotStoc(db.Model):
    __tablename__ = 'Loturi_Stoc'
    ID_Lot_Stoc = db.Column(db.Integer, primary_key=True)
    ID_Varianta_Comerciala = db.Column(db.Integer, db.ForeignKey('Variante_Comerciale_Produs.ID_Varianta_Comerciala'), nullable=False)
    ID_Livrare = db.Column(db.Integer, db.ForeignKey('Livrare_Comenzi.ID_Livrare'))
    Cantitate_Initiala_Stoc_Pachete = db.Column(db.Integer, nullable=False)
    Cantitate_Curenta_Stoc_Pachete = db.Column(db.Integer, nullable=False)
    Data_Intrare_Stoc = db.Column(db.Date, nullable=False, default=date.today)
    Data_Expirare = db.Column(db.Date)
    ID_Locatie_Depozitare = db.Column(db.Integer, db.ForeignKey('Locatii_Depozitare.ID_Locatie'), nullable=False)
    Detalii_Ambalare_Intrare = db.Column(db.Text)
    Numar_Lot_Producator = db.Column(db.Text)
    Nivel_Alerta_Stoc = db.Column(db.Integer)

    # Relații
    consumuri_rel = db.relationship('ConsumStoc', backref='lot_stoc_consum', lazy=True)

    def __repr__(self):
        return f"<LotStoc {self.ID_Lot_Stoc}>"

# 20. Model pentru Consum_Stoc
class ConsumStoc(db.Model):
    __tablename__ = 'Consum_Stoc'
    ID_Consum = db.Column(db.Integer, primary_key=True)
    ID_Lot_Stoc = db.Column(db.Integer, db.ForeignKey('Loturi_Stoc.ID_Lot_Stoc'), nullable=False)
    Cantitate_Consumata_Pachete = db.Column(db.Integer, nullable=False)
    Data_Consum = db.Column(db.Date, nullable=False, default=date.today)
    Utilizator_Consum = db.Column(db.Integer, db.ForeignKey('Utilizatori.ID_Utilizator'))
    Scop_Consum = db.Column(db.Text)

    def __repr__(self):
        return f"<ConsumStoc {self.ID_Consum}>"