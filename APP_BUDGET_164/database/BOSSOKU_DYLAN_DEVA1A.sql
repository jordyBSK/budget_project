-- Requêtes SQL pour la base de données BOSSOKU_DYLAN_DEVA1A_BUDGET_164_2024

-- 1. Sélectionner tous les utilisateurs
SELECT * FROM t_utilisateur;

-- 2. Sélectionner tous les comptes
SELECT * FROM t_compte;

-- 3. Sélectionner tous les revenus
SELECT * FROM t_revenu;

-- 4. Sélectionner tous les dépenses
SELECT * FROM t_depense;

-- 5. Sélectionner tous les utilisateurs et leurs revenus
SELECT u.nom_utilisateur, u.prenom_utilisateur, r.*
FROM t_utilisateur u
         JOIN t_revenu r ON u.id_utilisateur = r.id_utilisateur;

-- 6. Sélectionner tous les utilisateurs et leurs dépenses
SELECT u.nom_utilisateur, u.prenom_utilisateur, d.*
FROM t_utilisateur u
         JOIN t_depense d ON u.id_utilisateur = d.id_utilisateur;

-- 7. Sélectionner tous les utilisateurs et leurs comptes
SELECT u.nom_utilisateur, u.prenom_utilisateur, c.*
FROM t_utilisateur u
         JOIN t_compte c ON u.id_utilisateur = c.id_utilisateur;

-- 8. Sélectionner tous les comptes avec leurs utilisateurs associés
SELECT c.*, u.nom_utilisateur, u.prenom_utilisateur
FROM t_compte c
         JOIN t_utilisateur u ON c.id_utilisateur = u.id_utilisateur;

-- 9. Sélectionner tous les revenus et leurs utilisateurs associés
SELECT r.*, u.nom_utilisateur, u.prenom_utilisateur
FROM t_revenu r
         JOIN t_utilisateur u ON r.id_utilisateur = u.id_utilisateur;

-- 10. Sélectionner tous les dépenses et leurs utilisateurs associés
SELECT d.*, u.nom_utilisateur, u.prenom_utilisateur
FROM t_depense d
         JOIN t_utilisateur u ON d.id_utilisateur = u.id_utilisateur;

-- 11. Sélectionner tous les revenus avec leur compte associé
SELECT r.*, c.nom_compte
FROM t_revenu r
         JOIN t_compte c ON r.id_compte = c.id_compte;

-- 12. Sélectionner tous les dépenses avec leur compte associé
SELECT d.*, c.nom_compte
FROM t_depense d
         JOIN t_compte c ON d.id_compte = c.id_compte;

-- 13. Sélectionner tous les revenus avec leur catégorie associée
SELECT r.*, cat.nom_categorie
FROM t_revenu r
         JOIN t_depense cat ON r.id_categorie = cat.id_categorie;

-- 14. Sélectionner tous les dépenses avec leur catégorie associée
SELECT d.*, cat.nom_categorie
FROM t_depense d
         JOIN t_depense cat ON d.id_categorie = cat.id_categorie;

-- 15. Sélectionner le montant total des revenus par utilisateur
SELECT u.nom_utilisateur, u.prenom_utilisateur, SUM(r.montant_revenu) AS total_revenu
FROM t_utilisateur u
         JOIN t_revenu r ON u.id_utilisateur = r.id_utilisateur
GROUP BY u.id_utilisateur;

-- 16. Sélectionner le montant total des dépenses par utilisateur
SELECT u.nom_utilisateur, u.prenom_utilisateur, SUM(d.Montant_depense) AS total_depense
FROM t_utilisateur u
         JOIN t_depense d ON u.id_utilisateur = d.id_utilisateur
GROUP BY u.id_utilisateur;

-- 17. Sélectionner le solde de chaque compte
SELECT c.nom_compte,
       SUM(COALESCE(r.montant_revenu, 0)) - SUM(COALESCE(d.Montant_depense, 0)) AS solde
FROM t_compte c
         LEFT JOIN t_revenu r ON c.id_compte = r.id_compte
         LEFT JOIN t_depense d ON c.id_compte = d.id_compte
GROUP BY c.id_compte;

-- 18. Sélectionner les 5 utilisateurs ayant le plus de revenus
SELECT u.nom_utilisateur, u.prenom_utilisateur, SUM(r.montant_revenu) AS total_revenu
FROM t_utilisateur u
         JOIN t_revenu r ON u.id_utilisateur = r.id_utilisateur
GROUP BY u.id_utilisateur
ORDER BY total_revenu DESC
LIMIT 5;

-- 19. Sélectionner les 5 utilisateurs ayant le plus de dépenses
SELECT u.nom_utilisateur, u.prenom_utilisateur, SUM(d.Montant_depense) AS total_depense
FROM t_utilisateur u
         JOIN t_depense d ON u.id_utilisateur = d.id_utilisateur
GROUP BY u.id_utilisateur
ORDER BY total_depense DESC
LIMIT 5;

-- 20. Sélectionner le mois avec le plus de revenus
SELECT YEAR(date_revenu) AS annee, MONTH(date_revenu) AS mois, SUM(montant_revenu) AS total_revenu
FROM t_revenu
GROUP BY YEAR(date_revenu), MONTH(date_revenu)
ORDER BY total_revenu DESC
LIMIT 1;

-- 21. Sélectionner le mois avec le plus de dépenses
SELECT YEAR(date_depense) AS annee, MONTH(date_depense) AS mois, SUM(Montant_depense) AS total_depense
FROM t_depense
GROUP BY YEAR(date_depense), MONTH(date_depense)
ORDER BY total_depense DESC
LIMIT 1;

-- 22. Sélectionner les utilisateurs dont le nom commence par "Doe"
SELECT * FROM t_utilisateur WHERE nom_utilisateur LIKE 'Doe%';

-- 23. Sélectionner les dépenses supérieures à 100€
SELECT * FROM t_depense WHERE Montant_depense > 100;

-- 24. Sélectionner les revenus compris entre 1500€ et 3000€
SELECT * FROM t_revenu WHERE montant_revenu BETWEEN 1500 AND 3000;

-- 25. Sélectionner les dépenses effectuées dans un restaurant
SELECT * FROM t_depense WHERE lieu_depense LIKE '%Restaurant%';

-- 26. Sélectionner les revenus obtenus via un compte courant
SELECT r.* FROM t_revenu r JOIN t_compte c ON r.id_compte = c.id_compte WHERE c.nom_compte LIKE '%courant%';
