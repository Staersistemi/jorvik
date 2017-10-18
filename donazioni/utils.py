from collections import OrderedDict

import xlsxwriter.utility
import pyexcel
from django.conf import settings
from django.template.loader import get_template

from donazioni.models import TokenRegistrazioneDonatore
from posta.models import Messaggio


def _importa(formato, file_import, intestazione, separatore_csv=','):
    """
    :param formato: 'csv' o 'xls'
    :param file_import: InMemoryUploadedFile
    :param intestazione: int: numero di righe da saltare all'inizio
    :return: tupla: (preview dati, Oggetto Sheet di pyexcel)

        colonne_preview = {'A CampoX': 'A, B, C',
           'B CampoY': 'TEST 1, TEST 2, TEST 3',
           'C CampoZ': 'AMBA, RABA, CICCI, COCCO'} # dict di stringhe con chiave intera (indice colonna)
        dati = [['A', 'B', 'C',...,],...]  # oggetto Sheet iterabile come lista di liste
    """
    kwargs = {'file_content': file_import.read(), 'file_type': formato}
    if formato == 'csv':
        kwargs['delimiter'] = separatore_csv
    foglio = pyexcel.get_sheet(**kwargs)
    colonne_preview = _prepara_preview(foglio, intestazione)
    foglio = pyexcel.get_sheet(start_row=intestazione, **kwargs)
    return colonne_preview, foglio


def _prepara_preview(foglio, intestazione=0):
    # prepara una preview dei dati basata su colonna, con i valori delle prime 5 righe
    # include il nome della colonna presumibilmente a riga 0, se intestazione > 0
    dati_colonna = _OrderedDefaultListDict()
    intestazioni_colonna = {}
    for num_riga, riga in enumerate(foglio.row[:5]):
        for i, valore in enumerate(riga):
            if num_riga == 0 and intestazione > 0:  # fuzzy guess
                intestazioni_colonna[i] = valore
                continue
            if num_riga <= intestazione:
                continue
            nome_colonna = '{} {}'.format(colnum_string(i), intestazioni_colonna.get(i))
            dati_colonna[nome_colonna].append(str(valore))
    colonne_preview = OrderedDict()
    for nome_colonna, values in dati_colonna.items():
        colonne_preview[nome_colonna] = ', '.join(v for v in values if v)
    return colonne_preview


def analizza_file_import(file_importato, intestazione=0, formato='csv', separatore_csv=','):
    if formato not in ('csv', 'xls'):
        raise ValueError('Formato non valido %s' % formato)
    return _importa(formato, file_importato, intestazione, separatore_csv=separatore_csv)


def colnum_string(n):
    """
    Mappa l'indice di colonna con il tipico formato Excel per il nome della colonna
    :param n: int: numero colonna del foglio
    :return: stringa corrispondente nel formato lettere

    Esempio:
    >>> print(colnum_string(28))
    <<< 'AB'
    """
    return xlsxwriter.utility.xl_col_to_name(n)


class _OrderedDefaultListDict(OrderedDict):
    def __missing__(self, key):
        self[key] = value = []
        return value


class FormatoImport:
    associazioni = {}

    @property
    def campi_definiti(self):
        return [v for v in self.associazioni.values()]


class FormatoPayPal(FormatoImport):
    associazioni = {'colonna_A Data': 'data',
                    'colonna_C Nome': 'nome',
                    'colonna_I Netto': 'importo',
                    'colonna_J Codice transazione': 'codice_transazione',
                    }


class FormatoAmmado(FormatoImport):
    associazioni = {'colonna_A Data': 'data',
                    'colonna_D Nome': 'nome',
                    'colonna_E Cognome': 'cognome',
                    'colonna_F Indirizzo email': 'email',
                    'colonna_H Donation Source': 'metodo_pagamento',
                    'colonna_L Frequency': 'modalita_singola_ricorrente',
                    'colonna_W Payable Amount': 'importo',
                    'colonna_AE Address 1': 'indirizzo',
                    'colonna_AG City/Town': 'comune_residenza',
                    'colonna_AI ZIP/Postal Code': 'cap_residenza',
                    'colonna_AJ Country': 'stato_residenza',
                    'colonna_AK Language': 'lingua',
                    'colonna_AL Telephone': 'telefono',
                    }


class FormatoAmazon(FormatoImport):
    associazioni = {'colonna_A BuyerName': 'nome',
                    'colonna_B BuyerEmailAddress': 'email',
                    'colonna_C BillingAddressLine1': 'indirizzo',
                    'colonna_F BillingAddressCity': 'comune_residenza',
                    'colonna_I BillingAddressPostalCode': 'cap_residenza',
                    'colonna_J BillingAddressCountryCode': 'stato_residenza',
                    }


class FormatoCroceRossaIt(FormatoImport):
    associazioni = {'colonna_C TipoDonatore': 'tipo_donatore',
                    'colonna_D Nome': 'nome',
                    'colonna_E Cognome': 'cognome',
                    'colonna_F Genere': 'sesso',
                    'colonna_G CF': 'codice_fiscale',
                    'colonna_H RagioneSociale': 'ragione_sociale',
                    'colonna_I PIVA': 'partita_iva',
                    'colonna_J DTNascita': 'data_nascita',
                    'colonna_K Indirizzo': 'indirizzo',
                    'colonna_L CAP': 'cap_residenza',
                    'colonna_M Citta': 'comune_residenza',
                    'colonna_N NomeProvincia': 'provincia_residenza',
                    'colonna_O NomeNazione': 'stato_residenza',
                    'colonna_P Email': 'email',
                    'colonna_Q Telefono': 'telefono',
                    'colonna_S Lang': 'lingua',
                    'colonna_X CodiceDonazione': 'codice_transazione',
                    'colonna_Y Importo': 'importo',
                    'colonna_Z ModalitaDonazione': 'modalita_singola_ricorrente',
                    'colonna_AA TSDonazione': 'data',
                    'colonna_AC MetodoPagamento': 'metodo_pagamento',
                    }


class FormatoImportPredefinito:
    formati = {'P': FormatoPayPal, 'A': FormatoAmmado, 'Z': FormatoAmazon,
               'R': FormatoCroceRossaIt}


def invia_mail_ringraziamento(donatore, campagna):
    testo_email = campagna.testo_email_ringraziamento
    destinatario = donatore.email
    token = TokenRegistrazioneDonatore.genera(donatore, campagna.organizzatore)
    host_registrazione = 'https://gaia.cri.it/' if not settings.DEBUG else 'http://127.0.0.1:8000/'
    vista_registrazione = 'registrati/soggetto_donatore/credenziali/' if donatore.codice_fiscale else 'registrati/soggetto_donatore/codice_fiscale/'
    link_registrazione = '{}{}?t={}'.format(host_registrazione, vista_registrazione, token)

    oggetto = 'Ciao {}'.format(donatore.nome_completo)
    corpo = {'testo': testo_email,
             'donatore': donatore,
             'link_registrazione': link_registrazione,
             'campagna': campagna}
    # Messaggio.costruisci_e_accoda(oggetto, 'email_ringraziamento_donazione_economica.html',
    #                               corpo=corpo, destinatari=[destinatario])

    Messaggio.invia_raw(
        oggetto=oggetto,
        corpo_html=get_template('email_ringraziamento_donazione_economica.html').render(corpo),
        email_mittente=None,
        lista_email_destinatari=[[destinatario]]
    )
    return link_registrazione
