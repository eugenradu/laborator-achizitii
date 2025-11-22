--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: starereferat; Type: TYPE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TYPE public.starereferat AS ENUM (
    'CIORNA',
    'IN_APROBARE',
    'APROBAT'
);


ALTER TYPE public.starereferat OWNER TO nume_utilizator_pg;

--
-- Name: tipcontract; Type: TYPE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TYPE public.tipcontract AS ENUM (
    'CONTRACT_FERM',
    'ACORD_CADRU'
);


ALTER TYPE public.tipcontract OWNER TO nume_utilizator_pg;

--
-- Name: tipdocument; Type: TYPE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TYPE public.tipdocument AS ENUM (
    'FACTURA',
    'AVIZ_EXPEDITIE',
    'CERTIFICAT_CALITATE',
    'ALTUL'
);


ALTER TYPE public.tipdocument OWNER TO nume_utilizator_pg;

--
-- Name: tipprocedura; Type: TYPE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TYPE public.tipprocedura AS ENUM (
    'LICITATIE_DESCHISA',
    'PROCEDURA_SIMPLIFICATA',
    'ACHIZITIE_DIRECTA',
    'NEGOCIERE_COMPETITIVA',
    'ALTELE'
);


ALTER TYPE public.tipprocedura OWNER TO nume_utilizator_pg;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Articole_Contractate; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Articole_Contractate" (
    "ID_Articol_Contractat" integer NOT NULL,
    "ID_Contract" integer NOT NULL,
    "ID_Produs_Referat" integer NOT NULL,
    "ID_Varianta_Comerciala" integer NOT NULL,
    "Cantitate_Contractata_Pachete" integer NOT NULL,
    "Pret_Unitar_Pachet_Contract" double precision NOT NULL
);


ALTER TABLE public."Articole_Contractate" OWNER TO nume_utilizator_pg;

--
-- Name: Articole_Contractate_ID_Articol_Contractat_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Articole_Contractate_ID_Articol_Contractat_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Articole_Contractate_ID_Articol_Contractat_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Articole_Contractate_ID_Articol_Contractat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Articole_Contractate_ID_Articol_Contractat_seq" OWNED BY public."Articole_Contractate"."ID_Articol_Contractat";


--
-- Name: Articole_Oferta; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Articole_Oferta" (
    "ID_Articol_Oferta" integer NOT NULL,
    "ID_Oferta" integer NOT NULL,
    "ID_Varianta_Comerciala" integer NOT NULL,
    "ID_Produs_Referat" integer,
    "Pret_Unitar_Pachet" double precision NOT NULL,
    "ID_Lot_Procedura" integer,
    "Observatii" text
);


ALTER TABLE public."Articole_Oferta" OWNER TO nume_utilizator_pg;

--
-- Name: Articole_Oferta_ID_Articol_Oferta_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Articole_Oferta_ID_Articol_Oferta_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Articole_Oferta_ID_Articol_Oferta_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Articole_Oferta_ID_Articol_Oferta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Articole_Oferta_ID_Articol_Oferta_seq" OWNED BY public."Articole_Oferta"."ID_Articol_Oferta";


--
-- Name: Categorii; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Categorii" (
    "ID_Categorie" integer NOT NULL,
    "Nume_Categorie" text NOT NULL
);


ALTER TABLE public."Categorii" OWNER TO nume_utilizator_pg;

--
-- Name: Categorii_ID_Categorie_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Categorii_ID_Categorie_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Categorii_ID_Categorie_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Categorii_ID_Categorie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Categorii_ID_Categorie_seq" OWNED BY public."Categorii"."ID_Categorie";


--
-- Name: Comanda_General; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Comanda_General" (
    "ID_Comanda_General" integer NOT NULL,
    "ID_Contract" integer NOT NULL,
    "Data_Comanda" date NOT NULL,
    "Numar_Comanda" text,
    "Stare_Comanda" text NOT NULL,
    "Numar_Inregistrare_Document" text,
    "Data_Inregistrare_Document" date,
    "Link_Scan_PDF" text,
    "ID_Utilizator_Creare" integer
);


ALTER TABLE public."Comanda_General" OWNER TO nume_utilizator_pg;

--
-- Name: Comanda_General_ID_Comanda_General_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Comanda_General_ID_Comanda_General_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Comanda_General_ID_Comanda_General_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Comanda_General_ID_Comanda_General_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Comanda_General_ID_Comanda_General_seq" OWNED BY public."Comanda_General"."ID_Comanda_General";


--
-- Name: Contracte; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Contracte" (
    "Tip_Contract" public.tipcontract NOT NULL,
    "ID_Contract" integer NOT NULL,
    "ID_Procedura" integer NOT NULL,
    "ID_Furnizor" integer NOT NULL,
    "Pret_Total_Contract" double precision NOT NULL,
    "Moneda" text NOT NULL,
    "ID_Utilizator_Creare" integer,
    "Data_Semnare" date NOT NULL,
    "Numar_Contract" text NOT NULL,
    "Numar_Inregistrare_Document" text,
    "Data_Inregistrare_Document" date,
    "Link_Scan_PDF" text
);


ALTER TABLE public."Contracte" OWNER TO nume_utilizator_pg;

--
-- Name: Contracte_ID_Contract_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Contracte_ID_Contract_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Contracte_ID_Contract_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Contracte_ID_Contract_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Contracte_ID_Contract_seq" OWNED BY public."Contracte"."ID_Contract";


--
-- Name: Detalii_Comanda_Produs; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Detalii_Comanda_Produs" (
    "ID_Detalii_Comanda_Produs" integer NOT NULL,
    "ID_Comanda_General" integer NOT NULL,
    "ID_Articol_Contractat" integer NOT NULL,
    "Cantitate_Comandata_Pachete" integer NOT NULL
);


ALTER TABLE public."Detalii_Comanda_Produs" OWNER TO nume_utilizator_pg;

--
-- Name: Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq" OWNED BY public."Detalii_Comanda_Produs"."ID_Detalii_Comanda_Produs";


--
-- Name: Documente_Livrare; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Documente_Livrare" (
    "ID_Document" integer NOT NULL,
    "ID_Livrare" integer NOT NULL,
    "Tip_Document" public.tipdocument NOT NULL,
    "Numar_Document" text NOT NULL,
    "Data_Document" date,
    "Link_Scan_PDF" text
);


ALTER TABLE public."Documente_Livrare" OWNER TO nume_utilizator_pg;

--
-- Name: Documente_Livrare_ID_Document_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Documente_Livrare_ID_Document_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Documente_Livrare_ID_Document_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Documente_Livrare_ID_Document_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Documente_Livrare_ID_Document_seq" OWNED BY public."Documente_Livrare"."ID_Document";


--
-- Name: Furnizori; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Furnizori" (
    "ID_Furnizor" integer NOT NULL,
    "Nume_Furnizor" text NOT NULL,
    "CUI" text,
    "Adresa" text,
    "Persoana_Contact" text,
    "Email_Contact" text,
    "Telefon_Contact" text
);


ALTER TABLE public."Furnizori" OWNER TO nume_utilizator_pg;

--
-- Name: Furnizori_ID_Furnizor_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Furnizori_ID_Furnizor_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Furnizori_ID_Furnizor_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Furnizori_ID_Furnizor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Furnizori_ID_Furnizor_seq" OWNED BY public."Furnizori"."ID_Furnizor";


--
-- Name: Livrare_Comenzi; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Livrare_Comenzi" (
    "ID_Livrare" integer NOT NULL,
    "ID_Detalii_Comanda_Produs" integer NOT NULL,
    "Cantitate_Livrata_Pachete" integer NOT NULL,
    "Data_Livrare" date NOT NULL,
    "Numar_Lot_Producator" text,
    "Data_Expirare" date,
    "ID_Utilizator_Inregistrare" integer
);


ALTER TABLE public."Livrare_Comenzi" OWNER TO nume_utilizator_pg;

--
-- Name: Livrare_Comenzi_ID_Livrare_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Livrare_Comenzi_ID_Livrare_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Livrare_Comenzi_ID_Livrare_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Livrare_Comenzi_ID_Livrare_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Livrare_Comenzi_ID_Livrare_seq" OWNED BY public."Livrare_Comenzi"."ID_Livrare";


--
-- Name: Loturi; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Loturi" (
    "ID_Lot" integer NOT NULL,
    "ID_Referat" integer NOT NULL,
    "Nume_Lot" text NOT NULL,
    "Descriere_Lot" text
);


ALTER TABLE public."Loturi" OWNER TO nume_utilizator_pg;

--
-- Name: Loturi_ID_Lot_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Loturi_ID_Lot_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Loturi_ID_Lot_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Loturi_ID_Lot_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Loturi_ID_Lot_seq" OWNED BY public."Loturi"."ID_Lot";


--
-- Name: Loturi_Procedura; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Loturi_Procedura" (
    "ID_Lot_Procedura" integer NOT NULL,
    "ID_Procedura" integer NOT NULL,
    "Nume_Lot" text NOT NULL,
    "Descriere_Lot" text
);


ALTER TABLE public."Loturi_Procedura" OWNER TO nume_utilizator_pg;

--
-- Name: Loturi_Procedura_ID_Lot_Procedura_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Loturi_Procedura_ID_Lot_Procedura_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Loturi_Procedura_ID_Lot_Procedura_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Loturi_Procedura_ID_Lot_Procedura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Loturi_Procedura_ID_Lot_Procedura_seq" OWNED BY public."Loturi_Procedura"."ID_Lot_Procedura";


--
-- Name: Oferte; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Oferte" (
    "ID_Oferta" integer NOT NULL,
    "ID_Furnizor" integer NOT NULL,
    "Data_Oferta" date NOT NULL,
    "Numar_Inregistrare" text,
    "Data_Inregistrare" date,
    "Moneda" text NOT NULL,
    "ID_Procedura" integer,
    "ID_Referat" integer
);


ALTER TABLE public."Oferte" OWNER TO nume_utilizator_pg;

--
-- Name: Oferte_ID_Oferta_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Oferte_ID_Oferta_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Oferte_ID_Oferta_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Oferte_ID_Oferta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Oferte_ID_Oferta_seq" OWNED BY public."Oferte"."ID_Oferta";


--
-- Name: Proceduri_Achizitie; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Proceduri_Achizitie" (
    "ID_Procedura" integer NOT NULL,
    "Nume_Procedura" text NOT NULL,
    "Tip_Procedura" public.tipprocedura NOT NULL,
    "Data_Creare" date NOT NULL,
    "Stare" text NOT NULL,
    "Numar_Inregistrare_Caiet_Sarcini" text,
    "Data_Inregistrare_Caiet_Sarcini" date,
    "Link_Scan_Caiet_Sarcini_PDF" text,
    "ID_Utilizator_Creare" integer
);


ALTER TABLE public."Proceduri_Achizitie" OWNER TO nume_utilizator_pg;

--
-- Name: Proceduri_Achizitie_ID_Procedura_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Proceduri_Achizitie_ID_Procedura_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Proceduri_Achizitie_ID_Procedura_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Proceduri_Achizitie_ID_Procedura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Proceduri_Achizitie_ID_Procedura_seq" OWNED BY public."Proceduri_Achizitie"."ID_Procedura";


--
-- Name: Producatori; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Producatori" (
    "ID_Producator" integer NOT NULL,
    "Nume_Producator" text NOT NULL
);


ALTER TABLE public."Producatori" OWNER TO nume_utilizator_pg;

--
-- Name: Producatori_ID_Producator_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Producatori_ID_Producator_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Producatori_ID_Producator_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Producatori_ID_Producator_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Producatori_ID_Producator_seq" OWNED BY public."Producatori"."ID_Producator";


--
-- Name: Produse; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Produse" (
    "ID_Produs" integer NOT NULL,
    "Nume_Generic" text NOT NULL,
    "Specificatii_Tehnice" text,
    "Unitate_Masura" text,
    "ID_Categorie" integer NOT NULL
);


ALTER TABLE public."Produse" OWNER TO nume_utilizator_pg;

--
-- Name: Produse_ID_Produs_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Produse_ID_Produs_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Produse_ID_Produs_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Produse_ID_Produs_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Produse_ID_Produs_seq" OWNED BY public."Produse"."ID_Produs";


--
-- Name: Produse_In_Loturi; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Produse_In_Loturi" (
    "ID_Produs_Lot" integer NOT NULL,
    "ID_Lot" integer NOT NULL,
    "ID_Produs_Referat" integer NOT NULL
);


ALTER TABLE public."Produse_In_Loturi" OWNER TO nume_utilizator_pg;

--
-- Name: Produse_In_Loturi_ID_Produs_Lot_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Produse_In_Loturi_ID_Produs_Lot_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Produse_In_Loturi_ID_Produs_Lot_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Produse_In_Loturi_ID_Produs_Lot_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Produse_In_Loturi_ID_Produs_Lot_seq" OWNED BY public."Produse_In_Loturi"."ID_Produs_Lot";


--
-- Name: Produse_In_Referate; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Produse_In_Referate" (
    "ID_Produs_Referat" integer NOT NULL,
    "ID_Referat" integer NOT NULL,
    "ID_Produs_Generic" integer NOT NULL,
    "Cantitate_Solicitata" integer NOT NULL
);


ALTER TABLE public."Produse_In_Referate" OWNER TO nume_utilizator_pg;

--
-- Name: Produse_In_Referate_ID_Produs_Referat_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Produse_In_Referate_ID_Produs_Referat_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Produse_In_Referate_ID_Produs_Referat_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Produse_In_Referate_ID_Produs_Referat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Produse_In_Referate_ID_Produs_Referat_seq" OWNED BY public."Produse_In_Referate"."ID_Produs_Referat";


--
-- Name: Referate_Necesitate; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Referate_Necesitate" (
    "ID_Referat" integer NOT NULL,
    "Data_Creare" date NOT NULL,
    "Stare" public.starereferat NOT NULL,
    "Numar_Referat" text,
    "Numar_Inregistrare_Document" text,
    "Data_Inregistrare_Document" date,
    "Link_Scan_PDF" text,
    "ID_Utilizator_Creare" integer,
    "Observatii" text,
    "Observatii_Aprobare" text
);


ALTER TABLE public."Referate_Necesitate" OWNER TO nume_utilizator_pg;

--
-- Name: Referate_Necesitate_ID_Referat_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Referate_Necesitate_ID_Referat_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Referate_Necesitate_ID_Referat_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Referate_Necesitate_ID_Referat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Referate_Necesitate_ID_Referat_seq" OWNED BY public."Referate_Necesitate"."ID_Referat";


--
-- Name: Utilizatori; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Utilizatori" (
    "ID_Utilizator" integer NOT NULL,
    "Nume_Utilizator" text NOT NULL,
    "Email" text NOT NULL,
    "Parola_Hash" text NOT NULL,
    "Data_Creare" date NOT NULL,
    "Este_Activ" boolean NOT NULL
);


ALTER TABLE public."Utilizatori" OWNER TO nume_utilizator_pg;

--
-- Name: Utilizatori_ID_Utilizator_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Utilizatori_ID_Utilizator_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Utilizatori_ID_Utilizator_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Utilizatori_ID_Utilizator_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Utilizatori_ID_Utilizator_seq" OWNED BY public."Utilizatori"."ID_Utilizator";


--
-- Name: Variante_Comerciale_Produs; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public."Variante_Comerciale_Produs" (
    "ID_Varianta_Comerciala" integer NOT NULL,
    "ID_Produs_Generic" integer NOT NULL,
    "ID_Producator" integer NOT NULL,
    "Cod_Catalog" text NOT NULL,
    "Nume_Comercial_Extins" text,
    "Descriere_Ambalare" text NOT NULL,
    "Cantitate_Standard_Ambalare" integer NOT NULL
);


ALTER TABLE public."Variante_Comerciale_Produs" OWNER TO nume_utilizator_pg;

--
-- Name: Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq; Type: SEQUENCE; Schema: public; Owner: nume_utilizator_pg
--

CREATE SEQUENCE public."Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq" OWNER TO nume_utilizator_pg;

--
-- Name: Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nume_utilizator_pg
--

ALTER SEQUENCE public."Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq" OWNED BY public."Variante_Comerciale_Produs"."ID_Varianta_Comerciala";


--
-- Name: contracte_loturi_procedura_asociere; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public.contracte_loturi_procedura_asociere (
    contract_id integer NOT NULL,
    lot_procedura_id integer NOT NULL
);


ALTER TABLE public.contracte_loturi_procedura_asociere OWNER TO nume_utilizator_pg;

--
-- Name: lot_procedura_articole_asociere; Type: TABLE; Schema: public; Owner: nume_utilizator_pg
--

CREATE TABLE public.lot_procedura_articole_asociere (
    lot_procedura_id integer NOT NULL,
    produs_referat_id integer NOT NULL
);


ALTER TABLE public.lot_procedura_articole_asociere OWNER TO nume_utilizator_pg;

--
-- Name: Articole_Contractate ID_Articol_Contractat; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Contractate" ALTER COLUMN "ID_Articol_Contractat" SET DEFAULT nextval('public."Articole_Contractate_ID_Articol_Contractat_seq"'::regclass);


--
-- Name: Articole_Oferta ID_Articol_Oferta; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Oferta" ALTER COLUMN "ID_Articol_Oferta" SET DEFAULT nextval('public."Articole_Oferta_ID_Articol_Oferta_seq"'::regclass);


--
-- Name: Categorii ID_Categorie; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Categorii" ALTER COLUMN "ID_Categorie" SET DEFAULT nextval('public."Categorii_ID_Categorie_seq"'::regclass);


--
-- Name: Comanda_General ID_Comanda_General; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Comanda_General" ALTER COLUMN "ID_Comanda_General" SET DEFAULT nextval('public."Comanda_General_ID_Comanda_General_seq"'::regclass);


--
-- Name: Contracte ID_Contract; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Contracte" ALTER COLUMN "ID_Contract" SET DEFAULT nextval('public."Contracte_ID_Contract_seq"'::regclass);


--
-- Name: Detalii_Comanda_Produs ID_Detalii_Comanda_Produs; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Detalii_Comanda_Produs" ALTER COLUMN "ID_Detalii_Comanda_Produs" SET DEFAULT nextval('public."Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq"'::regclass);


--
-- Name: Documente_Livrare ID_Document; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Documente_Livrare" ALTER COLUMN "ID_Document" SET DEFAULT nextval('public."Documente_Livrare_ID_Document_seq"'::regclass);


--
-- Name: Furnizori ID_Furnizor; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Furnizori" ALTER COLUMN "ID_Furnizor" SET DEFAULT nextval('public."Furnizori_ID_Furnizor_seq"'::regclass);


--
-- Name: Livrare_Comenzi ID_Livrare; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Livrare_Comenzi" ALTER COLUMN "ID_Livrare" SET DEFAULT nextval('public."Livrare_Comenzi_ID_Livrare_seq"'::regclass);


--
-- Name: Loturi ID_Lot; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Loturi" ALTER COLUMN "ID_Lot" SET DEFAULT nextval('public."Loturi_ID_Lot_seq"'::regclass);


--
-- Name: Loturi_Procedura ID_Lot_Procedura; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Loturi_Procedura" ALTER COLUMN "ID_Lot_Procedura" SET DEFAULT nextval('public."Loturi_Procedura_ID_Lot_Procedura_seq"'::regclass);


--
-- Name: Oferte ID_Oferta; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Oferte" ALTER COLUMN "ID_Oferta" SET DEFAULT nextval('public."Oferte_ID_Oferta_seq"'::regclass);


--
-- Name: Proceduri_Achizitie ID_Procedura; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Proceduri_Achizitie" ALTER COLUMN "ID_Procedura" SET DEFAULT nextval('public."Proceduri_Achizitie_ID_Procedura_seq"'::regclass);


--
-- Name: Producatori ID_Producator; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Producatori" ALTER COLUMN "ID_Producator" SET DEFAULT nextval('public."Producatori_ID_Producator_seq"'::regclass);


--
-- Name: Produse ID_Produs; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse" ALTER COLUMN "ID_Produs" SET DEFAULT nextval('public."Produse_ID_Produs_seq"'::regclass);


--
-- Name: Produse_In_Loturi ID_Produs_Lot; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Loturi" ALTER COLUMN "ID_Produs_Lot" SET DEFAULT nextval('public."Produse_In_Loturi_ID_Produs_Lot_seq"'::regclass);


--
-- Name: Produse_In_Referate ID_Produs_Referat; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Referate" ALTER COLUMN "ID_Produs_Referat" SET DEFAULT nextval('public."Produse_In_Referate_ID_Produs_Referat_seq"'::regclass);


--
-- Name: Referate_Necesitate ID_Referat; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Referate_Necesitate" ALTER COLUMN "ID_Referat" SET DEFAULT nextval('public."Referate_Necesitate_ID_Referat_seq"'::regclass);


--
-- Name: Utilizatori ID_Utilizator; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Utilizatori" ALTER COLUMN "ID_Utilizator" SET DEFAULT nextval('public."Utilizatori_ID_Utilizator_seq"'::regclass);


--
-- Name: Variante_Comerciale_Produs ID_Varianta_Comerciala; Type: DEFAULT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Variante_Comerciale_Produs" ALTER COLUMN "ID_Varianta_Comerciala" SET DEFAULT nextval('public."Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq"'::regclass);


--
-- Data for Name: Articole_Contractate; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Articole_Contractate" ("ID_Articol_Contractat", "ID_Contract", "ID_Produs_Referat", "ID_Varianta_Comerciala", "Cantitate_Contractata_Pachete", "Pret_Unitar_Pachet_Contract") FROM stdin;
\.


--
-- Data for Name: Articole_Oferta; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Articole_Oferta" ("ID_Articol_Oferta", "ID_Oferta", "ID_Varianta_Comerciala", "ID_Produs_Referat", "Pret_Unitar_Pachet", "ID_Lot_Procedura", "Observatii") FROM stdin;
\.


--
-- Data for Name: Categorii; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Categorii" ("ID_Categorie", "Nume_Categorie") FROM stdin;
1	Ion
2	MLPA
3	PCR hemato
4	PCR virale
5	MSI Dx
6	Nanopore dx
7	Extracție Qia
8	PCR tumori
9	Bioanalyzer
10	Nanopore secvențiere
11	Hibridizare
12	Nanopore biblioteci
13	Qubit
14	Biomol
15	GeXP
16	MiniSeq secvențiere
17	Extracție manuală
18	dPCR
19	MiniSeq tumori
20	Necategorizat
21	QC biomol
22	QC IHC
\.


--
-- Data for Name: Comanda_General; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Comanda_General" ("ID_Comanda_General", "ID_Contract", "Data_Comanda", "Numar_Comanda", "Stare_Comanda", "Numar_Inregistrare_Document", "Data_Inregistrare_Document", "Link_Scan_PDF", "ID_Utilizator_Creare") FROM stdin;
\.


--
-- Data for Name: Contracte; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Contracte" ("Tip_Contract", "ID_Contract", "ID_Procedura", "ID_Furnizor", "Pret_Total_Contract", "Moneda", "ID_Utilizator_Creare", "Data_Semnare", "Numar_Contract", "Numar_Inregistrare_Document", "Data_Inregistrare_Document", "Link_Scan_PDF") FROM stdin;
\.


--
-- Data for Name: Detalii_Comanda_Produs; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Detalii_Comanda_Produs" ("ID_Detalii_Comanda_Produs", "ID_Comanda_General", "ID_Articol_Contractat", "Cantitate_Comandata_Pachete") FROM stdin;
\.


--
-- Data for Name: Documente_Livrare; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Documente_Livrare" ("ID_Document", "ID_Livrare", "Tip_Document", "Numar_Document", "Data_Document", "Link_Scan_PDF") FROM stdin;
\.


--
-- Data for Name: Furnizori; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Furnizori" ("ID_Furnizor", "Nume_Furnizor", "CUI", "Adresa", "Persoana_Contact", "Email_Contact", "Telefon_Contact") FROM stdin;
\.


--
-- Data for Name: Livrare_Comenzi; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Livrare_Comenzi" ("ID_Livrare", "ID_Detalii_Comanda_Produs", "Cantitate_Livrata_Pachete", "Data_Livrare", "Numar_Lot_Producator", "Data_Expirare", "ID_Utilizator_Inregistrare") FROM stdin;
\.


--
-- Data for Name: Loturi; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Loturi" ("ID_Lot", "ID_Referat", "Nume_Lot", "Descriere_Lot") FROM stdin;
\.


--
-- Data for Name: Loturi_Procedura; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Loturi_Procedura" ("ID_Lot_Procedura", "ID_Procedura", "Nume_Lot", "Descriere_Lot") FROM stdin;
\.


--
-- Data for Name: Oferte; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Oferte" ("ID_Oferta", "ID_Furnizor", "Data_Oferta", "Numar_Inregistrare", "Data_Inregistrare", "Moneda", "ID_Procedura", "ID_Referat") FROM stdin;
\.


--
-- Data for Name: Proceduri_Achizitie; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Proceduri_Achizitie" ("ID_Procedura", "Nume_Procedura", "Tip_Procedura", "Data_Creare", "Stare", "Numar_Inregistrare_Caiet_Sarcini", "Data_Inregistrare_Caiet_Sarcini", "Link_Scan_Caiet_Sarcini_PDF", "ID_Utilizator_Creare") FROM stdin;
\.


--
-- Data for Name: Producatori; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Producatori" ("ID_Producator", "Nume_Producator") FROM stdin;
\.


--
-- Data for Name: Produse; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Produse" ("ID_Produs", "Nume_Generic", "Specificatii_Tehnice", "Unitate_Masura", "ID_Categorie") FROM stdin;
1	Kit reactivi de secvențiere, 300 cicluri, capacitate medie	Kit ce conține un cartuș cu reactivii necesari pentru secvențiere, tampon de hibridizare și o celulă (cameră) de secvențiere, compatibile cu sistemul miniSeq produs de Illumina, din dotarea laboratorului\nReactivii permit generarea clusterelor pe suprafața chipului, secvențierea prin sinteză și spălările necesare\nKitul permite 300 de cicluri de citire a secvențelor de ADN și a două secvențe index\nCapabil să secvențieze 2,4 Gigabaze (8 milioane de fragmente)	kit	16
2	Kit reactivi de secvențiere, 300 cicluri, capacitate mare	Kit ce conține un cartuș cu reactivii necesari pentru secvențiere, tampon de hibridizare și o celulă (cameră) de secvențiere, compatibile cu sistemul miniSeq produs de Illumina, din dotarea laboratorului\nReactivii permit generarea clusterelor pe suprafața chipului, secvențierea prin sinteză și spălările necesare\nKitul permite 300 de cicluri de citire a secvențelor de ADN și a două secvențe index\nCapabil să secvențieze 7,5 Gigabaze (25 milioane de fragmente)	kit	16
3	Celule de secvențiere cu 2048 nanopori	Celulă (cameră) de secvențiere ce permite citirea secvenței unor molecule individuale de ADN cu lungimea cuprinsă între 200 baze și 30.000 baze sau mai mult, prin metoda nanoporilor\nCelula este un dispozitiv consumabil ce poate fi utilizată cu un sistem compatibil pentru achiziția și prelucrarea datelor\nPoate fi folosită împreună cu reactivii corespunzători, permițând citirea secvențelor ADN cu o rată de eroare mică (precizie mai mare de 99%, Q20+)\nConține 2048 de nanopori, din care maxim 512 pot fi utilizați simultan pentru secvențiere\nInclude un circuit integrat specific\nPoate fi stocată la 2-8˚C pentru perioada specificată de producător\nPoate fi spălată și reutilizată pentru cel puțin un nou experiment, în condițiile specificate de producător\nPachetul conține o celulă de secvențiere	buc	10
4	Celule de secvențiere cu 126 nanopori	Celulă (cameră) de secvențiere ce permite citirea secvenței unor molecule individuale de ADN cu lungimea cuprinsă între 200 baze și 30.000 baze sau mai mult, prin metoda nanoporilor\nCelula este un dispozitiv consumabil ce poate fi utilizată cu un sistem compatibil pentru achiziția și prelucrarea datelor\nUtilizarea celulei necesită un adaptor care include un circuit integrat specific și care este reutilizabil\nPoate fi folosită împreună cu reactivii corespunzători, permițând citirea secvențelor ADN cu o rată de eroare mică (precizie mai mare de 99%, Q20+)\nConține 126 de nanopori\nPoate fi stocată la 2-8˚C pentru perioada specificată de producător\nPachetul conține 12 celule de secvențiere	buc	10
5	Kit reactivi pentru amorsarea celulelor de secvențiere, 6 reacții	Set de reactivi necesari pentru amorsarea celulelor de secvențiere specificate la poziția 1\nReactivii sunt suficienți pentru 6 reacții\nCompatibil cu protocoalele de preparare a bibliotecilor de fragmente recomandate de producătorul celulelor de secvențiere.\nReactivii sunt compatibili cu toate tipurile de biblioteci de fragmente ADN	kit	10
6	Kit reactivi pentru spălarea celulelor de secvențiere	Kitul conține reactivi pentru spălarea camerelor de secvențiere cu nanopori în vederea stocării și reutilizării\nConține reactivi care permit îndepărtarea fragmentelor de ADN rămase de la utilizarea anterioară a camerei, în vederea evitării contaminării\nReactivii sunt compatibili cu celulele pentru secvențiere  solicitate\nInclud tampoanele pentru spălarea și pentru stocarea camerei de curgere\nReactivii sunt compatibili cu toate tipurile de biblioteci de fragmente ADN\nConține reactivi suficienți pentru 6 utilizări	kit	10
7	Kit cu reactivi suplimentari pentru secvențiere	Pachet de reactivi compatibili cu celulele de secvențiere descrise la punctul 1\nPermit reutilizarea celulelor de secvențiere, în condițiile descrise de producător\nReactivii includ: tampon de secvențiere, tampon de eluție, soluție pentru diluarea bibliotecilor de fragmente, reactivi pentru amorsarea camerei de secvențiere\nReactivii sunt compatibili cu toate tipurile de biblioteci de fragmente ADN\nConține reactivi suficienți pentru 12 reacții	kit	10
8	Kit reactivi pentru prepararea probelor prin ligare, multiplex	Conține reactivi ce permit prepararea bibliotecilor de fragmente pentru secvențiere prin metoda nanoporilor\nUtilizarea reactivilor este compatibilă cu celulele de secvențiere prin metoda nanoporilor\nMetoda de obținere a bibliotecilor de fragmente este bazată pe ligarea la capetele fragmentelor de ADN a unor adaptori care conțin etichete moleculare (secvențe index), urmată de ligarea adaptorilor pentru secvențiere\nMetoda nu utilizează amplificarea prin PCR și menține metilarea fragmentelor de ADN genomic din probele biologice\nReactivii permit secvențierea a până la 24 de probe ADN diferite în cadrul aceluiași experiment (multiplexare)\nReactivii permit citirea secvențelor ADN cu o rată de eroare mică (precizie mai mare de 99%, Q20+)\nKitul include 24 de secvențe index unice, adaptorii specifici, soluțiile tampon necesare, particule magnetice pentru purificarea produșilor de reacție, soluția pentru spălarea camerei de secvențiere înainte de utilizare, reactivii necesari pentru încărcarea camerei de secvențiere\nKitul poate fi utilizat pentru secvențierea a 400 – 1000 ng ADN genomic sau a ampliconilor\nConține reactivi suficienți pentru 6 reacții	kit	12
9	Kit cu reactivi suplimentari pentru prepararea probelor prin ligare	Kitul conține reactivi suplimentari, utilizați pentru a crește numărul de reacții ce pot fi efectuate cu ajutorul kitului descris la punctul 1 (pentru prepararea probelor prin ligare, multiplex)\nInclude: adaptori pentru secvențiere, particule magnetice pentru purificarea produșilor de reacție, tampoane specifice\nReactivii sunt compatibili cu celulele de secvențiere prin metoda nanoporilor  solicitate\nConține reactivi suficienți pentru 12 reacții	kit	12
10	Kit reactivi pentru prepararea probelor prin ligare, uniplex	Conține reactivi ce permit prepararea bibliotecilor de fragmente pentru secvențiere prin metoda nanoporilor\nUtilizarea reactivilor este compatibilă cu celulele de secvențiere prin metoda nanoporilor descrise la Lotul 2, pozițiile 1 și 2\nMetoda de obținere a bibliotecilor de fragmente este bazată pe ligarea la capetele fragmentelor de ADN a unor adaptori, urmată de ligarea adaptorilor pentru secvențiere\nMetoda nu utilizează amplificarea prin PCR și menține metilarea fragmentelor de ADN genomic din probele biologice\nReactivii permit secvențierea unei singure probe ADN în cadrul aceluiași experiment (uniplex)\nReactivii permit citirea secvențelor ADN cu o rată de eroare mică (precizie mai mare de 99%, Q20+)\nKitul include adaptorii specifici, soluțiile tampon necesare, particule magnetice pentru purificarea produșilor de reacție, soluția pentru spălarea camerei de secvențiere înainte de utilizare, reactivii necesari pentru încărcarea camerei de secvențiere\nKitul poate fi utilizat pentru secvențierea a 1 microgram ADN genomic sau a ampliconilor\nPermite secvențierea directă a ADNc și multiplexarea prin PCR\nConține reactivi suficienți pentru 6 reacții	kit	12
11	Kit reactivi pentru prepararea rapida a probelor, multiplex	Conține reactivi ce permit prepararea rapidă a bibliotecilor de fragmente pentru secvențiere prin metoda nanoporilor\nUtilizarea reactivilor este compatibilă cu celulele de secvențiere prin metoda nanoporilor\nMetoda de obținere a bibliotecilor de fragmente este bazată pe ligarea la capetele fragmentelor de ADN a unor adaptori care conțin etichete moleculare (secvențe index), urmată de ligarea adaptorilor pentru secvențiere\nReactivii permit secvențierea a până la 12 de probe ADN diferite în cadrul aceluiași experiment (multiplexare)\nReactivii permit citirea secvențelor ADN cu o rată de eroare mică (precizie mai mare de 99%, Q20+)\nKitul include 12 de secvențe index unice, adaptorii specifici, soluțiile tampon necesare, soluția pentru spălarea camerei de secvențiere înainte de utilizare, reactivii necesari pentru încărcarea camerei de secvențiere\nKitul poate fi utilizat pentru secvențierea a 10 nanograme – 2 micrograme ADN genomic sau a ampliconilor\nConține reactivi suficienți pentru 6 reacții	kit	12
12	Kit cu reactivi suplimentari pentru prepararea rapida a probelor	Kitul conține reactivi suplimentari, utilizați pentru a crește numărul de reacții ce pot fi efectuate cu ajutorul kitului descris la punctul 1 (pentru prepararea rapidă a probelor, multiplex)\nInclude: adaptori pentru secvențiere, particule magnetice pentru purificarea produșilor de reacție, tampoane specifice\nReactivii sunt compatibili cu celulele de secvențiere prin metoda nanoporilor\nConține reactivi suficienți pentru 12 reacții	kit	12
13	Kit cu reactivi pentru multiplexarea probelor prin utilizarea PCR	Conține reactivi ce permit prepararea bibliotecilor de fragmente pentru secvențiere prin metoda nanoporilor. Utilizarea reactivilor este compatibilă cu celulele de secvențiere prin metoda nanoporilor descrise la Lotul 2, pozițiile 1 și 2. Kitul permite multiplexarea probelor ce vor fi secvențiate pe baza protocolului de ligare a adaptorilor. Reactivii funcționează ca o extindere a kitului descris la poziția 3. Reactivii permit secvențierea a până la 12 de probe ADN diferite în cadrul aceluiași experiment (multiplexare). Metoda se bazează pe incorporarea de secvențe index la capetele fragmentelor de ADN cu ajutorul unor primeri unici, prin PCR. Ulterior, aceste  fragmente  sunt pregătite pentru secvențiere prin ligarea adaptorilor specifici. Kitul include 12 primeri cu secvențe index și un adaptor amplificabil. Conține reactivi suficienți pentru 6 reacții.	kit	12
14	Kit pentru prepararea rapidă a probelor și amplificare PCR	Conține reactivi ce permit prepararea bibliotecilor de fragmente pentru secvențiere prin metoda nanoporilor. Utilizarea reactivilor este compatibilă cu celulele de secvențiere prin metoda nanoporilor  solicitate. Kitul se bazează pe utilizarea unei transpozaze care clivează moleculele de ADN și, simultan, adaugă secvențe amplificabile la capetele acestora. Urmează apoi o amplificare PCR cu primeri ce include secvențe index unice și, în final, atașarea de adaptori specifici. Reactivii permit secvențierea a până la 24 de probe ADN diferite în cadrul aceluiași experiment (multiplexare). Reactivii permit secvențierea probelor ce conțin cantități reduse de ADN (1-5 ng). Kitul include adaptorii amplificabili, soluțiile tampon necesare, enzimele necesare, 24 de primeri cu secvențe index, adaptorul raid pentru secvențiere particule magnetice pentru purificarea produșilor de reacție, soluția pentru spălarea camerei de secvențiere înainte de utilizare, reactivii necesari pentru încărcarea camerei de secvențiere. Conține reactivi suficienți pentru 6 reacții.	kit	12
15	Reactivi pentru îndepărtarea fragmentelor mici de ADN	Reactiv ce permite eliminarea fragmentelor de ADN mai scurte de 25 kbaze prin precipitare, spălare și apoi resuspendare. Compatibil cu toate kiturile de obținere a bibliotecilor de fragmente pentru secvențierea prin metoda nanoporilor. Utilizarea reactivilor este compatibilă cu celulele de secvențiere prin metoda nanoporilor  solicitate. Conține reactivi suficienți pentru 30 reacții.	kit	12
16	Kit reactivi pentru analiza ARN tumoral, multiplex	*NU*\r\nKit pentru analiza prin secvențiere de nouă generație a ARN mesager exprimat în țesuturi tumorale.\r\nReactivii sunt compatibili cu secvențiatorul Illumina MiniSeq aflat în dotarea laboratorului.\r\nPermite analiza expresiei genelor, identificarea variantelor de secvență (polimorfisme uninucleotidice și inserții/deleții mici) și detecția genelor de fuziune.\r\nKitul analizează un panel de cel puțin 130 gene implicate în oncogeneză.\r\nKitul necesită cantități reduse de ARN extras, începând de la 10ng.\r\nProducătorul furnizează o soluție pentru analiza datelor generate, ce permite elaborarea unui raport privind rezultatele analizei. Inclusă în costul reactivilor.\r\nKitul include reactivii necesari pentru prepararea bibliotecilor de fragmente ce vor fi secvențiate - reactivi pentru: repararea capetelor fragmentelor de ADN, ligarea adaptorilor, amplificarea PCR, captura prin hibridizare a moleculelor ARN de interes, multiplexarea probelor (12 secvențe index diferite).\r\nPachetul include reactivi pentru reverstranscriere, cu următoarele caracteristici:\r\nReactivul conține 10.000 unități reverstranscriptază pentru sinteza lanțului de ADN complementar ARN\r\nEnzima este derivată din M-MuLV, are activitate redusă de RNAză H și termostabilitate sporită (până la 48˚C)\r\nEnzima are specificitate și eficiență crescute, permite sinteza de molecule de cDNA de până la 12.000 nucleotide\r\nKitul include enzima, tamponul de reacție optimizat și soluție DTT 0,1M. Concentrația enzimei este de 200.000 U/mL.\r\nKitul include numărul necesar de cartușe cu reactivi de secvențiere (150 cicluri de citire) și de camere de secvențiere (flow-cells).\r\nReactivii permit citirea a până la 25 milioane fragmente de ADN și sunt compatibili cu sistemul miniSeq.\r\nPentru a facilita compararea ofertelor, furnizorul va calcula și specifica costul / test, ținând cont de faptul că vor fi realizate 8 teste / rundă de secvențiere	kit	19
19	Kit reactivi pentru indexarea prin ligare a bibliotecilor de fragmente amplificate	*NU*\r\nReactivi pentru indexarea bibliotecilor de fragmente.\r\nReactivii sunt compatibili cu secvențiatorul Illumina MiniSeq aflat în dotarea laboratorului.\r\nReactivii pot fi utilizați împreună cu kiturile descrise la pozițiile 2, 3 și 4\r\nKitul conține combinații unice de adaptori index i7 și index i5 ce se leagă de capetele fragmentelor ADN prin ligare.\r\nKitul conține 24 de adaptori indexați, suficienți pentru 24 de probe, dispuși în placă cu 96 de godeuri	kit	19
22	Kit pentru analiza riscului ereditar de cancer 113 gene	Kit pentru analiza prin secvențiere de nouă generație a variantelor genetice asociate cu risc ereditar crescut de cancer colorectal, de sân, ovarian, gastric și cu alte localizări.\nReactivii sunt compatibili cu secvențiatorul Illumina MiniSeq aflat în dotarea laboratorului.\nKitul permite analiza a 113 gene și 125 de polimorfisme uninucleotidice (din care 77 pot fi utilizate pentru calcularea scorului de risc poligenic).\nMetoda poate detecta variante genetice germinale: variații ale numărului de copii, inserții/deleții, polimorfisme uninucleotidice.\nKit bazat pe hibridizarea de sonde oligonucleotidice biotinilate cu fragmentele indexate de ADN genomic.\nPoate fi utilizat pentru ADN extras din sânge sau salivă.\nProducătorul furnizează o soluție pentru analiza datelor generate, inclusă în costul reactivilor.\nReactivi pentru 8 reacții de selecție multiplexate	kit	19
25	Kit reactivi pentru extracția manuala a ARN din țesuturi fibroase	Kit de reactivi pentru extracția ARN din țesuturi fibroase (țesut conjunctiv, piele, mușchi) bazat pe centrifugare și adsorbție pe membrane selective.\nPentru izolarea ARN cu lungime mai mare de 200 nucleotide\nInclude proteinaza K pentru îndepărtarea proteinelor.\nInclude DNAză fără activitate de RNAză pentru îndepărtarea ARN.\nPermite prelucrarea a 0,5-30 mg țesut și produce până la 100µg ARN într-un volum de 30µL eluat.\nCompatibil cu omogenizatorul mecanic TissueLyser II aflat în dotarea laboratorului.\nInclude coloanele de separare și tuburile de colectare necesare.\nInclude toți reactivii necesari (tampoane de liză, de spălare etc)\nKit pentru 50 reacții	kit	17
27	Kit pentru extracția manuala a ADN bacterian pentru studiul microbiomului	Kitul permite izolarea și purificarea ADN bacterian total din fluide biologice sau țesuturi.\nKitul conține reactivi care permit îndepărtarea selectivă a ADN-ului uman prezent în probele biologice, prin liza selectivă a celulelor eucariote și degradarea acizilor nucleici ai acestora folosind benzonază.\nConține reactivi care permit liza celulelor bacteriene prin procedee chimice și mecanice.\nPurificarea ADN bacterian se realizează prin adsorbția selectivă pe coloane și cenntrifugare.\nKitul este compatibil cu disociere mecanică a probelor folosind sistemul TissueLyser II aflat în dotarea laboratorului\nKit pentru 50 probe	kit	17
29	Kit reactivi pentru purificarea ADN din țesuturi fixate și incluse în parafină	Trusă de reactivi pentru extracția și purificarea ADN din țesuturi fixate și incluse în parafină, marcaj CE-IVD.\nMetodă manuală, bazată pe adsorbția pe membrane de siliciu și centrifugare.\nMetoda nu presupune incubări îndelungate și îndepărtează parțial efectele fixării cu formol asupra ADN\nProtocolul de lucru include condiții speciale de liză și deparafinare a probelor.\nKit pentru 50 de probe	kit	17
31	Kit pentru purificarea acizilor nucleici liberi din plasmă	Trusă de reactivi pentru purificarea și concentrarea ADN și ARN liber, circulant în plasmă.\nMetodă manuală, bazată pe adsorbția pe membrane de siliciu și centrifugare.\nMetoda permite concentrarea cantităților mici de acizi nucleici liberi și poate fi folosită înn scop diagnostic.\nMetoda permite eluarea în volume variabile, între 20 și 150 microlitri.\nKit pentru 50 de probe	kit	17
30	Kit reactivi pentru purificarea ARN din țesuturi fixate și incluse în parafină	Trusă de reactivi pentru extracția și purificarea ARN din țesuturi fixate și incluse în parafină, marcaj CE-IVD.\r\nMetodă manuală, bazată pe adsorbția pe membrane de siliciu și centrifugare.\r\nKitul include soluția de deparafinare a secțiunilor.\r\nMetoda permite îndepărtarea efectelor fixării cu formol și permite eliberarea ARN fără a afecta integritatea acestuia.\r\nMetoda include condiții speciale de liză a probelor și un pas de îndepărtare a ADN.\r\nKit pentru 50 de probe	kit	17
28	Kit pentru extractia manuala a ADN genomic de masă moleculară mare	Kitul permite izolarea și purificarea ADN genomic cu lungime mare (100 – 200 kbaze)\r\nPermite îndepărtarea blândă a contaminanților (proteine, lipide și alții)\r\nPermite extracția ADN din 8 x 10E8 celule sau din sânge integral.\r\nCelulele sunt lizate în prezența unui stabilizator pentru ADN, apoi proba este tratată cu RNAză.\r\nProteinele sunt îndepărtate prin precipitare cu săruri, iar ADN este precipitat cu alcool și apoi recuperat în tampon de eluție	kit	17
26	Reactiv pentru prezervarea ARN din țesuturi	Soluție pentru stabilizarea imediată și prezervarea ARN.\r\nPermite procesarea fragmentelor de țesut la temperatura camerei.\r\nConservă profilul expresiei de gene în țesuturile recoltate.\r\nPermite conservarea țesuturilor cu protecția ARN pentru 24h la 37˚C, 7 zile la temperatura ambientală, 4 săptămâni la frigider sau pe termen nelimitat la -20 - -80˚C\r\nCompatibil cu kitul de reactivi pentru purificarea ARN din țesuturi fixate și incluse în parafină (metodă manuală).\r\nKitul conține 50 mL de soluție, suficientă pentru 25 probe	kit	17
24	Kit reactivi pentru indexarea bibliotecilor obținute prin fragmentare enzimatică, multiplex	Reactivi pentru indexarea fragmentelor ADN, compatibili cu kitul pentru analiza riscului ereditar de cancer 113 gene.\r\nInclude oligonucleotide cu secvențe unice pentru identificarea a 96 de probe.\r\nSe utilizează în cursul unei reacții PCR, înainte de selecția prin hibridizare și captură a fragmentelor de interes.\r\nReactivi suficienți pentru indexarea a 96 probe	kit	19
21	Kit reactivi pentru obținerea ADN pentru secvențiere prin amplificare din probe incluse la parafină	*NU*\r\nReactiv ce permite amplificarea directă a ADN din țesuturi fixate și incluse în parafină.\r\nCompatibil cu reactvii de la poziția 5\r\nNu necesită deparafinarea țesuturilor și purificarea ADN\r\nConține soluție de transfer și un reactiv de preparare directă.\r\nReactivi suficienți pentru 24 de reacții	kit	19
34	Vârfuri de pipetare de 1500 µL. Cutie cu 1024 vârfuri	Vârfuri de pipetare cu volumul de 1500 µL, compatibile cu sistemul QIAsymphony din dotarea laboratorului.\nPrevăzute cu filtru și capabile de detecția nivelului de lichid.\nCutii cu 1024 vârfuri (32 suporturi cu câte 32 vârfuri fiecare)	cutie	7
35	Vârfuri de pipetare de 200 µL. Cutie cu 1024 vârfuri	Vârfuri de pipetare cu volumul de 200 µL, compatibile cu sistemul QIAsymphony din dotarea laboratorului.\nCutii cu 1024 vârfuri (32 suporturi cu câte 32 vârfuri fiecare)	cutie	7
36	Plăci cu 8 cupe de reacție. Cutie cu 336 bucăți	Plăci cu 8 cupe de reacție, compatibile cu sistemul QIAsymphony din dotarea laboratorului.\nCutie cu 336 bucăți	cutie	7
37	Capace pentru bare magnetice. Cutie cu 144 bucăți	Capace pentru bare magnetice, compatibile cu sistemul QIAsymphony din dotarea laboratorului.\nCutie cu 144 bucăți	cutie	7
38	Plăci cu 96 godeuri pentru eluat. Cutie cu 24 plăci	Plăci cu 96 godeuri pentru eluat, compatibile cu sistemul QIAsymphony din dotarea laboratorului.\nVolum de stocare 100 µL\nInclud capace pentru godeuri.\nGodeuri cu fund rotund.\nCutie cu 144 bucăți	cutie	7
42	Kit pentru cuantificarea fluorimetrică de sensibilitate ridicată a ARN	Kitul permite cuantificarea fluorimetrică de sensibilitate ridicata a ARN. Compatibil cu sistemul de cuantificare fluorimetrică Qubit, produs de ThermoFisher Scientific. Spectrul de excitație și emisie a fluorescenței: 644/673. Limita de cuantificare ARN cuprinsă între 4-200 de nanograme. Kitul include tamponul de diluție, soluție fluorescentă concentrată, standarde de cantitate. Kit pentru 100 de reacții.	kit	13
43	Kit pentru cuantificarea fluorimetrică de sensibilitate ridicată a ADN	Kitul permite cuantificarea fluorimetrică de sensibilitate ridicată a ADN dublu catenar. Compatibil cu sistemul de cuantificare fluorimetrică Qubit, produs de ThermoFisher Scientific. Spectrul de excitație și emisie a fluorescenței: 510/527. Limita de cuantificare ADN cuprinsă între 0,1 - 120 nanograme. Kitul include tamponul de diluție, soluție fluorescentă concentrată, standarde de cantitate. Kit pentru 100 de reacții.	kit	13
44	Kit pentru cuantificarea fluorimetrică a ARN	Kitul permite cuantificarea fluorimetrică  a ARN. Compatibil cu sistemul de cuantificare fluorimetrică Qubit, produs de ThermoFisher Scientific. Spectrul de excitație și emisie a fluorescenței: 644/673. Limita de cuantificare ARN cuprinsă între 10 - 2000 nanograme. Kitul include tamponul de diluție, soluție fluorescentă concentrată, standarde de cantitate. Kit pentru 100 de reacții.	kit	13
45	Kit pentru cuantificarea fluorimetrică a ADN	Kitul permite cuantificarea fluorimetrică a ADN dublu catenar. Compatibil cu sistemul de cuantificare fluorimetrică Qubit, produs de ThermoFisher Scientific. Spectrul de excitație și emisie a fluorescenței: 510/527. Limita de cuantificare ADN cuprinsă între 4 - 2000 nanograme. Kitul include tamponul de diluție, soluție fluorescentă concentrată, standarde de cantitate. Kit pentru 100 de reacții.	kit	13
39	Kit reactivi electroforeză microfluidică a ARN	Kit pentru analiza prin electroforeză microfluidică a ARN compatibil cu sistemul Bioanlyzer 2100 aflat în dotarea laboratorului.\r\nPermite analiza și cuantificarea ARN total și ARN mesager cu concentrații de 25 - 500 ng/µL.\r\nKitul include 25 chipuri microfluidice, care pot fi utilizate pentru analiza a 300 probe.\r\nPermite analiza integrității ARN extras și calculează parametrul RIN (RNA Integrity Number).\r\nInclude toți reactivii necesari (gel de migrare, fluorocrom, tampon de migrare, markeri de masă moleculară, etc).	kit	9
33	Kit de extracție ARN total din sânge compatibil cu sistemul QiaSymphony	Reactivi și consumabile pentru extracția automată a ARN compatibili cu sistemul  QiaSymphony din dotarea laboratorului.\r\nPermite extracția ARN din sânge integral recoltat în tuburi cu soluție de conservare a ARN (PAXgene Blood RNA Tubes sau echivalent).\r\nPrincipiul de funcționare: purificare magnetică.\r\nKitul include toți reactivii necesari extracției (tampoane de legare, de spălare, de eluție ADN, proteinază K, DNAză).\r\nReactivii sunt ambalați într-un cartuș care se încarcă direct în sistemul de extracție.\r\nUn kit conține reactivi suficienți pentru prelucrarea a 96 probe.\r\nMarcă CE-IVD	kit	7
47	Capilare pentru electroforeză	Set 8 capilare pentru electroforeza ADN. Capilarele sunt compatibile cu sistemul GenomeLab GeXP aflat în dotarea laboratorului.\r\nCapilarele au diametrul intern 75 microni și lungimea 33 cm.\r\nKitul include adaptorul pentru instalare rapidă.	buc	15
53	Kit pentru testarea mutațiilor genelor BRCA1 și BRCA2	Kit de reactivi care permit testarea variantelor genetice somatice și germinale ale genelor BRCA1 și BRCA2. Reactivii permit identificarea variantelor genomice scurte și a numărului de copii. Metodă bazată pe amplificarea țintită a regiunilor genomice de interes. Reactivii permit utilizarea ADN extras din sânge sau din țesuturi. Reactivi cu marcaj CE-IVD pentru utilizarea pe sistemele de secvențiere bazate pe nanopori, cu capacitatea de a secvenția fragmente lungi de ADN. Kitul include reactivii necesari pentru amplificare, pentru multiplexare și adaptorii necesari pentru secvențiere. Kit pentru 16 teste.	kit	6
54	Kit pentru testarea mutațiilor genei CFTR	Kit de reactivi care permit testarea variantelor genetice germinale ale genei CFTR. Reactivii permit identificarea variantelor genomice scurte și a numărului de copii. Metodă bazată pe amplificarea țintită a regiunilor genomice de interes. Reactivii permit utilizarea ADN extras din sânge sau din țesuturi. Reactivi cu marcaj CE-IVD pentru utilizarea pe sistemele de secvențiere bazate pe nanopori, cu capacitatea de a secvenția fragmente lungi de ADN. Kitul include reactivii necesari pentru amplificare, pentru multiplexare și adaptorii necesari pentru secvențiere. Kit pentru 16 teste.	kit	6
55	Kit pentru testarea mutațiilor oncogenelor implicate în mai multe tipuri de cancer	Kit de reactivi care permit testarea variantelor genetice germinale și somatice ale unui număr de peste 40 gene asociate diferitelor forme de cancer: de sân, de ovar, colorectal ereditar. Panelul testează cel puțin următoarele gene: APC, BRCA 1 și 2, EPCAM, MLH1, MSH2, MSH6, PIK3CA, PMS2. Reactivii permit identificarea variantelor genomice scurte și a numărului de copii. Metodă bazată pe captura prin hibridizare a regiunilor genomice de interes. Reactivii permit utilizarea ADN extras din sânge sau din țesuturi (proaspete, congelate sau fixate). Reactivi cu marcaj CE-IVD pentru utilizarea pe sistemele de secvențiere bazate pe nanopori, cu capacitatea de a secvenția fragmente lungi de ADN. Kitul include reactivii necesari pentru captură, pentru multiplexare și adaptorii necesari pentru secvențiere. Kitul este însoțit de un program de analiză a datelor care permite analiza calității datelor, identificarea variantelor (SNV și CNV), clasificarea acestora și redactarea unui raport de analiză. Kit pentru 16 teste.	kit	6
56	Kit pentru secvențierea întregului exom	Kit de reactivi care permit analiza majorității (>99%, >22.000 gene) regiunilor codante din genomul uman. Regiunile genomice analizate însumează peste 40 Mbaze. Reactivii permit identificarea variantelor genomice de secvență și a numărului de copii. Metodă bazată pe captura prin hibridizare a regiunilor genomice de interes. Reactivii permit utilizarea ADN extras din sânge sau din țesuturi (proaspete, congelate sau fixate). Reactivi cu marcaj CE-IVD pentru utilizarea pe sistemele de secvențiere bazate pe nanopori, cu capacitatea de a secvenția fragmente lungi de ADN. Kitul include reactivii necesari pentru captură, pentru multiplexare și adaptorii necesari pentru secvențiere. Kitul este însoțit de un program de analiză a datelor care permite analiza calității datelor, identificarea variantelor (SNV și CNV), clasificarea acestora și redactarea unui raport de analiză. Kit pentru 16 teste.	kit	6
57	Kit pentru diagnosticul afecțiunilor cardiace	Kit de reactivi care permit analiza genelor implicate în cardiomiopatii, aritmii. multe gene. niste boli.	kit	6
59	Kit reactivi suplimentari pentru analiza MS-MLPA	Reactivi necesari realizării reacției MS-MLPA cu amestecul de sonde nucleotidice descris la poziția 1.\nReactivii sunt compatibili cu sistemul de electroforeză capilară Beckman Coulter GeXP din dotarea laboratorului.\nKitul conține: tampoane de reacție, enzimele necesare ligării, mix de primeri cuplați cu fluorocromul Cy5, polimerază ADN termostabilă.\nReactivi suficienți pentru 100 de reacții.	kit	2
61	ADN polimerază pentru amplificarea fragmentelor lungi de ADN	Amestec de ADN polimeraze recombinante ce permit amplificarea unor fragmente de ADN de până la 30 kbaze.\nFidelitate de 2 ori mai mare decât a polimerazei Taq.\nCu activitate de 3-5 și 5-3 exonuclează.\nPolimerază de tip hot-start, ce utilizează un aptamer pentru blocare la temperaturi sub 45˚C.\nReactivul furnizat sub forma unui amestec gata de utilizare, cu concentrația 2X.\nReactiv pentru 100 reacții cu volum final de 50 µL.	buc	14
48	Gel pentru electroforeză	Gel de înaltă rezoluție din poliacrilamidă pentru electroforeza ADN.\r\nGelul este împachetat în cartușe de 20 mL ce pot fi folosite direct pe sistemul de secvențiere GenomeLab GeXP, aflat în dotarea laboratorului.	buc	15
50	Kit standarde de dimensiuni fragmente ADN 420 nucleotide	Kit standarde de dimensiuni ale fragmentelor de ADN, compatibil cu sistemul GenomeLab GeXP.\r\nReactivul conține fragmente ADN cu lungimi cuprinse între 60 si 420 nucleotide, marcate fluorescent cu WellRED.\r\nKit pentru 96 reactii.	kit	15
49	Kit standarde de dimensiuni fragmente ADN 640 nucleotide	Kit standarde de dimensiuni ale fragmentelor de ADN, compatibil cu sistemul GenomeLab GeXP.\r\nReactivul conține fragmente ADN cu lungimi cuprinse între 60 si 640 nucleotide, marcate fluorescent cu WellRED.\r\nKit pentru 96 reactii.	kit	15
52	Soluție pentru încărcarea probelor în capilare	Soluție salină pentru diluarea și denaturarea probelor de ADN.\r\nPermite încărcarea fragmentelor de ADN în capilare.\r\nCompatibilă cu sistemul GenomeLab GeXP aflat în dotarea laboratorului.\r\nFlacon cu 6 mL.	flacon	15
51	Soluție tampon pentru separare	Soluție tampon pentru separarea electroforetică a fragmentelor de ADN, compatibilă cu sistemul GenomeLab GeXP.\r\nPermite migrarea fragmentelor de ADN în matricea de gel.\r\nKitul conține 120 mL soluție.	kit	15
60	Enzimă de restricție HhaI	Reactiv ce conține enzima Hha I, endonuclează dependentă de metilare.\r\nSe utilizează împreună cu amestecul de oligonucleotide pentru analiza metilării în sindromul Lynch prin metoda MS-MLPA și cu kitul de reactivi suplimentari pentru analiza MS-MLPA.\r\nPentru diagnostic in vitro.	buc	2
62	Kit de enzime pentru repararea capetelor fragmentelor de ADN și pentru adăugarea de adenozină la capătul 3	Kitul include un amestec enzimatic (diferite ADN polimeraze) care repară capetele fragmentelor de ADN rezultate în urma amplificării PCR.\nAmestecul include și o enzimă ce adaugă o adenozină fosforilată în 5’ la capătul 3’ al fragmentelor de ADN rezultate.\nKitul include și tamponul optimizat pentru desfășurarea reacțiilor.\nReactivi pentru prepararea bibliotecilor de fragmente în vederea secvențierii prin metoda nanoporilor.\nReactivi suficienți pentru 24 de reacții cu volum final de 60 µL.	kit	14
63	Kit pentru ligarea rapidă a adaptorilor de secvențiere	Kitul include o ligază ADN T4 cu acțiune rapidă pentru ligarea adaptorilor necesari secvențierii.\nKitul include tamponul de reacție optimizat, în concentrație 5X.\nReactivi pentru prepararea bibliotecilor de fragmente în vederea secvențierii prin metoda nanoporilor.\nReactivi suficienți pentru 20 reacții de ligare.	kit	14
64	Kit pentru ligarea etichetelor oligonucleotidice	Kitul include ADN ligaza T4 în tampon gata de întrebuințare.\nUtilizat pentru legarea etichetelor oligonucleotidice de fragmentele de ADN din probe diferite.\nInclude un reactiv de îmbunătățire a activității enzimatice.\nPermite ligarea fragmentelor de ADN cu capete drepte sau cu capete inegale (ligare TA).\nReactivi pentru prepararea bibliotecilor de fragmente în vederea secvențierii prin metoda nanoporilor.\nReactiv suficient pentru 50 reacții de ligare în volum de 5µL / reacție.	kit	14
65	Reactiv pentru repararea ADN din probe fixate și incluse	Amestec enzimatic ce permite repararea ADN din probe fixate cu formol și incluse în parafină.\nPermite repararea citozinelor deaminate, a rupturilor ADN, a bazelor oxidate.\nAmestec gata de întrebuințare.\nReactivi pentru prepararea bibliotecilor de fragmente în vederea secvențierii prin metoda nanoporilor.\nReactiv suficient pentru 24 reacții.	buc	14
66	Kit de reactivi auxiliari de preparare a probelor pentru secvențierea prin metoda nanoporilor	Kit care conține mai mulți reactivi utilizați pentru prepararea probelor în vederea secvențierii prin metoda nanoporilor.\nRecomandat de producător pentru bibliotecile de fragmente obținute prin reacții de ligare, permite citirea secvențelor de ADN cu precizie mare (Q20+).\nInclude următorii reactivi:\nAmestec de reparare ADN din probe fixate și incluse la parafină și tamponul de reacție aferent\nEnzime pentru repararea capetelor fragmentelor de ADN și pentru adăugarea de adenozină la capătul 3’ și tamponul de reacție aferent\nLigază DNA T4 cu acțiune rapidă\nReactivi suficienți pentru 24 de reacții în volumele recomandate.	kit	14
67	Kit pentru amplificare qPCR și detecție pe baza hidrolizei sondelor fluorescente	Kitul conține un amestec de reacție ce permite amplificarea PCR și detecția produșilor de reacție pe baza hidrolizei sondelor oligonucleotidice cuplate cu fluorocromi.\nInclude Taq polimerază de tip hot-start.\nNu conține ROX.\nConține dUTP în amestecul de reacție pentru a preveni contaminarea.\nConține un colorant vizibil pentru a reduce erorile de pipetare.\nFormulat ca amestec 2X ce include toate componentele necesare reacției.\nKit pentru 200 reacții.	kit	14
68	Kit amestec ezimatic pentru reverstranscriere și amplificare simultană qPCR	Kitul permite desfășurarea reacțiilor de reverstranscriere și de amplificare qPCR într-un singur pas.\nDetecția se realizează pe baza hidrolizei sondelor oligonucleotidice cuplate cu fluorocromi.\nInclude o reverstranscriptază care devine activă la temperaturi mai mari decât temperatura camerei. Reverstranscriptaza funcționează la temperaturi de 55-60˚C.\nInclude Taq polimerază de tip hot-start.\nNu conține ROX.\nConține dUTP în amestecul de reacție pentru a preveni contaminarea.\nConține un colorant vizibil pentru a reduce erorile de pipetare.\nKit pentru 200 reacții.	kit	14
69	Kit pentru amplificare qPCR și detecție cu fluorocrom legat nespecific	Kitul conține un amestec de reacție ce permite amplificarea PCR și detecția produșilor de reacție pe baza legării unui fluorocrom la moleculele de ADN dublu-catenar, fără specificitate de secvență.\nInclude Taq polimerază de tip hot-start.\nNu conține ROX.\nConține dUTP în amestecul de reacție pentru a preveni contaminarea.\nConține un colorant vizibil pentru a reduce erorile de pipetare.\nFormulat ca amestec 2X ce include toate componentele necesare reacției.\nKit pentru 200 reacții.	kit	14
70	ADN-polimerază de înaltă fidelitate, tip hot-start	Kit cu polimerază optimizată, de înaltă fidelitate, cu activitate rapidă.\nRata de eroare la incorporarea bazelor de peste 250 ori mai mică decât cea a polimerazei Taq clasice.\nEnzimă de tip hot-start.\nEficiență sporită pentru regiunile bogate în GC.\nInclude enzima, cantitate totală 100U.\nInclude tampon de reacție optimizat, cu concentrația finală de 2mM Mg++.\nInclude separat tampon optimizat pentru amplificarea regiunilor genomice bogate în GC.\nKit pentru 100 reacții la 1U polimerază/reacție.	kit	14
71	Kit pentru reverstranscriere, include primeri	Conține un amestec de reacție ce include reverstranscriptază, inhibitor de RNAze și amestecul dNTP.\nReverstranscriptază cu viteză mare de reacție, necesită un timp de incubare de cel mult 15min la 55˚C.\nInclude primeri oligo-dT și hexameri cu secvență aleatorie.\nConține un colorant vizibil pentru a reduce erorile de pipetare.\nInclude amestec de control noRT.\nKit pentru 25 reacții.	kit	14
72	Kit pentru reverstranscriere, nu include primeri	Conține un amestec de reacție ce include reverstranscriptază, inhibitor de RNAze și amestecul dNTP.\nReverstranscriptază cu viteză mare de reacție, necesită un timp de incubare de cel mult 15min la 55˚C.\nNu include primeri în amestecul de reacție.\nConține un colorant vizibil pentru a reduce erorile de pipetare.\nInclude amestec de control noRT.\nKit pentru 25 reacții.	kit	14
73	ADN-polimerază hot-start	Kitul include ADN-polimerază tip hot-start.\nInclude un aptamer pentru blocare la temperaturi sub 45˚C.\nInclude tampon standard pentru amplificare, concentrație 10X.\nConține 200 U polimerază.	kit	14
74	Kit reactivi pentru testarea riscului genetic de trombofilie	Permite depistarea simultană a cel puțin următoarelor variante genetice: Factor V G1691A (Leiden), Factor V H1299R (R2), Protrombină G20210A, MTHFR C677T, MTHFR A1298C, Factor XIII V34L, PAI-1 4G/5G, EPCR A4600G, EPCR G4678C.\nTest bazat pe amplificarea ADN genomic din regiunile de interes şi hibridizarea\nprodusului de amplificare pe membrane, urmată de o reacție de culoare pentru evidențierea hibridizării.\nHibridizarea se realizează pe suport solid (benzi de hârtie).\nInclude pe fiecare test un control de reacție.\nConține amestecul pentru amplificarea PCR, cu excepția polimerazei.\nConține benzile de hârtie pentru hibridizarea produșilor de amplificare.\nConține reactivii necesari hibridizării (tampon de hibridizare, soluții de spălare, conjugat, substrat colorant) gata de întrebuințare.\nTimp de lucru total maxim 8 ore.\nCompatibil cu sistemul de hibridizare automată BeeBlot 20, existent în dotarea\nlaboratorului.\nMarcaj CE IVD	kit	11
75	Kit detecție și cuantificare infecții EBV, CMV, HHV6	Kit RT-PCR multiplex hot-start care permite screening-ul si evaluarea cantitativă simultană pentru infecțiile virale cu virusurile EBV, CMV și Herpes simplex 6 (HHV6).\nPermite analiza ADN extras din probe clinice de sânge integral, lichid cefalorahidian.\nKit-ul detectează gena umană pentru beta-globină pentru controlul intern.\nDeterminarea cantitativă se face prin raportarea la numărul de copii de control intern.\nKit-ul include reactivi pentru controlul pozitiv de extracție și standarde cu diferite concentrații.\nKit certificat CE-IVD.\nCompatibil cu sistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului.\nFormă de ambalare: kit pentru cel puțin 96 de reacții	kit	4
76	Kit detecție și cuantificare infecție HHV7	Kit RT-PCT pentru screening-ul și evaluarea cantitativă a infecției cu virusul Herpes simplex 7 (HHV7).\nPermite analiza ADN extras din probe clinice de plasmă, sânge integral, salivă, exsudat nazo-faringian, lichid cefalorahidian.\nKit-ul detectează gena umană pentru beta-globină pentru controlul intern.\nDeterminarea cantitativă se face prin raportarea la numărul de copii dintr-un material de control exogen inclus în kit.\nInclude un control pentru verificarea corectitudinii extracției ADN.\nKit-ul include standarde cu diferite concentrații.\nKit certificat CE-IVD.\nCompatibil cu sistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului.\nFormă de ambalare: kit pentru cel puțin 96 de reacții	kit	4
77	Kit detecție și cuantificare infecție Parvovirus B19	Kit RT-PCT hot-start pentru screening-ul și evaluarea cantitativă a infecției cu parvovirus B19.\nPermite analiza ADN extras din probe clinice de plasmă, sânge periferic integral, salivă, exsudat nazo-faringian, lichid cefalorahidian, biopsie osteo-medulară.\nDeterminarea cantitativă se face prin calcularea numărului de copii raportat la numărul de copii de control intern.\nKit-ul conține și reactivi pentru controlul corectitudinii extracției ADN.\nKit-ul include standarde cu diferite concentrații.\nKit certificat CE-IVD.\nCompatibil cu sistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului.\nFormă de ambalare: kit pentru cel puțin 48 de reacții	kit	4
78	Kit pentru testarea cantitativă a produsului genei de fuziune bcr-abl prin PCR digital	Reactivi și consumabile pentru detecția cantitativă cel puțin a variantei majore (e13a2 și e14a2) a genei de fuziune BCR-ABL1.\nPrincipiul metodei: reacție PCR cu sonde fluorescente cu partiționarea volumului de reacție într-un număr mare (peste 15.000) de compartimente individuale.\nMetoda nu necesită analiza unei curbe de diluții standard.\nTimpul de lucru (excluzând extracția ARN): maxim 2h.\nTestul trebuie să permită utilizarea ca probe biologice a sângelui periferic recoltat pe un mediu de stabilizare a ARN.\nSistemul de analiză generază un raport al testului cu rezultatul cantitativ exprimat în unități IS și în răspuns molecular (MR).\nSensibilitatea testului: minim 0,003% IS (MR 4,52) sau mai bună.\nKitul include reactivii consumabilele necesare (de exemplu cartușe de reacție).\nSistem cu marcaj CE-IVD.\nFurnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nÎn cazul în care sunt necesare programe de calculator dedicate analizei și interpretării rezultatelor, acestea vor fi oferite împreună cu reactivii.\nLa evaluarea ofertelor se va lua în considerare prețul per test la care este oferit produsul (1 test reprezintă analiza unei probe biologice)	kit	18
79	Kit pentru testarea cantitativă a produsului genei de fuziune PML-RARA	Reactivi pentru analiza cantitativă a produsului genei de fuziune PML-RARA (formele BCR1 și BCR2) prin real-time qPCR.\nReactivii trebuie să fie compatibili cu sistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului, în caz contrar, furnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD	kit	3
80	Kit pentru testarea calitativă a mutației JAK2 V617F	Reactivi pentru analiza calitativă a mutației JAK2 V617F prin real-time qPCR.\nReactivii trebuie să fie compatibili cu rsistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului, în caz contrar, furnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD	kit	3
81	Kit pentru testarea calitativă a mutației MPL V515K / L	Reactivi pentru analiza calitativă a mutației MPL V515K / L prin real-time qPCR.\nReactivii trebuie să fie compatibili cu rsistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului, în caz contrar, furnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD	kit	3
82	Kit pentru testarea calitativă a mutațiilor CALR tip 1 și 2	Reactivi pentru analiza calitativă a mutațiilor CALR tip 1 și 2 prin real-time qPCR.\nReactivii trebuie să fie compatibili cu rsistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului, în caz contrar, furnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD	kit	3
83	Kit pentru testarea calitativă a mutațiilor IDH1 și IDH2	Reactivi pentru analiza calitativă a mutațiilor IDH1 (aminoacizii 132 și 100) și IDH2 (aminoacizii 172 și 140) prin real-time qPCR.\nReactivii trebuie să fie compatibili cu rsistemele real-time PCR Bio-Rad CFX96 sau Roche LightCycler 480 II din dotarea laboratorului, în caz contrar, furnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD	kit	3
84	Kit pentru testarea calitativă a mutațiilor EGFR	Kitul include reactivii și consumabilele necesare pentru detecrarea a cel puțin 50 mutații în exonii 18-21 ai EGFR.\nMetoda este destinată analizei țesuturilor fixate și incluse în parafină.\nMetoda permite realizarea automată a tuturor pașilor procedurali: deparafinare, extracție acizi nucleici, amplificare, detecție, elaborarea raportului de analiză.\nFurnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD.\nLa evaluarea ofertelor se va lua în considerare prețul per test la care este oferit produsul (1 test reprezintă analiza unei probe de țesut)	kit	8
85	Kit pentru testarea mutațiilor KRAS	Kitul include reactivii și consumabilele necesare pentru detecrarea a cel puțin 20 mutații în exonii 2-4 ai KRAS.\nMetoda este destinată analizei țesuturilor fixate și incluse în parafină.\nMetoda permite realizarea automată a tuturor pașilor procedurali: deparafinare, extracție acizi nucleici, amplificare, detecție, elaborarea raportului de analiză.\nFurnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD.\nLa evaluarea ofertelor se va lua în considerare prețul per test la care este oferit produsul (1 test reprezintă analiza unei probe de țesut)	kit	8
86	Kit pentru testarea mutațiilor NRAS și BRAF	Kitul include reactivii și consumabilele necesare pentru detecrarea a cel puțin 15 mutații în exonii 2-4 ai NRAS și a cel puțin 5 mutații în codonul 600 al BRAF.\nMetoda este destinată analizei țesuturilor fixate și incluse în parafină.\nMetoda permite realizarea automată a tuturor pașilor procedurali: deparafinare, extracție acizi nucleici, amplificare, detecție, elaborarea raportului de analiză.\nFurnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD.\nLa evaluarea ofertelor se va lua în considerare prețul per test la care este oferit produsul (1 test reprezintă analiza unei probe de țesut)	kit	8
87	Kit pentru testarea mutațiilor BRAF	Kitul include reactivii și consumabilele necesare pentru detecrarea a cel puțin 5 mutații în codonul 600 al BRAF.\nMetoda este destinată analizei țesuturilor fixate și incluse în parafină.\nMetoda permite realizarea automată a tuturor pașilor procedurali: deparafinare, extracție acizi nucleici, amplificare, detecție, elaborarea raportului de analiză.\nFurnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD.\nLa evaluarea ofertelor se va lua în considerare prețul per test la care este oferit produsul (1 test reprezintă analiza unei probe de țesut)	kit	8
88	Kit pentru testarea fuziunilor genelor ALK, ROS1 și RET	Kitul include reactivii și consumabilele necesare pentru detecrarea produșilor de transcriere ai genelor de fuziune ce implică ALK, ROS1 și RET.\nDe asemenea, ktiul permite detectarea fuziunilor cu parteneri necunoscuți prin analiza dezechilibrului dintre expresia capetelor 5' și 3' ale genelor.\nMetoda este destinată analizei țesuturilor fixate și incluse în parafină.\nMetoda permite realizarea automată a tuturor pașilor procedurali: deparafinare, extracție acizi nucleici, amplificare, detecție, elaborarea raportului de analiză.\nFurnizorul trebuie să pună la dispoziția Autorității Contractante un echipament compatibil cu testele descrise, pe toată perioada de valabilitate a contractelor subsecvente.\nKit cu marcaj CE-IVD.\nLa evaluarea ofertelor se va lua în considerare prețul per test la care este oferit produsul (1 test reprezintă analiza unei probe de țesut)	kit	8
89	Kit pentru secvențierea țintită a ADN și ARN din hemopatii maligne mieloide	Reactivii permit diagnosticul neoplaziilor mieloide maligne prin secvențiere țintită de nouă generație.\nKitul permite amplificarea prin PCR a cel puțin următoarelor regiuni genomice de interes:\nregiuni predispuse la mutații din genele ABL1, BRAF, CBL, CSF3R, DNMT3A, FLT3, GATA2, HRAS, IDH1, IDH2, JAK2, KIT, KRAS, MPL, MYD88, NPM1, NRAS, PTPN11, SETBP1, SF3B1, SRSF2, U2AF1 și WT1\nîntreaga regiune codantă a genelor ASXL1, BCOR, CALR, CEBPA, ETV6, EZH2, IKZF1, NF1, PHF6, PRPF8, RB1, RUNX1, SH2B3, STAG2, TET2, TP53 și  ZRSR2\neventualele inserții în regiunea genei FLT3 (FLT3-ITD)\nSimultan, reactivii permit analiza ARNm prin amplificare PCR după reverstranscriere a cel puțin următoarelor specii de ARN:\nARNm rezultat frecvent în urma unor evenimente de fuziune ale genelor ABL1, ALK, BCL2, BRAF, CCND1, CREBBP, EGFR, ETV6, FGFR1, FGFR2, FUS, HMGA2, JAK2, KMT2A (MLL), MECOM, MET, MLLT10, MLLT3, MYBL1, MYH11, NTRK3, NUP214, PDGFRA, PDGFRB, RARA, RBM15, RUNX1, TCF3 și TFE3\nExpresia genelor BAALC, MECOM, MYC, SMC1A și WT1 prin comparație cu un set de gene de referință.\nReactivii includ două amestecuri de primeri specifici pentru amplificarea ADN și un amestec de primeri specifici pentru amplificarea ARN după reverstranscriere.\nReacțiile de amplificare pornesc de la cantități minime de cel mult 10 ng ADN și ARN.\nKitul include reactivii necesari preparării bibliotecilor de fragmente (amplificarea ADN sau ADNc, digestia parțială a ampliconilor, ligarea adaptorilor, indexarea fragmentelor) ambalați sub forma unor cartușe de unică folosință ce permit prelucrarea a 4 probe în paralel (8 cartușe / kit).\nKitul include tampoanele necesare preparării bibliotecilor de fragmente ambalate sub forma unor cartușe de unică folosință ce permit prelucrarea a 4 probe în paralel (8 cartușe / kit).\nKitul include reactivii necesari pentru purificarea magnetică a bibliotecilor de fragmente.\nKitul include consumabilele necesare preparării bibliotecilor de fragmente, de unică folosință: vârfuri de pipetare, dispozitive pentru fixarea plăcilor PCR, cartușe de reacție din plastic pentru purificarea magnetică.\nKitul include 4 plăci PCR ce conțin câte 8 perechi de etichete moleculare distincte, necesare pentru indexarea a 32 de probe.\nKitul include programul necesar pentru analiza informatică și generarea raportului de analiză pentru 32 de probe	kit	1
90	Kit reactivi pentru inițializarea echipamentelor și pentru pregatirea automată a probelor, 8 rulări / kit	Kit ce permite pregătirea robustă și automatizată a șabloanelor (templating)  pentru secvențiere.\nKitul conține cartușe de șabloane (templating) și reactivi de secvențiere de unică folosință preambalate, cu urmărire integrată a probelor, oferind un flux de lucru automatizat pentru secvențiere, cu trasabilitate completă a protocolului.\nKitul trebuie să permită rularea a 8 reacții de secvențiere.\nCompatibil cu chipuride diferite capacități	kit	1
91	Kit cu chipuri pentru reactia de secvențiere, 8 chipuri/kit	Pachet de chipuri cu cod de bare pentru secvențierea bibliotecilor de fragmente.\nChipul poate să detecteaze electronic încorporarea bazei azotate sub acțiunea ADN-polimerazei, fără a utiliza fluorescența.\nChipul trebuie să permită un număr citirea unui număr de 15-20 milioane fragmente de ADN.\nPermite citirea unor fragmente cu lungimea de până la 400-600 baze.\nÎmpachetare: 8 chipuri / kit	kit	1
92	Reactivi pentru reacția de revertranscriere a ARN cu reverstranscriptază de tip SuperScript IV, 50 reactii	Master mix conceput pentru sinteza rapidă, sensibilă și reproductibilă a ADN complementar.\nReacție de reverse transcriere în doar 10 minute.\nAmestec convenabil de reacție cDNA cu un singur tub pentru master mix de reacție cDNA pentru RT-qPCR.\nReacție eficientă chiar și cu cantități mici de probă și de puritate suboptimală.\nInclude reactivul pentru eliminarea ADN genomic (DNază) în doar două minute.\nÎmpachetarea: 50 de reacții	kit	1
94	Tampon de liză ATL, 4 x 50 ml	Tampon de liză a probei biologice recomandat de producător pentru a fi utilizat cu kitul de extracție automată a ADN din sânge și țesuturi compatibil cu sistemul QiaSymphony.\r\nTamponul este recomandat de producător pentru a fi utilizat cu sistemul automat QIAsymphony din dotarea labpratorului.\r\nAmbalare: 4 flacoane a câte 50 mL	buc	7
96	Kit extracție ARN din țesuturi incluse la parafină, kit pentru 192 reacții	Reactivi și consumabile pentru extracția automată a ARN, compatibili cu sistemul  QiaSymphony din dotarea laboratorului.\nPermite extracția automată a ARN total (inclusiv molecule mici de ARN) din țesuturi fixate și incluse în parafină și din alte tipuri de probe biologice.\nPermite extracția din secțiuni la parafină cu grosimea de 5-10 µm.\nARN extras poate fi utilizat pentru real-tipe PCR, secvențiere.\nPermite volume de eluție de 50-200 µL.\nPrincipiul de funcționare: purificare magnetică.\nKitul include reactivii necesari extracției (particule magnetice, tampoane de legare, de spălare, de eluție ARN, etc).\nReactivii sunt ambalați într-un cartuș care poate fi păstrat la temperatura camerei și se încarcă direct în sistemul de extracție.\nUn kit conține reactivi suficienți pentru prelucrarea a 192 probe	kit	7
98	Soluție proteinază K, 2 mL	Soluție >600 mAU/mL, volum 2 mL.\nProteinaza K are specificitate de substrat largă și activitate înaltă.\nProteinaza K este stabilă și activă la pH crescut, în prezența de agenți denaturanți puternici (uree, guanidină), sau în prezența SDS.\nEnzima poate fi inactivată prin incubarea 15 min. la 70°C.\nRecomandată de producător pentru utilizare în combinație cu kitul de extracție automată ARN	buc	7
101	Kit extracție ADN din plasmă, kit pentru 96 reacții	Reactivi și consumabile pentru extracția automată a ADN compatibili cu sistemul  QiaSymphony din dotarea laboratorului.\nPermite extracția ADN liber circulant din plasmă.\nPermite prelucrarea a 96 de probe plasmă, fiecare cu volumul de 2 mL.\nPrincipiul de funcționare: purificare magnetică.\nADN extras poate fi utilizat ulterior pentru secvențiere, real-time PCR, PCR digital.\nKitul include reactivii necesari extracției (particule magnetice, tampoane de legare, de spălare, de eluție ADN, proteinază K).\nReactivii sunt ambalați într-un cartuș care poate fi păstrat la temperatura camerei și se încarcă direct în sistemul de extracție.\nUn kit conține reactivi suficienți pentru prelucrarea a 192 probe	kit	7
102	Kit pentru secvențierea țintită a tumorilor, variantă automatizată, kit pentru 32 probe	Kitul permite secvențierea de nouă generație (NGS), țintită, a tumorilor solide, pulmonare și cu alte localizări pentru a detecta variante de secvență atât în ADN cât și în ARN.\nReactivii permit obținerea a două biblioteci de fragmente pentru fiecare probă (ADN și ARN) folosind sistemul automat Ion Chef, pornind de la probe fixate cu formaldehidă și incluse la parafină.\nProdusul permite analiza variantelor punctiforme, a inserțiilor/delețiilor mici, a variantelor de număr de copii și a transcriptelor de fuziune.\nProdusul include: primerii pentru amplificarea a 52 de gene relevante pentru patologia tumorală, cartușe cu reactivi pentru amplificare (enzime, tampon de reacție), cartușe cu soluții pentru amplificare (reactivi pentru purificare magnetică, tampoane de reacție).\nKitul include consumabilele necesare: vârfuri de pipetare, plăci PCR, cartușe pentru purificare.\nKitul include reactivi pentru indexarea probelor, dispuși în plăci PCR cu 96 godeuri.\nAnaliza începe de la 10 ng ARN total și 10 ng ADN.\nBibliotecile de fragmente obținute pot fi secvențiate folosind sistemul IonTorrent S5.\nSecvențele rezultate în urma analizei trebuie să fie compatibile cu programele de analiză primară (identificarea secvenței de baze) și secundară (alinierea la genom de referință, identificarea variantelor) a datelor furnizate de producător.\nOferta trebuie să includă generarea unui număr corespunzător (32) de buletine de analiză detaliate care să cuprindă informații despre semnificația clinică a variantelor identificate, valoarea lor predictivă pentru răspunsul la terapie și eventualele studii clinice curente relevante pentru structura moleculară a tumorilor analizate.\nReactivii și consumabilele sunt suficiente pentru prepararea a 32 de probe (32 biblioteci ADN și 32 de biblioteci ARN) în 4 runde de lucru	kit	1
103	Kit cu celule secvențiere pentru sistemul Ion Gene Studio S5, kit cu 8 celule	Pachet de celule de secvențiere (chipuri) cu cod de bare.\nCelula poate să detecteaze electronic încorporarea bazei de către polimerază fără a utiliza fluorescența.\nCelula trebuie să permită un număr de citiri între 3-6 milioane.\nCelula trebuie să permită  lungimi de citire de până la 400-600 baze.\nSă fie compatibilă cu metodele de pregătire a bibliotecilor și secvențiere folosind instrumentele  Ion Chef și S5	kit	1
104	Kit reactivi pentru reverstranscriere, 32 probe	Reactivi pentru reverstranscriere ARN (prima catenă) optimizați pentru prepararea probelor în vederea secvențierii NGS.\nInclude o reverstranscriptază mutantă tip MMLV.\nKitul permite utilizarea probelor fixate și incluse la parafină.\nInclude un tub cu amestec de reverstranscriere concentrat 10X și un tub cu tampon de reacție concentrat 5x.\nPermite reverstranscrierea rapidă (25 minute) și utilizarea produsului de reacție direct în etapa următoare a preparării probelor folosind reactivii descriși la punctul 1.\nAmbalare: kit pentru 32 probe	kit	1
112	Materiale pentru control extern de calitate - testarea fuziunilor NTRK în cancer	Materiale de control extern de calitate constând în lame cu secțiuni seriate din blocuri la parafină din diferite tipuri de cancer.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului molecular (detecția fuziunilor NTRK prin secvențiere de nouă generație), de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori.\nMaterialele sunt acreditate de către un organism național de acreditare pentru activitatea de testare a competenței laboratoarelor	kit	21
99	Tampon PKD	Tampon de digestie optimizat, recomandat de producător pentru utilizare în combinație cu kitul de extracție ARN din țesuturi incluse la parafină compatibil cu sistemul QiaSymphony din dotarea laboratorului.\r\nAmbalare: flacon cu 15 mL	buc	7
100	Tampon pentru digestia cu dezoxiribonuclează	Tampon concentrat pentru tratamentul probelor cu deoziribonuclează.\r\nTamponul este recomandat de producător pentru utilizare în combinație cu kitul de extracție ARN din țesuturi incluse la parafină compatibil cu sistemul QiaSymphony.\r\nTamponul amplifică efectul enzimatic al deoziribonucleazei	buc	7
105	Kit pentru analiza variantelor EGFR în țesut tumoral, kit pentru 52 reacții	Kit de reactivi cu marcaj CE IVD, validat pentru utilizarea în scop diagnostic folosind unul dintre sistemele existente în laborator: Bio-Rad CFX96 sau Roche LightCycler 480. Validarea trebuie să fie menționată clar în instrucțiunile de utilizare a kitului.\nReactivii sunt utilizați pentru analiza mutațiilor în gena EGFR folosind tehnica real-time PCR în țesut tumoral fixat cu formaldehidă și inclus la parafină.\nAceastă utilizare trebuie să fie menționată specific în instrucțiunile de utilizare a kitului.\nPermite utilizarea a 10 ng ADN / reacție.\nReactivii permit detecția cel puțin a variantelor ce afectează aminoacidul G719 (variante în exonul 18), a delețiilor frecvente din exonul 19, a variantelor ce afectează aminoacizi S768 și T790 (variante în exonul 20), a unor inserții din exonul 20, precum și a variantelor din exonul 21 ce afectează aminoacizii L858 și L861.\nKitul include: amestec de reacție concentrat 2X, amestecuri de amorse și sonde, reactiv de control pozitiv endogen.\nAmorsele și sondele sunt distribuite în 8 amestecuri ce sunt utilizate în paralel, în 8 reacții pentru fiecare probă.\nReacțiile utilizează două canale de fluorescență diferite, unul pentru variantele EGFR și celălalt pentru controlul intern endogen.\nLimita de detecție de 3,5% sau mai bună pentru variantele descrise.\nReactivii din kit permit realizarea a 52 de reacții	kit	8
106	Kit pentru analiza variantelor EGFR în ADN liber circulant, kit pentru 48 reacții	Kit de reactivi cu marcaj CE IVD, recomandat pentru utilizarea în scop diagnostic folosind unul dintre sistemele existente în laborator: Bio-Rad CFX96 sau Roche LightCycler 480. Recomandarea trebuie să fie menționată clar în instrucțiunile de utilizare a kitului.\nReactivii sunt utilizați pentru analiza mutațiilor în gena EGFR folosind tehnica real-time PCR în ADN genomic uman liber circulant în plasmă (cell-free DNA).\nAceastă utilizare trebuie să fie menționată specific în instrucțiunile de utilizare a kitului.\nPermite utilizarea a 1,5 - 15 ng ADN / reacție.\nReactivii permit detecția cel puțin a variantelor ce afectează aminoacidul G719 (variante în exonul 18), a delețiilor frecvente din exonul 19, a variantelor ce afectează aminoacizi S768 și T790 (variante în exonul 20), a unor inserții din exonul 20, precum și a variantelor din exonul 21 ce afectează aminoacizii L858 și L861.\nKitul include: amestec de reacție concentrat 2X, amestecuri de amorse și sonde, reactiv de control pozitiv endogen.\nAmorsele și sondele sunt distribuite în 7 amestecuri ce sunt utilizate în paralel, în 7 reacții pentru fiecare probă.\nReacțiile utilizează cel puțin două canale de fluorescență diferite, unul sau mai multe pentru variantele EGFR și unul pentru controlul intern endogen.\nLimita de detecție: 25 sau mai puține copii mutante T790M.\nReactivii din kit permit realizarea a 48 de reacții	kit	8
107	Materiale pentru control extern de calitate imunohistochimie - proteina de fuziune EML4-ALK în adenocarcinomul pulmonar	Materiale de control extern de calitate constând în lame cu secțiuni seriate dintr-un bloc la parafină ce cuprinde mai multe țesuturi, cel puțin unul dintre acestea fiind un adenocarcinom pulmonar cu translocația EML4-ALK care exprimă proteina de fuziune corespunzătoare.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului de imunohistochimie de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori.\nMaterialele sunt acreditate de către un organism național de acreditare pentru activitatea de testare a competenței laboratoarelor	kit	22
108	Materiale pentru control extern de calitate hibridizare in situ - amplificarea HER2 în carcinomul mamar	Materiale de control extern de calitate constând în lame cu secțiuni seriate dintr-un bloc la parafină ce cuprinde mai multe țesuturi tumorale (carcinom mamar) cu niveluri diferite de amplificare a genei HER2.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului de hibridizare in situ de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori	kit	22
109	Materiale pentru control extern de calitate imunohistochimie - nivelul expresiei PD-L1 în carcinomul pulmonar non-microcelular	Materiale de control extern de calitate constând în lame cu secțiuni seriate dintr-un bloc la parafină ce cuprinde mai multe țesuturi tumorale (carcinom pulmonar non-microcelular) și de control cu niveluri diferite de expresie a PD-L1.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului de imunohistochimie, exprimate sub forma scorului proporției de celule tumorale (TPS), de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori.\nMaterialele sunt acreditate de către un organism național de acreditare pentru activitatea de testare a competenței laboratoarelor	kit	22
110	Materiale pentru control extern de calitate - testarea variantelor EGFR în ADN plasmatic liber circulant	Materiale de control extern de calitate constând în plasmă artificială pentru testarea competenței în analiza variantelor EGFR folosind probe de ADN plasmatic liber circulant.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului molecular de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori.\nMaterialele sunt acreditate de către un organism național de acreditare pentru activitatea de testare a competenței laboratoarelor	kit	21
111	Materiale pentru control extern de calitate - testarea variantelor EGFR în cancerul pulmonar	Materiale de control extern de calitate constând în lame cu secțiuni seriate din blocuri la parafină din carcinom pulmonar.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului molecular (detecția variantelor EGFR), de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori.\nMaterialele sunt acreditate de către un organism național de acreditare pentru activitatea de testare a competenței laboratoarelor	kit	21
113	Materiale pentru control extern de calitate - testarea fuziunilor ALK, ROS1 și MET în cancerul pulmonar	Materiale de control extern de calitate constând în lame cu secțiuni seriate din blocuri la parafină dincancer pulmonar.\nParticipanții se pot înregistra și trimite electronic detalii despre protocolul de lucru și rezultatele obținute.\nProdusul include evaluarea rezultatelor testului molecular (detecția fuziunilor ALK, ROS1 și MET), de către un grup de experți.\nRezultatele detaliate ale evaluării sunt trimise înapoi beneficiarului sub forma unui raport care include și observații și sugestii ale experților evaluatori.\nMaterialele sunt acreditate de către un organism național de acreditare pentru activitatea de testare a competenței laboratoarelor	kit	21
114	Kit reactivi pentru testarea variantelor EGFR , kit pentru 20 reacții	Permite depistarea simultană a cel puțin următoarelor variante genetice: variante din exonul 18 care afectează aminoacidul G719;\nvariante (inclusiv deleții și deleții-inserții) din exonul 19 care afectează unul sau mai mulți dintre aminoacizii K745, E746 și L747;\nvariante din exonul 20 ce conduc la substituția T790M; variante din exonul 21 care afectează L858 și L861.\nTestul poate fi utilizat pentru ADN extras din țesuturi fixate în formaldehidă și incluse la parafină, utilizarea trebuie să fie menționată explicit în instrucțiunile de utilizare a kitului.\nTest bazat pe amplificarea ADN genomic din regiunile de interes şi hibridizarea produsului de amplificare pe membrane, urmată de o reacție de evidențiere a hibridizării.\nInclude pe fiecare test un control de reacție, două controale pozitive și patru controale negative.\nConține amestecul pentru amplificarea PCR inclusiv polimerază Taq.\nConține bandeletele pentru hibridizarea produșilor de amplificare.\nConține reactivii necesari hibridizării (tampoane de denaturare și de hibridizare, soluții de spălare, conjugat și substrat cromogen).\nTimp de lucru total maxim 8 ore.\nCompatibil cu sistemul de hibridizare automată BeeBlot 20, existent în dotarea laboratorului.\nMarcaj CE IVD	kit	11
40	Kit reactivi electroforeză microfluidică a ADN	Kit pentru analiza prin electroforeză microfluidică a ADN compatibil cu sistemul Bioanlyzer 2100 aflat în dotarea laboratorului.\r\nPermite analiza și cuantificarea ADN cu concentrații de 0.5-50 ng/µL.\r\nPermite analiza fragmentelor cu dimensiuni între 50 și 1000 baze.\r\nKitul include 25 chipuri microfluidice, care pot fi utilizate pentru analiza a 300 probe.\r\nInclude toți reactivii necesari (gel de migrare, fluorocrom, tampon de migrare, markeri de masă moleculară, etc).	kit	9
41	Kit reactivi electroforeză microfluidică de mare sensibilitate a ADN	Kit pentru analiza prin electroforeză microfluidică a ADN compatibil cu sistemul Bioanlyzer 2100 aflat în dotarea laboratorului.\r\nPermite analiza și cuantificarea ADN cu concentrații de 5-500 pg/µL.\r\nPermite analiza fragmentelor cu dimensiuni între 50 și 7000 baze.\r\nKitul include 10 chipuri microfluidice, care pot fi utilizate pentru analiza a 110 probe.\r\nInclude toți reactivii necesari (gel de migrare, fluorocrom, tampon de migrare, markeri de masă moleculară, etc).	kit	9
32	Kit de extracție automată a ADN din sânge și țesuturi compatibil cu sistemul QiaSymphony	Reactivi și consumabile pentru extracția automată a ADN compatibili cu sistemul  QiaSymphony din dotarea laboratorului.\r\nPermite extracția ADN din 200 µL de sânge integral, suspensie de leucocite, țesuturi și țesuturi fixate și incluse în parafină.\r\nPrincipiul de funcționare: purificare magnetică.\r\nKitul include toți reactivii necesari extracției (tampoane de legare, de spălare, de eluție ADN, proteinază K).\r\nReactivii sunt ambalați într-un cartuș care poate fi păstrat la temperatura camerei și se încarcă direct în sistemul de extracție.\r\nUn kit conține reactivi suficienți pentru prelucrarea a 192 probe.\r\nMarcă CE-IVD	kit	7
95	Ribonuclează A, flacon cu 2,5 mL	Ribonuclează A cu concentrația de 100 mg/mL, sau 7000 unități/mL, volum 2,5 mL.\r\nRibonuclează A pentru utilizarea în protocolul recomandat de producăor pentru extracția ADN din țesuturi incluse la parafină cu kitul de extracție automată a ADN din sânge și țesuturi compatibil cu sistemul QiaSymphony.\r\nSoluție certificată fără activitate de deoxiribonuclează.\r\nSoluție gata de întrebuințare	buc	7
93	Soluție deparafinare pentru extracția ADN, flacon 50 mL	Soluție de deparafinizare optimizată pentru tratarea secțiunilor la parafină anterior purificării ADN folosind kitul de extracție automată a ADN din sânge și țesuturi compatibil cu sistemul QiaSymphony.\r\nSoluția poate rămâne în contact cu proba biologică și pe parcursul tratamentului cu proteinază K.\r\nNu este necesară îndepărtarea supernatantului înainte de procesarea ulterioară a probei.\r\nConține un colorant albastru inert.\r\nSoluția este recomandată de producător pentru utilizare în combinație cu kitul de extracție ADN specificat la punctul 1.\r\nAmbalare: flacon cu 50 mL	kit	7
97	Soluție deparafinare pentru extracția ARN, 16 mL	Soluție de deparafinare recomandată de producător a fi utilizată pentru extracția și purificarea ARN din țesuturi incluse la parafină folosind kitul extracție ARN din țesuturi incluse la parafină compatibil cu sistemul QiaSymphony din dotarea laboratorului.\r\nSoluția poate rămâne în contact cu proba biologică și pe parcursul tratamentului cu proteinază K.\r\nNu este necesară îndepărtarea supernatantului înainte de procesarea ulterioară a probei.\r\nConține un colorant albastru inert.\r\nSoluția este recomandată de producător pentru utilizare în combinație cu kitul de extracție ARN specificat la punctul 5.\r\nAmbalare: 2 flacoane cu câte 8 mL soluție	buc	7
115	Kit cu reactivi suplimentari pentru hibridizare stripuri, kit pentru 20 de teste	Reactivi auxiliari utilizați în combinație cu kituri de amplificare și hibridizare acizi nucleici pe suport solid.\r\nConține reactivi pentru denaturare, hibridizare, spălare, conjugare și soluție substrat cromogen necesari hibridizării pe stripuri.\r\nCompatibil cu sistemul de hibridizare automată BeeBlot 20, existent în dotarea laboratorului.\r\nMarcaj CE IVD	kit	11
58	Amestec de oligonucleotide pentru analiza metilării în sindromul Lynch prin metoda MS-MLPA	Amestec de oligonucleotide utilizate ca sonde pentru analiza metilării în sindromul Lynch.\r\nReactivii permit analiza prin metoda MS-MLPA (amplificarea multiplex a sondelor oligonucleotidice, dependentă de ligare și specifică pentru metilare).\r\nMetoda analizează statutul metilării regiunilor promoter ale genelor MLH1, MSH2, PMS2 și MSH6, precum și existența mutației BRAF p.V600E.\r\nReacția poate fi utilizată și pentru detecția delețiilor sau duplicațiilor în regiunea 3’ a genei EPCAM sau în regiunile promoterilor genelor  MLH1, MSH2, PMS2 și MSH6.\r\nKitul include și ADN de control.\r\nProdusul este însoțit de o soluție informatică de analiză și interpretare a rezultatelor, inclusă în costul reactivilor.\r\nReactivi pentru diagnostic in vitro.\r\nKit pentru 25 de teste.	buc	2
46	Reactivi pentru analiza prin PCR a instabilității microsateliților ADN	Set de reactivi ce permit amplificarea prin PCR și apoi analiza lungimii unor regiuni genomice ce conțin microsateliți ADN mono- sau multi-nucleotidici.\r\nRegiunile analizate trebie să aibă o variație redusă (cuasi-monomorfice) în populația fără patologie, astfel încât polimorfismele de lungime să poată fi detectate fără a fi necesară analiza unei probe de ADN non-tumoral a pacientului.\r\nSetul trebuie să analizeze cel puțin 4 locusuri genomice.\r\nMetoda permite analiza ADN extras din țesuturi fixate în formol și incluse în parafină.\r\nKitul conține toți reactivii necesari amplificării PCR și detecției fluorescente a polimorfismelor de lungime în regiunile genomice studiate. Metoda de testare să fie validată prin studii care au analizat caracteristicile analitice în populații de pacienți cu diferite tumori maligne (cel puțin cancer colorectal).\r\nÎn cazul în care reactivii nu pot fi utilizați folosind echipamentele aflate în dotarea laboratorului (extracție ADN cu kit CE-IVD, termocicloare Applied Biosciences GeneAmp 9700 și SensoQuest Labcycler, sisteme real-time PCR Bio-Rad CFX 96 și Roche LC480 II, sistem de electroforeză capilară Beckman Coulter GenomeLab GeXP), furnizorul trebuie să pună la dispoziția Autorității Contractante un sistem de analiză compatibil pe toată perioada de valabilitate a contractelor subsecvente.\r\nÎn cazul în care sunt necesare programe de calculator dedicate analizei și interpretării rezultatelor, acestea vor fi oferite împreună cu reactivii.	kit	5
23	Kit pentru prepararea bibliotecilor de secvențiere prin fragmentare enzimatică, multiplex	Reactivi pentru obținerea de biblioteci de fragmente care pot fi secvențiate pe sistemul MiniSeq Illumina, aflat în dotarea laboratorului.\r\nKitul trebuie să fie compatibil cu kitul pentru analiza riscului ereditar de cancer 113 gene.\r\nKitul permite prelucrarea ADN genomic prin fragmentare enzimatică (tagmentare) și adăugarea de secvențe cunoscute la capetele fragmentelor.\r\nMetoda este una rapidă (timp total de lucru aprox. 7 ore)\r\nPermite adăugarea de etichete moleculare unice (indici) la capetele fragmentelor prin reacții PCR.\r\nPermite amplificarea bibliotecilor de fragmente după pasul de selecție prin hibridizare și captură.\r\nKitul conține toți reactivii necesari pentru realizarea pașilor descriși mai sus, mai puțin particulele magnetice pentru purificarea și selecția fragmentelor de ADN.\r\nKit pentru 16 reacții	kit	19
20	Kit de reactivi pentru obținerea ADNc	*NU*\r\nReactivi pentru sinteza lanțului de ADN complementar ARN.\r\nCompatibil cu reactvii de la poziția 5\r\nConține amestecul de reacție și, separat, enzimele necesare.\r\nReactivi suficienți pentru 100 de reacții	kit	19
18	Kit pentru preparearea bibliotecilor de secvențiere prin amplificare, multiplex	*NU*\r\nReactivi pentru prepararea rapidă a bibliotecilor de  fragmente , pornind de la produși de amplificare PCR.\r\nReactivii sunt compatibili cu secvențiatorul Illumina MiniSeq aflat în dotarea laboratorului.\r\nReactivii pot fi utilizați împreună cu kiturile descrise la pozițiile 2 și 3\r\nKitul permite ligarea secvențelor index, purificarea bibliotecii de fragmente și amplificarea fragmentelor.\r\nKitul conține primeri specifici, amestec enzimatic pentru amplificarea probelor, ligază ADN, reactivi pentru amplificarea bibliotecii de fragmente, reactivi pentru adăugarea de secvențe index.\r\nReactivi suficienți pentru 24 de reacții	kit	19
17	Kit reactivi pentru analiza ADN și ARN din tumori solide prin amplificarea regiunilor de interes	*NU* AmpliSeq for Illumina Cancer Hotspot Panel v2\r\nKit pentru analiza prin secvențiere de nouă generație a ADN și ARN din tumori solide.\r\nReactivii sunt compatibili cu secvențiatorul Illumina MiniSeq aflat în dotarea laboratorului.\r\nKitul permite analiza a 52 de oncogene cu rol de biomarker în tumori maligne solide de plâmân, colon, sân, ovar, prostată și melanocitare.\r\nMetoda este bazată pe amplificarea prin PCR multiplex a genelor de interes.\r\nReactivii permit analiza acizilor nucleici extrași din țesuturi fixate și incluse la parafină.\r\nKitul conține amestecul de primeri specifici.\r\nProducătorul furnizează o soluție pentru analiza datelor generate, inclusă în costul reactivilor.\r\nReactivi suficienți pentru analiza a 24 de probe	kit	19
\.


--
-- Data for Name: Produse_In_Loturi; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Produse_In_Loturi" ("ID_Produs_Lot", "ID_Lot", "ID_Produs_Referat") FROM stdin;
\.


--
-- Data for Name: Produse_In_Referate; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Produse_In_Referate" ("ID_Produs_Referat", "ID_Referat", "ID_Produs_Generic", "Cantitate_Solicitata") FROM stdin;
\.


--
-- Data for Name: Referate_Necesitate; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Referate_Necesitate" ("ID_Referat", "Data_Creare", "Stare", "Numar_Referat", "Numar_Inregistrare_Document", "Data_Inregistrare_Document", "Link_Scan_PDF", "ID_Utilizator_Creare", "Observatii", "Observatii_Aprobare") FROM stdin;
\.


--
-- Data for Name: Utilizatori; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Utilizatori" ("ID_Utilizator", "Nume_Utilizator", "Email", "Parola_Hash", "Data_Creare", "Este_Activ") FROM stdin;
1	admin	admin@example.com	scrypt:32768:8:1$e8b3V0NNWlH9unGl$f573506b604757cda45366cba37936e370668531570a256a2cf5e97a36b5ddc5f1d982ccf0d29c3cc1088bd8cb39595c34de41d827f5fff82d550ca3bee66636	2025-11-21	t
\.


--
-- Data for Name: Variante_Comerciale_Produs; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public."Variante_Comerciale_Produs" ("ID_Varianta_Comerciala", "ID_Produs_Generic", "ID_Producator", "Cod_Catalog", "Nume_Comercial_Extins", "Descriere_Ambalare", "Cantitate_Standard_Ambalare") FROM stdin;
\.


--
-- Data for Name: contracte_loturi_procedura_asociere; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public.contracte_loturi_procedura_asociere (contract_id, lot_procedura_id) FROM stdin;
\.


--
-- Data for Name: lot_procedura_articole_asociere; Type: TABLE DATA; Schema: public; Owner: nume_utilizator_pg
--

COPY public.lot_procedura_articole_asociere (lot_procedura_id, produs_referat_id) FROM stdin;
\.


--
-- Name: Articole_Contractate_ID_Articol_Contractat_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Articole_Contractate_ID_Articol_Contractat_seq"', 1, false);


--
-- Name: Articole_Oferta_ID_Articol_Oferta_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Articole_Oferta_ID_Articol_Oferta_seq"', 1, false);


--
-- Name: Categorii_ID_Categorie_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Categorii_ID_Categorie_seq"', 22, true);


--
-- Name: Comanda_General_ID_Comanda_General_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Comanda_General_ID_Comanda_General_seq"', 1, false);


--
-- Name: Contracte_ID_Contract_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Contracte_ID_Contract_seq"', 1, false);


--
-- Name: Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Detalii_Comanda_Produs_ID_Detalii_Comanda_Produs_seq"', 1, false);


--
-- Name: Documente_Livrare_ID_Document_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Documente_Livrare_ID_Document_seq"', 1, false);


--
-- Name: Furnizori_ID_Furnizor_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Furnizori_ID_Furnizor_seq"', 1, false);


--
-- Name: Livrare_Comenzi_ID_Livrare_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Livrare_Comenzi_ID_Livrare_seq"', 1, false);


--
-- Name: Loturi_ID_Lot_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Loturi_ID_Lot_seq"', 1, false);


--
-- Name: Loturi_Procedura_ID_Lot_Procedura_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Loturi_Procedura_ID_Lot_Procedura_seq"', 1, false);


--
-- Name: Oferte_ID_Oferta_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Oferte_ID_Oferta_seq"', 1, false);


--
-- Name: Proceduri_Achizitie_ID_Procedura_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Proceduri_Achizitie_ID_Procedura_seq"', 1, false);


--
-- Name: Producatori_ID_Producator_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Producatori_ID_Producator_seq"', 1, false);


--
-- Name: Produse_ID_Produs_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Produse_ID_Produs_seq"', 115, true);


--
-- Name: Produse_In_Loturi_ID_Produs_Lot_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Produse_In_Loturi_ID_Produs_Lot_seq"', 1, false);


--
-- Name: Produse_In_Referate_ID_Produs_Referat_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Produse_In_Referate_ID_Produs_Referat_seq"', 1, false);


--
-- Name: Referate_Necesitate_ID_Referat_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Referate_Necesitate_ID_Referat_seq"', 1, false);


--
-- Name: Utilizatori_ID_Utilizator_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Utilizatori_ID_Utilizator_seq"', 1, true);


--
-- Name: Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq; Type: SEQUENCE SET; Schema: public; Owner: nume_utilizator_pg
--

SELECT pg_catalog.setval('public."Variante_Comerciale_Produs_ID_Varianta_Comerciala_seq"', 1, false);


--
-- Name: Articole_Contractate Articole_Contractate_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Contractate"
    ADD CONSTRAINT "Articole_Contractate_pkey" PRIMARY KEY ("ID_Articol_Contractat");


--
-- Name: Articole_Oferta Articole_Oferta_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Oferta"
    ADD CONSTRAINT "Articole_Oferta_pkey" PRIMARY KEY ("ID_Articol_Oferta");


--
-- Name: Categorii Categorii_Nume_Categorie_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Categorii"
    ADD CONSTRAINT "Categorii_Nume_Categorie_key" UNIQUE ("Nume_Categorie");


--
-- Name: Categorii Categorii_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Categorii"
    ADD CONSTRAINT "Categorii_pkey" PRIMARY KEY ("ID_Categorie");


--
-- Name: Comanda_General Comanda_General_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Comanda_General"
    ADD CONSTRAINT "Comanda_General_pkey" PRIMARY KEY ("ID_Comanda_General");


--
-- Name: Contracte Contracte_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Contracte"
    ADD CONSTRAINT "Contracte_pkey" PRIMARY KEY ("ID_Contract");


--
-- Name: Detalii_Comanda_Produs Detalii_Comanda_Produs_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Detalii_Comanda_Produs"
    ADD CONSTRAINT "Detalii_Comanda_Produs_pkey" PRIMARY KEY ("ID_Detalii_Comanda_Produs");


--
-- Name: Documente_Livrare Documente_Livrare_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Documente_Livrare"
    ADD CONSTRAINT "Documente_Livrare_pkey" PRIMARY KEY ("ID_Document");


--
-- Name: Furnizori Furnizori_CUI_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Furnizori"
    ADD CONSTRAINT "Furnizori_CUI_key" UNIQUE ("CUI");


--
-- Name: Furnizori Furnizori_Nume_Furnizor_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Furnizori"
    ADD CONSTRAINT "Furnizori_Nume_Furnizor_key" UNIQUE ("Nume_Furnizor");


--
-- Name: Furnizori Furnizori_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Furnizori"
    ADD CONSTRAINT "Furnizori_pkey" PRIMARY KEY ("ID_Furnizor");


--
-- Name: Livrare_Comenzi Livrare_Comenzi_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Livrare_Comenzi"
    ADD CONSTRAINT "Livrare_Comenzi_pkey" PRIMARY KEY ("ID_Livrare");


--
-- Name: Loturi_Procedura Loturi_Procedura_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Loturi_Procedura"
    ADD CONSTRAINT "Loturi_Procedura_pkey" PRIMARY KEY ("ID_Lot_Procedura");


--
-- Name: Loturi Loturi_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Loturi"
    ADD CONSTRAINT "Loturi_pkey" PRIMARY KEY ("ID_Lot");


--
-- Name: Oferte Oferte_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Oferte"
    ADD CONSTRAINT "Oferte_pkey" PRIMARY KEY ("ID_Oferta");


--
-- Name: Proceduri_Achizitie Proceduri_Achizitie_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Proceduri_Achizitie"
    ADD CONSTRAINT "Proceduri_Achizitie_pkey" PRIMARY KEY ("ID_Procedura");


--
-- Name: Producatori Producatori_Nume_Producator_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Producatori"
    ADD CONSTRAINT "Producatori_Nume_Producator_key" UNIQUE ("Nume_Producator");


--
-- Name: Producatori Producatori_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Producatori"
    ADD CONSTRAINT "Producatori_pkey" PRIMARY KEY ("ID_Producator");


--
-- Name: Produse_In_Loturi Produse_In_Loturi_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Loturi"
    ADD CONSTRAINT "Produse_In_Loturi_pkey" PRIMARY KEY ("ID_Produs_Lot");


--
-- Name: Produse_In_Referate Produse_In_Referate_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Referate"
    ADD CONSTRAINT "Produse_In_Referate_pkey" PRIMARY KEY ("ID_Produs_Referat");


--
-- Name: Produse Produse_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse"
    ADD CONSTRAINT "Produse_pkey" PRIMARY KEY ("ID_Produs");


--
-- Name: Referate_Necesitate Referate_Necesitate_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Referate_Necesitate"
    ADD CONSTRAINT "Referate_Necesitate_pkey" PRIMARY KEY ("ID_Referat");


--
-- Name: Utilizatori Utilizatori_Email_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Utilizatori"
    ADD CONSTRAINT "Utilizatori_Email_key" UNIQUE ("Email");


--
-- Name: Utilizatori Utilizatori_Nume_Utilizator_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Utilizatori"
    ADD CONSTRAINT "Utilizatori_Nume_Utilizator_key" UNIQUE ("Nume_Utilizator");


--
-- Name: Utilizatori Utilizatori_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Utilizatori"
    ADD CONSTRAINT "Utilizatori_pkey" PRIMARY KEY ("ID_Utilizator");


--
-- Name: Variante_Comerciale_Produs Variante_Comerciale_Produs_Cod_Catalog_key; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Variante_Comerciale_Produs"
    ADD CONSTRAINT "Variante_Comerciale_Produs_Cod_Catalog_key" UNIQUE ("Cod_Catalog");


--
-- Name: Variante_Comerciale_Produs Variante_Comerciale_Produs_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Variante_Comerciale_Produs"
    ADD CONSTRAINT "Variante_Comerciale_Produs_pkey" PRIMARY KEY ("ID_Varianta_Comerciala");


--
-- Name: Produse_In_Loturi _lot_produs_referat_uc; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Loturi"
    ADD CONSTRAINT _lot_produs_referat_uc UNIQUE ("ID_Lot", "ID_Produs_Referat");


--
-- Name: contracte_loturi_procedura_asociere contracte_loturi_procedura_asociere_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public.contracte_loturi_procedura_asociere
    ADD CONSTRAINT contracte_loturi_procedura_asociere_pkey PRIMARY KEY (contract_id, lot_procedura_id);


--
-- Name: lot_procedura_articole_asociere lot_procedura_articole_asociere_pkey; Type: CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public.lot_procedura_articole_asociere
    ADD CONSTRAINT lot_procedura_articole_asociere_pkey PRIMARY KEY (lot_procedura_id, produs_referat_id);


--
-- Name: Articole_Contractate Articole_Contractate_ID_Contract_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Contractate"
    ADD CONSTRAINT "Articole_Contractate_ID_Contract_fkey" FOREIGN KEY ("ID_Contract") REFERENCES public."Contracte"("ID_Contract");


--
-- Name: Articole_Contractate Articole_Contractate_ID_Produs_Referat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Contractate"
    ADD CONSTRAINT "Articole_Contractate_ID_Produs_Referat_fkey" FOREIGN KEY ("ID_Produs_Referat") REFERENCES public."Produse_In_Referate"("ID_Produs_Referat");


--
-- Name: Articole_Contractate Articole_Contractate_ID_Varianta_Comerciala_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Contractate"
    ADD CONSTRAINT "Articole_Contractate_ID_Varianta_Comerciala_fkey" FOREIGN KEY ("ID_Varianta_Comerciala") REFERENCES public."Variante_Comerciale_Produs"("ID_Varianta_Comerciala");


--
-- Name: Articole_Oferta Articole_Oferta_ID_Lot_Procedura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Oferta"
    ADD CONSTRAINT "Articole_Oferta_ID_Lot_Procedura_fkey" FOREIGN KEY ("ID_Lot_Procedura") REFERENCES public."Loturi_Procedura"("ID_Lot_Procedura");


--
-- Name: Articole_Oferta Articole_Oferta_ID_Oferta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Oferta"
    ADD CONSTRAINT "Articole_Oferta_ID_Oferta_fkey" FOREIGN KEY ("ID_Oferta") REFERENCES public."Oferte"("ID_Oferta");


--
-- Name: Articole_Oferta Articole_Oferta_ID_Produs_Referat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Oferta"
    ADD CONSTRAINT "Articole_Oferta_ID_Produs_Referat_fkey" FOREIGN KEY ("ID_Produs_Referat") REFERENCES public."Produse_In_Referate"("ID_Produs_Referat");


--
-- Name: Articole_Oferta Articole_Oferta_ID_Varianta_Comerciala_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Articole_Oferta"
    ADD CONSTRAINT "Articole_Oferta_ID_Varianta_Comerciala_fkey" FOREIGN KEY ("ID_Varianta_Comerciala") REFERENCES public."Variante_Comerciale_Produs"("ID_Varianta_Comerciala");


--
-- Name: Comanda_General Comanda_General_ID_Contract_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Comanda_General"
    ADD CONSTRAINT "Comanda_General_ID_Contract_fkey" FOREIGN KEY ("ID_Contract") REFERENCES public."Contracte"("ID_Contract");


--
-- Name: Comanda_General Comanda_General_ID_Utilizator_Creare_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Comanda_General"
    ADD CONSTRAINT "Comanda_General_ID_Utilizator_Creare_fkey" FOREIGN KEY ("ID_Utilizator_Creare") REFERENCES public."Utilizatori"("ID_Utilizator");


--
-- Name: Contracte Contracte_ID_Furnizor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Contracte"
    ADD CONSTRAINT "Contracte_ID_Furnizor_fkey" FOREIGN KEY ("ID_Furnizor") REFERENCES public."Furnizori"("ID_Furnizor");


--
-- Name: Contracte Contracte_ID_Procedura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Contracte"
    ADD CONSTRAINT "Contracte_ID_Procedura_fkey" FOREIGN KEY ("ID_Procedura") REFERENCES public."Proceduri_Achizitie"("ID_Procedura");


--
-- Name: Contracte Contracte_ID_Utilizator_Creare_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Contracte"
    ADD CONSTRAINT "Contracte_ID_Utilizator_Creare_fkey" FOREIGN KEY ("ID_Utilizator_Creare") REFERENCES public."Utilizatori"("ID_Utilizator");


--
-- Name: Detalii_Comanda_Produs Detalii_Comanda_Produs_ID_Articol_Contractat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Detalii_Comanda_Produs"
    ADD CONSTRAINT "Detalii_Comanda_Produs_ID_Articol_Contractat_fkey" FOREIGN KEY ("ID_Articol_Contractat") REFERENCES public."Articole_Contractate"("ID_Articol_Contractat");


--
-- Name: Detalii_Comanda_Produs Detalii_Comanda_Produs_ID_Comanda_General_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Detalii_Comanda_Produs"
    ADD CONSTRAINT "Detalii_Comanda_Produs_ID_Comanda_General_fkey" FOREIGN KEY ("ID_Comanda_General") REFERENCES public."Comanda_General"("ID_Comanda_General");


--
-- Name: Documente_Livrare Documente_Livrare_ID_Livrare_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Documente_Livrare"
    ADD CONSTRAINT "Documente_Livrare_ID_Livrare_fkey" FOREIGN KEY ("ID_Livrare") REFERENCES public."Livrare_Comenzi"("ID_Livrare");


--
-- Name: Livrare_Comenzi Livrare_Comenzi_ID_Detalii_Comanda_Produs_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Livrare_Comenzi"
    ADD CONSTRAINT "Livrare_Comenzi_ID_Detalii_Comanda_Produs_fkey" FOREIGN KEY ("ID_Detalii_Comanda_Produs") REFERENCES public."Detalii_Comanda_Produs"("ID_Detalii_Comanda_Produs");


--
-- Name: Livrare_Comenzi Livrare_Comenzi_ID_Utilizator_Inregistrare_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Livrare_Comenzi"
    ADD CONSTRAINT "Livrare_Comenzi_ID_Utilizator_Inregistrare_fkey" FOREIGN KEY ("ID_Utilizator_Inregistrare") REFERENCES public."Utilizatori"("ID_Utilizator");


--
-- Name: Loturi Loturi_ID_Referat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Loturi"
    ADD CONSTRAINT "Loturi_ID_Referat_fkey" FOREIGN KEY ("ID_Referat") REFERENCES public."Referate_Necesitate"("ID_Referat");


--
-- Name: Loturi_Procedura Loturi_Procedura_ID_Procedura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Loturi_Procedura"
    ADD CONSTRAINT "Loturi_Procedura_ID_Procedura_fkey" FOREIGN KEY ("ID_Procedura") REFERENCES public."Proceduri_Achizitie"("ID_Procedura");


--
-- Name: Oferte Oferte_ID_Furnizor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Oferte"
    ADD CONSTRAINT "Oferte_ID_Furnizor_fkey" FOREIGN KEY ("ID_Furnizor") REFERENCES public."Furnizori"("ID_Furnizor");


--
-- Name: Oferte Oferte_ID_Procedura_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Oferte"
    ADD CONSTRAINT "Oferte_ID_Procedura_fkey" FOREIGN KEY ("ID_Procedura") REFERENCES public."Proceduri_Achizitie"("ID_Procedura");


--
-- Name: Oferte Oferte_ID_Referat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Oferte"
    ADD CONSTRAINT "Oferte_ID_Referat_fkey" FOREIGN KEY ("ID_Referat") REFERENCES public."Referate_Necesitate"("ID_Referat");


--
-- Name: Proceduri_Achizitie Proceduri_Achizitie_ID_Utilizator_Creare_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Proceduri_Achizitie"
    ADD CONSTRAINT "Proceduri_Achizitie_ID_Utilizator_Creare_fkey" FOREIGN KEY ("ID_Utilizator_Creare") REFERENCES public."Utilizatori"("ID_Utilizator");


--
-- Name: Produse Produse_ID_Categorie_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse"
    ADD CONSTRAINT "Produse_ID_Categorie_fkey" FOREIGN KEY ("ID_Categorie") REFERENCES public."Categorii"("ID_Categorie");


--
-- Name: Produse_In_Loturi Produse_In_Loturi_ID_Lot_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Loturi"
    ADD CONSTRAINT "Produse_In_Loturi_ID_Lot_fkey" FOREIGN KEY ("ID_Lot") REFERENCES public."Loturi"("ID_Lot");


--
-- Name: Produse_In_Loturi Produse_In_Loturi_ID_Produs_Referat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Loturi"
    ADD CONSTRAINT "Produse_In_Loturi_ID_Produs_Referat_fkey" FOREIGN KEY ("ID_Produs_Referat") REFERENCES public."Produse_In_Referate"("ID_Produs_Referat");


--
-- Name: Produse_In_Referate Produse_In_Referate_ID_Produs_Generic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Referate"
    ADD CONSTRAINT "Produse_In_Referate_ID_Produs_Generic_fkey" FOREIGN KEY ("ID_Produs_Generic") REFERENCES public."Produse"("ID_Produs");


--
-- Name: Produse_In_Referate Produse_In_Referate_ID_Referat_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Produse_In_Referate"
    ADD CONSTRAINT "Produse_In_Referate_ID_Referat_fkey" FOREIGN KEY ("ID_Referat") REFERENCES public."Referate_Necesitate"("ID_Referat");


--
-- Name: Referate_Necesitate Referate_Necesitate_ID_Utilizator_Creare_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Referate_Necesitate"
    ADD CONSTRAINT "Referate_Necesitate_ID_Utilizator_Creare_fkey" FOREIGN KEY ("ID_Utilizator_Creare") REFERENCES public."Utilizatori"("ID_Utilizator");


--
-- Name: Variante_Comerciale_Produs Variante_Comerciale_Produs_ID_Producator_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Variante_Comerciale_Produs"
    ADD CONSTRAINT "Variante_Comerciale_Produs_ID_Producator_fkey" FOREIGN KEY ("ID_Producator") REFERENCES public."Producatori"("ID_Producator");


--
-- Name: Variante_Comerciale_Produs Variante_Comerciale_Produs_ID_Produs_Generic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public."Variante_Comerciale_Produs"
    ADD CONSTRAINT "Variante_Comerciale_Produs_ID_Produs_Generic_fkey" FOREIGN KEY ("ID_Produs_Generic") REFERENCES public."Produse"("ID_Produs");


--
-- Name: contracte_loturi_procedura_asociere contracte_loturi_procedura_asociere_contract_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public.contracte_loturi_procedura_asociere
    ADD CONSTRAINT contracte_loturi_procedura_asociere_contract_id_fkey FOREIGN KEY (contract_id) REFERENCES public."Contracte"("ID_Contract");


--
-- Name: contracte_loturi_procedura_asociere contracte_loturi_procedura_asociere_lot_procedura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public.contracte_loturi_procedura_asociere
    ADD CONSTRAINT contracte_loturi_procedura_asociere_lot_procedura_id_fkey FOREIGN KEY (lot_procedura_id) REFERENCES public."Loturi_Procedura"("ID_Lot_Procedura");


--
-- Name: lot_procedura_articole_asociere lot_procedura_articole_asociere_lot_procedura_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public.lot_procedura_articole_asociere
    ADD CONSTRAINT lot_procedura_articole_asociere_lot_procedura_id_fkey FOREIGN KEY (lot_procedura_id) REFERENCES public."Loturi_Procedura"("ID_Lot_Procedura");


--
-- Name: lot_procedura_articole_asociere lot_procedura_articole_asociere_produs_referat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nume_utilizator_pg
--

ALTER TABLE ONLY public.lot_procedura_articole_asociere
    ADD CONSTRAINT lot_procedura_articole_asociere_produs_referat_id_fkey FOREIGN KEY (produs_referat_id) REFERENCES public."Produse_In_Referate"("ID_Produs_Referat");


--
-- PostgreSQL database dump complete
--

