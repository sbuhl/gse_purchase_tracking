# Purchase Tracking

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

## Purchase Tracking columns

1. Name: nom de la tâche (caché par défaut)
2. Confirmation Date: Date de confirmation chez Fournisseur Final
3. Final Supplier
4. PO Ref: Purchase chez le Fournisseur Final
5. PO Status: état chez le fourn final (caché par défaut)
6. Billing Status
7. Conf. Date Atimex 
8. Indirect Supplier - Atimex (99% des cas Atimex, caché par défaut)
9. PO Atimex
10. PO Status Atimex (caché par défaut) 
11. Scheduled Date
12. Atimex Reception Status: Réception chez Atimex/Herfurth, donc du fournisseur final vers Atimex
13. Final Destination
14. Final Destination Scheduled Date
15. Final Destination Reception Status
16. Direct Purchase (caché par défaut)
17. Final Destination Reception Date 
18. Forwarder (defined on BL)
19. Forwarder Reference
20. Forwarder Method (seafreight (green) | airfreight (blue))
21. Delivery Step (only field editable in tree view)
22. Departure Date
