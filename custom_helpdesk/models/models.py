# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class HrJobInherit(models.Model):
    _inherit = 'hr.job'

    is_autre = fields.Boolean(string="Autre")
    metier = fields.Selection([
        ('MARKETING/ACHATS', 'MARKETING/ACHATS'),
        ('IT', 'IT'),
        ('CONTRÔLE DE GESTION', 'CONTRÔLE DE GESTION'),
        ('COMPTABILITE', 'COMPTABILITE'),
        ('RH', 'RH'),
        ('COMMERCE', 'COMMERCE'),
        ('LOGISTIQUE', 'LOGISTIQUE'),
        ('APPROVISIONNEMENT', 'APPROVISIONNEMENT'),
        ('TRANSPORT', 'TRANSPORT'),
        ('SERVICE CLIENT', 'SERVICE CLIENT'),
        ('QSE', 'QSE'),
    ], string='Métier')
    
    metier_id = fields.Many2one('dr.metier', string='Métier')

    @api.model
    def get_jobs_by_metier(self, metier):
        if not metier:
            return []

        try:
            # Use sudo to bypass access rights
            return self.sudo().search_read([('metier_id', '=', int(metier))], ['id', 'name'])
        except Exception as e:
            _logger.error(f"Error fetching jobs by metier: {e}")
            return []





class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    access_for_numero_de_mobile = fields.Boolean(string="Accès pour Numéro de mobile")
    access_for_code_sim = fields.Boolean(string="Accès pour Code SIM")
    access_for_numero_de_ligne_fixe = fields.Boolean(string="Accès pour Numéro de ligne fixe")
    access_for_adresse_mail = fields.Boolean(string="Accès pour Adresse mail")
    access_for_mot_de_passe_windows = fields.Boolean(string="Accès pour Mot de passe windows")
    access_for_commentaires_prestataires = fields.Boolean(string="Accès pour Commentaires prestataires")
    
    group_demande_recrutement_demandeur = fields.Boolean(string="Group Demandeur")
    group_demande_recrutement_rrh = fields.Boolean(string="Group RRH")
    group_demande_recrutement_rdrh = fields.Boolean(string="Group RDRH")
    group_demande_recrutement_direction = fields.Boolean(string="Group Direction")
    group_demande_recrutement_drh = fields.Boolean(string="Group DRH")

    demande_recrutement_session = fields.Char(string="Demande recrutement session")

    direction_a_choisir = fields.Selection([
        ('MARKETING/ACHATS', 'MARKETING/ACHATS'),
        ('IT', 'IT'),
        ('FINANCES', 'FINANCES'),
        ('RH', 'RH'),
        ('GRANDS COMPTES NAT.', 'GRANDS COMPTES NAT.'),
        ('DO OUEST', 'DO OUEST'),
        ('DO SUD', 'DO SUD'),
        ('DO IDF', 'DO IDF'),
        ('SUPPLY NAT.', 'SUPPLY NAT.'),
        ('GESLOT', 'GESLOT'),
        ('PROJET', 'PROJET'),
    ], string='Direction à choisir')
    
    direction_id = fields.Many2one('dr.direction', string='Direction')


    






    
class HelpdeskTeamInherit(models.Model):
    _inherit = 'helpdesk.team'

    equipe = fields.Selection([('service_clientele', 'Service Clientèle'),
                              ('support_rh', 'Support RH'),
                              ('master_data', 'Master Data'),('demande_recrutement', 'Demande Recrutement'),
                              ], string='Equipe')


class HelpdeskStageInherit(models.Model):
    _inherit = 'helpdesk.stage'


    etape =fields.Selection([('traitement_prestataire', 'Traitement prestataire'), ('preparation_coordinateur_it', 'Préparation Coordinateur IT'),
                             ('demande_rh', 'Demande RH'), ('preparation_prestataire', 'Préparation Prestataire'),('traitement_manager', 'Traitement Manager'),
                             ('Preparation_materiel_interne', 'Préparation matériel interne'), ('retour_presta', 'Retour Presta'), ('en_attente', 'En attente'), ('dr_demande', 'DR Demande'),('dr_traitemnt_rrh', 'DR traitement rrh'),
                              ('dr_traitement_rdrh', 'DR traitement rdrh'),('dr_traitement_direction', 'DR traitement direction'),
                             ('dr_traitement_drh', 'DR traitement drh'),
                                ('dr_refuse', 'DR refuse'),('dr_valide', 'DR valide'),], string='Etape')
    destinataires = fields.Char(string='Destinataires')
    destinataires_besoin_smartphone = fields.Char(string='Destinataires Smartphones')
    besoin_smartphone = fields.Boolean(string='Besoin Smartphone')
    
    destinataires_for_pc_portable = fields.Char(string='Destinataires Pc Portable + Chargeur + Housse')
    destinataires_for_tablette = fields.Char(string='Destinataires Tablette + Chargeur')
    destinataires_for_smartphone = fields.Char(string='Destinataires Smartphone + Accessoires')
    destinataires_for_besoin_ligne_fixe = fields.Char(string="Destinataires Besoin d'une ligne fixe")

    destinataires_for_vehicule_fonction = fields.Char(string='Destinataires Véhicule de fonction')
    destinataires_for_logiciel_sap = fields.Char(string='Destinataires logiciel SAP')
    destinataires_for_lc_start = fields.Char(string='Destinataires Logiciel Commerce Start')
    destinataires_for_lc_nomad = fields.Char(string='Destinataires Logiciel Commerce Nomad')






# class MailChannelInherit(models.Model):
#     _inherit = 'mail.channel'
#
#
#     ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', readonly=True)

class ResUsersInherit(models.Model):
    _inherit = 'res.users'


    #notification = fields.Boolean( string='Notification from ticket')
    group_hr_manager_data = fields.Boolean()
    group_it_manager_data = fields.Boolean()

class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    def name_get(self):
        result = []
        for ticket in self:
            result.append((ticket.id, "%s (#%s)" % (ticket.name, ticket.id)))
        return result

    # Formulaire IT
    status = fields.Char(compute="get_status")
    equipe = fields.Char(compute="get_equipe")

    @api.depends('stage_id')
    def get_status(self):
        self.status = str(self.stage_id.etape)

    @api.depends('team_id')
    def get_equipe(self):
        self.equipe = str(self.team_id.equipe)

    employee_id = fields.Many2one('hr.employee', string='Employé')
    site_rattachment = fields.Selection([('lisses', 'Lisses'),
                                         ('paris', 'Paris'),
                                         ('montaigu', 'Montaigu'), ('bourgoin', 'Bourgoin'),
                                         ('castelnau', 'Castelnau'),
                                         ('geslot', 'Geslot')
                                         ], string='Site de rattachment')




    question = fields.Selection([
        ('materiel', 'Matèriel'),
        ('logiciel', 'Logiciel'),
        ('master_data', 'Master data')
    ], string='Question concerne')

    materiel = fields.Selection([('pc', 'PC'),
                                 ('smartphone', 'Smartphone'),
                                 ('ipad', 'IPad'), ('imprimante', 'Imprimante'),
                                 ('wap_logistique', 'Wap logistique'),
                                 ('reseau_sasety', 'Réseau sasety'),
                                 ('flasheuse', 'Flasheuse'),
                                 ('voice_picking', 'Appareil voice Picking'),
                                 ('wap_logistique', 'Wap logistique'),
                                 ('autres', 'Autres')
                                 ], string='Matèriel')

    logiciel = fields.Selection([('sap', 'SAP'),
                                 ('nomad', 'Nomad'),
                                 ('edi', 'EDI'),
                                 ('office', 'Office (teams, outlook)'), ('start', 'Start'),
                                 ('argu', 'L argu au bout des doigts'),
                                 ('ecommerce', 'Site E-commerce'),
                                 ('cleemy', 'Cleemy/Timmy'), ('note_frais', 'Note de frais/Congés'),
                                 ('kyriba', 'Kyriba'), ('wechek', 'Wechek'), ('vim', 'VIM'),
                                 ], string='Logiciel')

    sujet = fields.Char(string='Sujet')
    sujet_master_data = fields.Char(string='Sujet')

    seul_impacte = fields.Selection([('oui', 'Oui'),
                                     ('non', 'Non'),

                                     ], string='Seul impacté', default='oui')

    travaille = fields.Selection([('oui', 'Oui'),
                                  ('non', 'Non'),

                                  ], string='Continuation de travailler', default='oui')

    num_transaction = fields.Char(string='Numéro de transaction')
    num_imprimante = fields.Char(string='Numéro Imprimane')

    nouveau_materiel = fields.Selection([('oui', 'Oui'),
                                         ('non', 'Non'),

                                         ], string='Demande de nouveau matèriel', default='non')

    responsable_hierarchique = fields.Char(string='Responsable hierarchique')

    type_materiel = fields.Selection([('pc', 'PC'),
                                      ('smartphone', 'Smartphone'),
                                      ('ipad', 'Tablette (IPad)'), ('imprimante', 'Imprimante'),
                                      ('ecran', 'Ecran'), ('hub', 'HUB(station)'), ('cable', 'Câble'),
                                      ('autres', 'Autres'),
                                      ], string='Type matèriel')

    # pc = fields.Boolean(string="PC")
    # smartphone = fields.Boolean(string="Smartphone")
    # ipad = fields.Boolean(string="Ecran")
    # ecran = fields.Boolean(string="Ecran")
    # imprimante = fields.Boolean(string="Imprimante")
    # hub = fields.Boolean(string="HUB(station)")
    # cable = fields.Boolean(string="Câble")
    # autres = fields.Boolean(string="Autres")

    comment = fields.Text(string='Commentaire')
    comment_master_data = fields.Text(string='Commentaire')
    piece = fields.Binary(string='Pièce jointe')
    piece_master_data = fields.Binary(string='Pièce jointe')

    type_master_data = fields.Selection([('creation', 'Création'),
                                         ('modification', 'Modification'),
                                         ('erreur', 'Erreur'),
                                         ], string='Type')

    seul_impacte_master_data = fields.Selection([('oui', 'Oui'),
                                                 ('non', 'Non'),

                                                 ], string='Seul impacté', default='oui')

    # Formulaire RH

    collaborateur = fields.Many2one('res.partner', string='Personne avec un poste similaire')

    pc_housse = fields.Selection([('oui', 'Oui'),
                                  ('non', 'Non'),

                                  ], string='Pc Portable + Chargeur + Housse', default='non')
    clavier = fields.Boolean(string='Matériel Supplémentaire', default=False)
    souris = fields.Boolean(string='Souris', default=False)
    ecran = fields.Boolean(string='Ecran', default=False)
    x_studio_smartphone = fields.Selection([('oui', 'Oui'),
                                       ('non', 'Non'),

                                       ], string='Smartphone + Accessoires', default='non')

    x_studio_ligne_fixe = fields.Selection([('oui', 'Oui'),
                                            ('non', 'Non'),

                                            ], string="Besoin d'une ligne fixe", default='non')
    cx = fields.Selection([('3CX', '3CX'),
                           ('INO', 'INO'),
                           ], string='3CX ou INO')
    x_studio_ligne = fields.Selection([('Nouvelle ligne', 'Nouvelle ligne'),
                                            ("Reprise d'une ligne", "Reprise d'une ligne"),

                                            ], string="Ligne fixe")
    nom_1 = fields.Char(string='Nom ou N° de la nouvelle ligne')
    nom_2 = fields.Char(string='Nom ou N° de la ligne à reprendre')


    tablette_chargeur_housse_clavier = fields.Selection([('oui', 'Oui'),
                                                         ('non', 'Non'),

                                                         ], string='Tablette + Chargeur',
                                                        default='non')

    # logiciel_commerce = fields.Selection([('nomad', 'Nomad'),
    #                                       ('start', 'Start'),
    #
    #                                       ], string='Logiciel Commerce')
    nomad = fields.Boolean(string="Nomad")
    start = fields.Boolean(string="Start")
    aucun = fields.Boolean(string="Aucun", default=True)
    sales_apps = fields.Boolean(string="SalesApps")

    # logiciel_finance = fields.Selection([('etafi', 'Etafi (laisse fiscale)'),
    #                                      ('kyriba', 'Kyriba'), ('wecheck', 'Wecheck'),
    #
    #                                      ], string='Logiciel Finance')
    etafi = fields.Boolean(string="Etafi (Liasse Fiscale)")
    kyriba = fields.Boolean(string="Kyriba")
    wecheck = fields.Boolean(string="Wecheck")
    aucun_f = fields.Boolean(string="Aucun", default=True)

    logiciel_conge = fields.Selection([('utilisateur', 'Utilisateur'),
                                         ('Contrôleur', 'Contrôleur'), ('manager', 'Manager'),
                                         ('admin', 'Admin')
                                         ], string='Profil logiciel congés (Timmy) et note de frais (Cleemy)', default='utilisateur')

    profil_fairjungle = fields.Selection([('utilisateur', 'Utilisateur'),
                                       ('Contrôleur', 'Contrôleur'), ('manager', 'Manager'),
                                       ('admin', 'Admin')
                                       ], string='Profil fairjungle', default='utilisateur')

    logiciel_sap = fields.Selection([('oui', 'Oui'),
                                  ('non', 'Non'),

                                  ], string='Logiciel SAP', default='non')

    vehicule_1 = fields.Selection([('oui', 'Oui'),
                                     ('non', 'Non'),

                                     ], string='Véhicule', default='non')
    vehicule_marque = fields.Selection([
                                   ('VP0', 'VP0'),
                                   ('VP0RM', 'VP0RM'),
                                   ('VP1', 'VP1'),
                                   ('VP3', 'VP3'),

                                   ], string='Marque')

    #nom = fields.Char(string='Liste des droits')



    logiciel_sap_analytic = fields.Selection([('oui', 'Oui'),
                                     ('non', 'Non'),

                                     ], string='Logiciel SAP Analytics', default='non')
    #justification = fields.Char(string='Justification d accées')
    vehicule = fields.Selection([('nouveau', 'Nouveau véhicule'),
                                       ('reprise', 'Reprise de véhicule d un Collaborateur'), ('aucun', 'Aucun'),
                                       ('admin', 'Admin')
                                           ], string='Voiture de fonction', default='aucun')
    personne_vehicule = fields.Char(string='Nom de la personne dont le véhicule est à reprendre')
    acces_dossier = fields.Selection([('oui', 'Oui'),
                                              ('non', 'Non'),

                                              ], string='Accés au dossiers du réseau Supergroupe', default='non')
    nom_reseau = fields.Char(string='Nom des réseaux')
    list_dossiers = fields.Char(string='Liste des dossiers (lecteurs réseau)')
    bal_partagee = fields.Char(string='BAL Partagée')
    besoin_imprimante = fields.Selection([('oui', 'Oui'),
                                      ('non', 'Non'),

                                      ], string='Besoin imprimante', default='non')

    # besoin_epi = fields.Selection([('oui', 'Oui'),
    #                                       ('non', 'Non'),
    #
    #                                       ], string='Besoin en EPI', default='non')

    comment_manager = fields.Text(string='Commentaire de manager')
    reponse = fields.Text(string='Réponse', readonly=True)

    ticket_url = fields.Char()
    reponse_url = fields.Char()

    prestataire_link = fields.Char()

    numero_de_mobile = fields.Char(string="Numéro de mobile")
    code_sim = fields.Char(string="Code SIM")
    numero_de_ligne_fixe = fields.Char(string="Numéro de ligne fixe")
    adresse_mail = fields.Char(string="Adresse mail")
    mot_de_passe_windows = fields.Char(string="Mot de passe windows")
    commentaires_prestataires = fields.Text(string="Commentaires prestataires")

    #################Begin Formulaire demande recrutement #############################

    demandeur_id = fields.Many2one('res.users', string="Damandeur ID")
    nom_du_demandeur_a_afficher = fields.Char(string="Nom du demandeur à afficher")

    date_de_creation_a_afficher = fields.Date(string="Date de création à afficher")


    etablissement = fields.Selection([
        ('MONTAIGU', 'MONTAIGU'),
        ('LISSES', 'LISSES'),
        ('PARIS', 'PARIS'),
        ('GESLOT', 'GESLOT'),
        ('BOURGOIN', 'BOURGOIN'),
        ('CASTELNAU', 'CASTELNAU'),
    ], string='Etablissement')



    rrh = fields.Selection([
        ('Juliette FABIEN', 'Juliette FABIEN'),
        ('Carole LARRAUD', 'Carole LARRAUD'),
        ('Coralie BERTHET', 'Coralie BERTHET'),
    ], string='RRH')


    direction_a_choisir = fields.Selection([
        ('MARKETING/ACHATS', 'MARKETING/ACHATS'),
        ('IT', 'IT'),
        ('FINANCES', 'FINANCES'),
        ('RH', 'RH'),
        ('GRANDS COMPTES NAT.', 'GRANDS COMPTES NAT.'),
        ('DO OUEST', 'DO OUEST'),
        ('DO SUD', 'DO SUD'),
        ('DO IDF', 'DO IDF'),
        ('SUPPLY NAT.', 'SUPPLY NAT.'),
        ('GESLOT', 'GESLOT'),
        ('PROJET', 'PROJET'),
    ], string='Direction à choisir')

    direction_a_choisir_id = fields.Many2one('dr.direction', string='Direction à choisir')


    metier_a_choisir = fields.Selection([
        ('MARKETING/ACHATS', 'MARKETING/ACHATS'),
        ('IT', 'IT'),
        ('CONTRÔLE DE GESTION', 'CONTRÔLE DE GESTION'),
        ('COMPTABILITE', 'COMPTABILITE'),
        ('RH', 'RH'),
        ('COMMERCE', 'COMMERCE'),
        ('LOGISTIQUE', 'LOGISTIQUE'),
        ('APPROVISIONNEMENT', 'APPROVISIONNEMENT'),
        ('TRANSPORT', 'TRANSPORT'),
        ('SERVICE CLIENT', 'SERVICE CLIENT'),
        ('QSE', 'QSE'),
    ], string='Métier à choisir')

    metier_a_choisir_id = fields.Many2one('dr.metier', string='Métier à choisir')

    poste_a_choisir = fields.Many2one('hr.job', string='Poste à choisir')

    poste_a_choisir_autre = fields.Text(string='Poste à choisir autre')

    motif_de_recrutement = fields.Selection([
        ('Création', 'Création'),
        ('Remplacement Départ CDI', 'Remplacement Départ CDI'),
        ('Remplacement Départ CDD', 'Remplacement Départ CDD'),
        ('Remplacement interimaire', 'Remplacement interimaire'),
        ('Remplacement CDI AML/AT/etc.', 'Remplacement CDI AML/AT/etc.'),
    ], string='Motif de recrutement')

    si_remplacement_qui = fields.Char(string="Si remplacement qui")

    type_contrat = fields.Selection([
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Saisonnier', 'Saisonnier'),
        ('Stage', 'Stage'),
        ('Alternant', 'Alternant'),
    ], string='Type contrat')

    date_de_debut_souhaite = fields.Date(string="Date de début souhaité")
    date_de_debut = fields.Date(string="Date de début")
    date_de_fin = fields.Date(string="Date de fin")

    missions_principales = fields.Text(string="Missions principales")

    commentaire_demandeur = fields.Text(string="Commentaire demandeur")

    




    secteur_geographique = fields.Char(string="Secteur géographique")

    specificite_clients = fields.Selection([
        ('Détail', 'Détail'),
        ('Pétrolier', 'Pétrolier'),
        ('GMS', 'GMS'),
        ('Hybride', 'Hybride'),
        ('Autres', 'Autres'),
        
    ], string='Spécificité clients')

    lieu_habitation_souhaite = fields.Char(string="Lieu d’habitation souhaité")

    chiffre_affaires_du_secteur_actuel = fields.Char(string="Chiffre d’affaires du secteur Actuel")
    evaluation_remuneration_annuelle_actuel = fields.Char(string="Evaluation rémunération annuelle Actuel")
    garantie_de_salaire_actuel = fields.Char(string="Garantie de salaire Actuel")
    nombre_de_clients_actuel = fields.Char(string="Nombre de clients Actuel")
    panier_moyen_actuel = fields.Char(string="Panier moyen Actuel")

    chiffre_affaires_du_secteur_vise = fields.Char(string="Chiffre d’affaires du secteur Visé")
    evaluation_remuneration_annuelle_vise = fields.Char(string="Evaluation rémunération annuelle Visé")
    garantie_de_salaire_vise = fields.Char(string="Garantie de salaire Visé")
    nombre_de_clients_vise = fields.Char(string="Nombre de clients Visé")
    panier_moyen_vise = fields.Char(string="Panier moyen Visé")




     





    #INFOS RRH
    poste_budgete = fields.Selection([
        ('Oui', 'Oui'),
        ('Non', 'Non'),
        
    ], string='Poste budgeté')

    statut_a_choisir = fields.Selection([
        ('CADRE', 'CADRE'),
        ('AGENT DE MAITRISE', 'AGENT DE MAITRISE'),
        ('TECHNICIEN', 'TECHNICIEN'),
        ('EMPLOYE', 'EMPLOYE'),
        
    ], string='Statut à choisir')

    temps_de_travail_a_choisir = fields.Selection([
        ('151,67h/mois', '151,67h/mois'),
        ('Forfait 216j', 'Forfait 216j'),
        ('Temps partiel', 'Temps partiel'),
        
    ], string='Temps de travail à choisir')

    confidentiel = fields.Selection([
        ('Oui', 'Oui'),
        ('Non', 'Non'),
        
    ], string='Confidentiel')

    fourchette_de_remuneration_annuelle_debutant = fields.Char(string="Fourchette de rémunération annuelle débutant")
    fourchette_de_remuneration_annuelle_experimente = fields.Char(string="Fourchette de rémunération annuelle expérimenté")

    commentaires = fields.Text(string="Commentaires")

    rrh_acceptation = fields.Selection([
        ('Valide', 'Valide'),
        ('Refuse', 'Refuse'),
        
    ], string='RRH acceptation')

    rrh_acceptation_user = fields.Many2one('res.users')

    rdrh_acceptation = fields.Selection([
        ('Valide', 'Valide'),
        ('Refuse', 'Refuse'),
        
    ], string='RDRH acceptation')

    rdrh_acceptation_user = fields.Many2one('res.users')

    direction_acceptation = fields.Selection([
        ('Valide', 'Valide'),
        ('Refuse', 'Refuse'),
        
    ], string='RRH acceptation')

    direction_acceptation_user = fields.Many2one('res.users')

    drh_acceptation = fields.Selection([
        ('Valide', 'Valide'),
        ('Refuse', 'Refuse'),
        
    ], string='DRH acceptation')

    drh_acceptation_user = fields.Many2one('res.users')


    rdrh_comment_complete = fields.Text()
    from_rdrh_ck_demandeur = fields.Boolean()
    from_rdrh_ck_rrh = fields.Boolean()

    direction_commentaire = fields.Text()

    drh_comment_complete = fields.Text()
    from_drh_ck_demandeur = fields.Boolean()
    from_drh_ck_rrh = fields.Boolean()
    manager_recrutement = fields.Many2one('res.partner')

    demande_recrutement_link = fields.Char(string="Demande recrutement link")


    #################End Formulaire demande recrutement ###############################

    def write(self, values):
        res = super(HelpdeskTicketInherit, self).write(values)

        if 'stage_id' in values:

            destinataires = self.stage_id.destinataires
            dbname = self.env.cr.dbname
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url += '/web?db=%s#id=%d&view_type=form&model=%s' % (dbname, self.id, self._name)

            if self.stage_id.etape == 'traitement_prestataire':
                dbname = request.env.cr.dbname
                prestataire_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                prestataire_base_url += '/helpdesk/prestataire/%s' % (self.id)
                self.prestataire_link = prestataire_base_url
                if self.stage_id.besoin_smartphone == True:
                    if self.stage_id.destinataires:
                        if self.stage_id.destinataires_besoin_smartphone:
                            destinataires = str(self.stage_id.destinataires) + ',' + str(
                                self.stage_id.destinataires_besoin_smartphone)

                    if self.stage_id.destinataires_besoin_smartphone:
                        if self.stage_id.destinataires:
                            destinataires = str(self.stage_id.destinataires) + ',' + str(
                                self.stage_id.destinataires_besoin_smartphone)
                        else:
                            destinataires = str(self.stage_id.destinataires_besoin_smartphone)

                if self.pc_housse == 'oui' and destinataires and self.stage_id.destinataires_for_pc_portable:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_pc_portable)

                if self.tablette_chargeur_housse_clavier == 'oui' and destinataires and self.stage_id.destinataires_for_tablette:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_tablette)

                if self.x_studio_smartphone == 'oui' and destinataires and self.stage_id.destinataires_for_smartphone:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_smartphone)

                if self.x_studio_ligne_fixe == 'oui' and destinataires and self.stage_id.destinataires_for_besoin_ligne_fixe:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_besoin_ligne_fixe)

                if self.nomad == True and destinataires and self.stage_id.destinataires_for_lc_nomad:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_lc_nomad)

                if self.start == True and destinataires and self.stage_id.destinataires_for_lc_start:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_lc_start)

                if self.logiciel_sap == 'oui' and destinataires and self.stage_id.destinataires_for_logiciel_sap:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_logiciel_sap)

                if self.vehicule != 'aucun' and destinataires and self.stage_id.destinataires_for_vehicule_fonction:
                    destinataires = destinataires + ',' + str(self.stage_id.destinataires_for_vehicule_fonction)

                mail_template = self.env.ref('custom_helpdesk.email_template_traitement_prestataire_avec_les_infos_1')

                # mail_context = {
                #
                #     'email_from': 'omar@exploit-consult.com',
                #     'email_to': 'exploitconsult2022@gmail.com',
                #
                # }

                mail_context = {

                    'email_to': destinataires,

                }

                mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True)

                # notification_ids = [(0, 0,
                #                      {
                #                          'res_partner_id': self.env.user.partner_id.id,
                #                          'notification_type': 'inbox'
                #                      }
                #                      )]
                # #users_id = self.env['res.users'].search([('notification', '=', True)])
                # users_id = self.env['res.users'].search([])
                # list_ids = []
                # if users_id:
                #     for user in users_id:
                #         list_ids.append(user.id)
                # channel_id = self.env.ref('custom_helpdesk.mail_channel_id')
                # _logger.info('*************** channel_id %s', channel_id)
                # dbname = self.env.cr.dbname
                # base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                # base_url += '/web?db=%s#id=%d&view_type=form&model=%s' % (dbname, self.id, self._name)
                # notification_ids = [(0, 0,
                #                      {
                #                          'res_partner_id': self.env.user.partner_id.id,
                #                          'notification_type': 'inbox'
                #                      }
                #                      )]
                # channel_id.message_post(author_id=self.env.user.partner_id.id,
                #                         body=(
                #                                     f"le statut de la tâche " + self.name + " est devenu " + self.stage_id.name + "<a href='" + base_url + "'>Ticket</a"),
                #                         message_type='notification',
                #                         subtype_xmlid="mail.mt_comment",
                #                         notification_ids=notification_ids,
                #                         partner_ids=list_ids,
                #                         notify_by_email=False,
                #                         )

                # channel_id.write({'ticket_id': self.id})




            elif self.stage_id.etape == 'preparation_coordinateur_it':
                # _logger.info('*************** preparation_coordinateur_it %s', self.stage_id.etape)
                mail_template = self.env.ref('custom_helpdesk.email_template_coordinateur_it')

                mail_context = {

                    'email_to': destinataires,

                }

                mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True)

                #channel_id = self.env.ref('custom_helpdesk.mail_channel_id')
                #_logger.info('*************** channel_id %s', channel_id)
                #users_id = self.env['res.users'].search([('notification', '=', True)])
                #users_id = self.env['res.users'].search([])
                #list_ids = []
                #if users_id:
                    #for user in users_id:
                        #list_ids.append(user.id)


                #notification_ids = [(0, 0,
                                     #{
                                         #'res_partner_id': self.env.user.partner_id.id,
                                         #'notification_type': 'inbox'
                                     #}
                                     #)]
                #channel_id.message_post(author_id=self.env.user.partner_id.id,
                                        #body=( f"le statut de la tâche " + self.name + " est devenu " + self.stage_id.name+ "<a href='"+base_url+"'>Ticket</a"),
                                        #message_type='notification',
                                        #subtype_xmlid="mail.mt_comment",
                                        #notification_ids=notification_ids,
                                        #partner_ids=list_ids,
                                        #notify_by_email=False,
                                        #)
                #channel_id.write({'ticket_id': self.id})





            # elif self.stage_id.etape == 'traitement_manager':
            #     # _logger.info('*************** email_template_bylink %s', self.stage_id.etape)
            #     mail_template = self.env.ref('custom_helpdesk.email_template_traitement_manager')

            #     mail_context = {

            #         'email_to': destinataires,
            #         'body_html': f"vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a" +" à remplir : "

            #     }

            #     mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True)

                # notification_ids = [(0, 0,
                #                      {
                #                          'res_partner_id': self.env.user.partner_id.id,
                #                          'notification_type': 'inbox'
                #                      }
                #                      )]
                # channel_id = self.env.ref('custom_helpdesk.mail_channel_id')
                # #users_id = self.env['res.users'].search([('notification', '=', True)])
                # users_id = self.env['res.users'].search([])
                # list_ids = []
                # if users_id:
                #     for user in users_id:
                #         list_ids.append(user.id)
                # channel_id.message_post(author_id=self.env.user.partner_id.id,
                #                         body=(
                #                                 f"le statut de la tâche " + self.name + " est devenu " + self.stage_id.name + "<a href='" + base_url + "'>Ticket</a"),
                #                         message_type='notification',
                #                         subtype_xmlid="mail.mt_comment",
                #                         notification_ids=notification_ids,
                #                         partner_ids=list_ids,
                #                         notify_by_email=False,
                #                         )
