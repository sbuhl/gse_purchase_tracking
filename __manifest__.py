# -*- coding: utf-8 -*-
{
    'name': "Purchase Tracking",

    'summary': """
        Track the localisation of purchases,
        whether it be their geographical location
        their position in the purchasing flow""",

    'description': """
        GoShop, GoShop Energy, Kivu Solutions and Utrade, can make two
        kind of purchases:
        - Direct Purchases
        - Indirect Purchases
        Direct Purchases are done to the final Supplier.
        Indirect Purchases are made throught the belgian company, Atimex

        Direct Purchase Flow is: GoShop -> BYD
        Indirect Purchase Flow is: GoShop -> Atimex -> Victron

        The important information for GoShop is when the marchandise will
        be delivered. That's the reason why we introduce the notion of
        final_supplier and the documents related to it.

        Purchase Process:

        1. Nouveau
            Demandeur:

            - Nom de la tâche:
            - Description: produits souhaités

                Nomenclature: Quantité | [référence] | Nom du produit
                e.g. • 1 | [ABC123] Valve thermostatique

            - Tag Destination: Goma, Kinshasa, Bukavu, etc.
            - Sale Order: lien vers la vente liée. Laisser vide si réappro stock
            - Boule verte: Demande complète, prête à l'analyse du responsable achat

            Responsable achat:
            - si demande claire et compréhensive: Tag Type: Local ou International
            - si demande pas claire: boule rouge + Note dans le chatter

        2. Consolidation (si International)
            Etant donné que les achats internationaux ne sont faits que
            les jeudi, étape de consolidation pour grouper les commandes

            Reponsable achat:
            - Une tâche de consolidation par marque (Victron, Lorentz, etc)
            - Si une tâche consolidation existe, ajouter

        3. Ordre d'achat
            Si Achat Local,

            Si Achat International,
            Loic prend la tâche en vert dans consolidation


        4. Fournisseur Final

        5. Entrepôt réceptionné en attente

        6. Livraison - en transit

        7. Terminé

        8. Refusé

        9. Consolidé

    """,

    'author': "Sébastien Bühl",
    'website': "http://www.buhl.be",

    'category': 'Customizations',
    'version': '0.0.4',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['gse_picking_status', 'project', 'delivery'],

    'data': [       
        'views/views.xml',
        'views/purchase.xml',
    ],
    
}