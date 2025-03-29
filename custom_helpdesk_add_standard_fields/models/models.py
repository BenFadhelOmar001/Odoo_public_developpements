# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)




class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    
    x_studio_civilit_1 = fields.Selection([('mme', 'Mme'),
                                      ('mr', 'Mr'),

                                      ], string="Civilité")
    x_studio_selection_field_7Bvj3 = fields.Selection([('test1', 'Test1'),
                                      ('test2', 'Test2'),

                                      ], string="New selection")
    # x_studio_nom1 = fields.Selection([('TEST1', 'Test1'),
    #                                   ('TEST2', 'Test2'),
    #
    #                                   ],string="nom 1")
    x_studio_nom_2 = fields.Char(string="Nom")
    x_studio_prnom = fields.Char(string="Prénom")
    x_studio_date_de_naissance = fields.Date(string="Date de naissance")
    x_studio_date_adresse_1 = fields.Text(string="Adresse mail professionnelle")
    num_professionnel = fields.Integer()
    x_studio_date_de_cration = fields.Date(string="Date de création", default=datetime.today())
    x_studio_pc_housse_sourisclavier = fields.Boolean(string="PC + Housse + Souris/Clavier")
    x_studio_ecran = fields.Boolean(string="Ecran")
    x_studio_ecran_supplmentaire = fields.Boolean(string="Ecran Supplémentaire")
    x_studio_email_cc = fields.Char(string="Email cc")
    x_studio_date_darrive = fields.Date(string="Date d'arrivée")
    x_studio_date_de_depart = fields.Date(string="Date de départ")
    x_studio_type_de_recrutement = fields.Selection([('Création de poste', 'Création de poste'),
                                      ('Changement interne', 'Changement interne'),
                                      ('Remplacement', 'Remplacement'),

                                      ],string="Type de recrutement")
    x_studio_type_de_contrat = fields.Selection([('CDI', 'CDI'),
                                      ('CDD', 'CDD'),
                                      ('Stage', 'Stage'),
                                      ('Intérim', 'Intérim'),
                                      ('Saisonnier', 'Saisonnier'),
                                      ('Changement de contrat', 'Changement de contrat'),
                                      ("Contrat d'apprentissage", "Contrat d'apprentissage"),

                                      ],string="Type de contrat")
    x_studio_matricule = fields.Char(string="Matricule")
    x_studio_centre_de_cot = fields.Char(string="Centre de coût")
    x_studio_site_de_rattachement = fields.Selection([('Paris', 'Paris'),
                                      ('Bourgoin', 'Bourgoin'),
                                      ('Montaigu', 'Montaigu'),
                                      ('Castelnau', 'Castelnau'),
                                      ('geslot', 'Geslot'),
                                      ('Lisses', 'Lisses')

                                      ],string="Site de rattachement")
    x_studio_direction = fields.Selection([('RH', 'RH'),
                                      ('Logistique', 'Logistique'),
                                      ('Informatique', 'Informatique'),
                                      ('Commerce', 'Commerce'),
                                      ('Finance', 'Finance'),
                                      ('Achat & Marketing', 'Achat & Marketing'),

                                      ],string="Direction")
    #x_studio_nom_du_n1 = fields.Char(string="Nom de N+1")
    #x_studio_adresse_mail_du_n1 = fields.Char(string="Adresse mail de N+1")
    x_studio_type_de_fontion = fields.Many2one('hr.job', string="Type de foncion")
    # x_studio_nom_dun_collaboratteur_avec_un_poste_quivalent = fields.Many2one('hr.job', string="Nom d'un collaboratteur avec un poste équivalent")

    personne_remplace = fields.Many2one('res.partner')
    
    is_autre_fonction = fields.Boolean(related='x_studio_type_de_fontion.is_autre')
    autre_type_de_fonction = fields.Char(string="Autre type de fonction")


    
