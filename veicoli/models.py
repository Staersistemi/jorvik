from django.db import models
from anagrafica.models import Persona, Sede
from base.models import ModelloSemplice
from base.tratti import ConEstensione, ConStorico
from base.tratti import ConMarcaTemporale

__author__ = 'alfioemanuele'


class Autoparco(ModelloSemplice, ConEstensione, ConMarcaTemporale):
    """
    Rappresenta un Autoparco CRI
    """

    class Meta:
        verbose_name_plural = "Autoparchi"


class Veicolo(ModelloSemplice, ConMarcaTemporale):
    """
    Rappresenta un Veicolo CRI, immatricolato o meno.

    Le tipologie di Targa sono state estratte dall'Allegato 12/10 del Testo Unico della Motorizzazione CRI
    """

    DEFAULT_PROPRIETARIO_COGNOME = "Croce Rossa Italiana"
    DEFAULT_PROPRIETARIO_NOME = "Comitato Centrale"
    DEFAULT_PROPRIETARIO_INDIRIZZO = "Via Toscana, 12, 00187 Roma (RM), Italia"

    class Meta:
        verbose_name_plural = "Veicoli"

    IN_IMMATRICOLAZIONE = 'IM'
    IN_SERVIZIO = 'OK'
    DISMESSO = 'KO'
    STATO = (
        (IN_IMMATRICOLAZIONE, "In immatricolazione"),
        (IN_SERVIZIO, "In servizio"),
        (DISMESSO, "Dismesso/Fuori uso")
    )
    stato = models.CharField("Stato", choices=STATO, max_length=2, default=IN_SERVIZIO)

    TARGA_AUTOVEICOLI_A = 'A'
    TARGA_AUTOVEICOLI_B = 'B'
    TARGA_MOTOVEICOLI = 'C'
    TARGA_RIMORCHI = 'D'
    FORMATO_TARGA = (
        (TARGA_AUTOVEICOLI_A, "Targa per Autoveicoli (A)"),
        (TARGA_AUTOVEICOLI_B, "Targa per Autoveicoli (B), per alloggiamenti viconlati"),
        (TARGA_MOTOVEICOLI, "Targa per Motoveicoli, Veicoli Speciali, Macchine Operatrici"),
        (TARGA_RIMORCHI, "Targa per Rimorchi")
    )

    libretto = models.CharField("N. Libretto", help_text="Formato 201X-XXXXXXXXX", max_length=16, db_index=True, blank=False, null=False)
    targa = models.CharField("Targa (A)", help_text="Targa del Veicolo, senza spazi.", max_length=5, db_index=True, blank=False, null=False)
    formato_targa = models.CharField("Formato Targa", max_length=1, choices=FORMATO_TARGA, default=TARGA_AUTOVEICOLI_A)
    prima_immatricolazione = models.DateField("Prima Immatricolazione (B)", db_index=True, blank=False, null=False)

    # Sezione C: Proprietario
    proprietario_cognome = models.CharField("Proprietario: Cognome o Ragione Sociale (C2.1)", max_length=127, default=DEFAULT_PROPRIETARIO_COGNOME)
    proprietario_nome = models.CharField("Proprietario: Nome o Iniziale (C2.2)", max_length=127, default=DEFAULT_PROPRIETARIO_NOME)
    proprietario_indirizzo = models.CharField("Proprietario: Indirizzo (C2.3)", max_length=127, default=DEFAULT_PROPRIETARIO_INDIRIZZO)

    # Sezione Pneumatici
    pneumatici_anteriori = models.CharField("Pneumatici: Anteriori", max_length=32, help_text="es. 215/70 R12C")
    pneumatici_posteriori = models.CharField("Pneumatici: Posteriori", max_length=32, help_text="es. 215/70 R12C")
    pneumatici_alt_anteriori = models.CharField("Pneumatici alternativi: Anteriori", max_length=32, help_text="es. 215/70 R12C", blank=True, null=True)
    pneumatici_alt_posteriori = models.CharField("Pneumatici alternativi: Posteriori", max_length=32, help_text="es. 215/70 R12C", blank=True, null=True)

    # Sezione Caratteristiche e Dimensioni
    cambio = models.CharField("Cambio", max_length=32, help_text="Tipologia di Cambio", default="Meccanico")
    lunghezza = models.FloatField("Lunghezza m.", blank=True, null=True)
    larghezza = models.FloatField("Larghezza m.", blank=True, null=True)
    sbalzo = models.FloatField("Sbalzo m.", blank=True, null=True)
    tara = models.PositiveIntegerField("Tara kg.", blank=True, null=True)

    # Sezione D: Veicolo
    marca = models.CharField("Marca (D.1)", max_length=32, help_text="es. Fiat")
    modello = models.CharField("Tipo (D.2)", max_length=32, help_text="es. Ducato")

    # Sezione E:
    telaio = models.CharField("Numero Identificazione Veicolo (E)", help_text="Numero di telaio del veicolo, es. ZXXXXXXXXXXXXXXX", max_length=24, db_index=True, unique=True)

    # Sezione F
    massa_max = models.PositiveIntegerField("Massa Massima a carico (F.2)")

    # Sezione I
    data_immatricolazione = models.DateField("Data immatricolazione attuale (I)", db_index=True)

    # Sezione J
    categoria = models.CharField("Categoria del Veicolo (J)", max_length=16, help_text="es. Ambulanza", db_index=True)
    destinazione = models.CharField("Destinazione ed uso (J.1)", max_length=32, help_text="es. Amb. Soccorso (AMB-A)")
    carrozzeria = models.CharField("Carrozzeria (J.2)", max_length=16, help_text="es. Chiuso")

    # Sezione K
    omologazione = models.CharField("N. Omologazione (K)", max_length=32, help_text="es. OEXXXXXXXXXX", blank=True, null=True)

    # Sezione L
    num_assi = models.PositiveSmallIntegerField("Num. Assi (L)", default=2)

    # Sezione O
    rimorchio_frenato = models.FloatField("Massa massima a Rimorchio frenato tecnicamente ammissibile (O) kg.", blank=True, null=True)

    # Sezione P
    cilindrata = models.PositiveIntegerField("Cilindrata (P.1)")
    potenza_massima = models.PositiveIntegerField("Potenza Massima (P.2) kW.")

    BENZINA = 'B'
    GASOLIO = 'G'
    GPL = 'P'
    METANO = 'M'
    ELETTRICA = 'E'
    ALIMENTAZIONE = (
        (BENZINA, "Benzina"),
        (GASOLIO, "Gasolio"),
        (GPL, "GPL"),
        (METANO, "Metano"),
        (ELETTRICA, "Elettrica"),
    )
    alimentazione = models.CharField("Alimentazione (P.3)", choices=ALIMENTAZIONE, default=BENZINA)

    # Sezione S
    posti = models.SmallIntegerField("N. Posti a sedere conducente compreso (S.1)", default=5)

    # Sezione U
    regine = models.PositiveIntegerField("Livello Sonoro: Regime del motore (U.2)")

    # Informazioni aggiuntive
    telepass = models.CharField("Numero Telepass", max_length=64, blank=True, null=True)
    card_rifornimento = models.CharField("N. Card Rifornimento", max_length=64, blank=True, null=True)
    selettiva_radio = models.CharField("Selettiva Radio", max_length=64, blank=True, null=True)
    telepass = models.CharField("Numero Telepass", max_length=64, blank=True, null=True)

    # Intervallo revisione
    INTERVALLO_REVISIONE = (
        (365, "1 anno (365 giorni)"),
        (730, "2 anni (730 giorni)")
    )
    intervallo_revisione = models.PositiveIntegerField("Intervallo Revisione", choices=INTERVALLO_REVISIONE, default=365)


class Immatricolazione(ModelloSemplice, ConMarcaTemporale):
    """
    Rappresenta una pratica di immatricolazione di un Veicolo

    Una pratica viene istruita da un ufficio motorizzazione per conto di una unita' CRI richiedente.
    La stessa viene sottoposta a due stadi di approvazione, in seguito alla istruzione. Quando la
    pratica termina, il veicolo viene immatricolato ed entra in servizio.
    """

    class Meta:
        verbose_name = "Pratica di Immatricolazione"
        verbose_name_plural = "Pratiche di Immatricolazione"

    richiedente = models.ForeignKey(Sede, related_name='immatricolazioni_richieste')
    ufficio = models.ForeignKey(Sede, related_name='immatricolazioni_istruite')
    veicolo = models.ForeignKey(Veicolo, related_name='richieste_immatricolazione')


class Collocazione(ModelloSemplice, ConStorico):

    class Meta:
        verbose_name = "Collocazione veicolo"
        verbose_name_plural = "Collocazioni veicolo"

    veicolo = models.ForeignKey(Veicolo, related_name='collocazioni')
    autoparco = models.ForeignKey(Autoparco, related_name='autoparco')


class FermoTecnico(ModelloSemplice, ConStorico, ConMarcaTemporale):

    class Meta:
        verbose_name = "Fermo tecnico"
        verbose_name_plural = "Fermi tecnici"

    veicolo = models.ForeignKey(Veicolo, related_name='fermi_tecnici')


class Manutenzione(ModelloSemplice, ConMarcaTemporale):

    class Meta:
        verbose_name = "Intervento di Manutenzione"
        verbose_name_plural = "Interventi di Manutenzione"


class Segnalazione(ModelloSemplice, ConMarcaTemporale):
    """
    Rappresenta una segnalazione di malfunzionamento o incidente relativa ad un veicolo in autoparco.

    Una Segnalazione puo' essere iniziata da un qualsiasi individuo che entri in contatto col veicolo.
    La Segnalazione NON puo' essere rimossa. Viene archiviata una volta che viene assegnata ad una manutenzione.
    """

    autore = models.ForeignKey(Persona, related_name='segnalazioni')
    descrizione = models.TextField("Descrizione", max_length=1024, )
    manutenzione = models.ForeignKey(Manutenzione, related_name='segnalazioni', blank=True, null=True)
    veicolo = models.ForeignKey(Veicolo, related_name='segnalazioni')

    class Meta:
        verbose_name = "Segnalazione di malfunzionamento o incidente"
        verbose_name_plural = "Segnalazioni di malfunzionamento o incidente"


class Rifornimento(ModelloSemplice, ConMarcaTemporale):
    """
    Rappresenta un rifornimento di Carburante registrato relativamente ad un veicolo CRI.

    Gli attributi di questa entita' sono stati costruiti sulla base dell'Allegato 38/10 al Testo
    Unico della Motorizzazione CRI ("FOGLIO DI RIFORNIMENTO PER AUTOMEZZI E NATANTI").

    Il campo RAPPORTO non e' riprodotto. Invece, ove necessario, una nuova SEGNALAZIONE puo' essere
    creata, ed assegnata al Rifornimento (tramite il campo `segnalazione`).
    """

    numero = models.PositiveIntegerField("Num. rifornimento", default=1, db_index=True)
    veicolo = models.ForeignKey(Veicolo, related_name='rifornimenti')
    conducente = models.ForeignKey(Persona, related_name='rifornimenti')
    data = models.DateTimeField("Data rifornimento", db_index=True)
    contachilometri = models.PositiveIntegerField("Contachilometri", db_index=True)

    consumo_carburante = models.FloatField("Consumo carburante lt.", blank=True, default=None, null=True, db_index=True)
    consumo_olio_m = models.FloatField("Consumo Olio motori Kg.", blank=True, default=None, null=True, db_index=True)
    consumo_olio_t = models.FloatField("Consumo Olio trasmissioni Kg.", blank=True, default=None, null=True, db_index=True)
    consumo_olio_i = models.FloatField("Consumo Olio idraulico Kg.", blank=True, default=None, null=True, db_index=True)

    CISTERNA_INTERNA = 'I'
    DISTRIBUTORE_CONVENZIONATO = 'C'
    DISTRIBUTORE_OCCASIONALE = 'D'
    PRESSO = (
        (CISTERNA_INTERNA, "Cisterna interna"),
        (DISTRIBUTORE_CONVENZIONATO, "Distributore convenzionato"),
        (DISTRIBUTORE_OCCASIONALE, "Distributore occasionale")
    )
    presso = models.CharField("Presso", choices=PRESSO, default=DISTRIBUTORE_OCCASIONALE, max_length=1)

    contalitri = models.FloatField("(c/o Cisterna int.) Contalitri", blank=True, default=None, null=True, db_index=True)
    ricevuta = models.CharField("(c/o Distributore) N. Ricevuta", max_length=32, blank=True, default=None, null=True, db_index=True)

    segnalazione = models.ForeignKey(Segnalazione, help_text="Rapporto conducente", blank=True, default=None, null=True, db_index=True)

    class Meta:
        verbose_name = "Rifornimento di carburante"
        verbose_name_plural = "Rifornimenti di carburante"