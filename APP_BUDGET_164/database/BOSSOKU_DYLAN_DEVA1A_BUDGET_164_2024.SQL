-- Database: BOSSOKU_DYLAN_DEVA1A_BUDGET_164_2024

-- Supprimer la base de données si elle existe
DROP DATABASE IF EXISTS BOSSOKU_DYLAN_DEVA1A_BUDGET_164_2024;

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS BOSSOKU_DYLAN_DEVA1A_BUDGET_164_2024;

-- Sélection de la base de données
USE BOSSOKU_DYLAN_DEVA1A_BUDGET_164_2024;

-- Supprimer les tables si elles existent
DROP TABLE IF EXISTS t_utilisateur_revenus;
DROP TABLE IF EXISTS t_utilisateur_depenses;
DROP TABLE IF EXISTS t_utilisateur_comptes;
DROP TABLE IF EXISTS t_categorie;
DROP TABLE IF EXISTS t_depense;
DROP TABLE IF EXISTS t_revenu;
DROP TABLE IF EXISTS t_compte;
DROP TABLE IF EXISTS t_utilisateur;

-- Table Utilisateurs
CREATE TABLE t_utilisateur
(
    id_utilisateur           INT AUTO_INCREMENT PRIMARY KEY,
    nom_utilisateur          VARCHAR(255),
    prenom_utilisateur       VARCHAR(255),
    email_utilisateur        VARCHAR(255),
    password_utilisateur     VARCHAR(255)
);

-- Table categories de Depenses
CREATE TABLE t_categorie
(
    id_categorie          INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie         VARCHAR(255)
);

-- Table Comptes
CREATE TABLE t_compte
(
    id_compte      INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT,
    nom_compte     VARCHAR(255),
    FOREIGN KEY (id_utilisateur) REFERENCES t_utilisateur (id_utilisateur)
);

-- Table Depenses
CREATE TABLE t_depense
(
    id_depense           INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur       INT,
    id_categorie         INT,
    id_compte            INT,
    Montant_depense      DECIMAL(10, 2),
    date_depense         DATE,
    description_depense  TEXT,
    lieu_depense         VARCHAR(255),
    FOREIGN KEY (id_utilisateur) REFERENCES t_utilisateur (id_utilisateur),
    FOREIGN KEY (id_categorie) REFERENCES t_categorie (id_categorie),
    FOREIGN KEY (id_compte) REFERENCES t_compte(id_compte)
);

-- Table Revenus
CREATE TABLE t_revenu
(
    id_revenu      INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT,
    id_compte      INT,
    montant_revenu DECIMAL(10, 2),
    date_revenu    DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES t_utilisateur (id_utilisateur),
    FOREIGN KEY (id_compte) REFERENCES t_compte (id_compte)
);

-- Table Utilisateur_Comptes
CREATE TABLE t_utilisateur_comptes
(
    id_utilisateur INT,
    id_compte      INT,
    PRIMARY KEY (id_utilisateur, id_compte),
    FOREIGN KEY (id_utilisateur) REFERENCES t_utilisateur (id_utilisateur),
    FOREIGN KEY (id_compte) REFERENCES t_compte (id_compte)
);

-- Table Utilisateur_Depenses
CREATE TABLE t_utilisateur_depenses
(
    id_utilisateur INT,
    id_depense     INT,
    PRIMARY KEY (id_utilisateur, id_depense),
    FOREIGN KEY (id_utilisateur) REFERENCES t_utilisateur (id_utilisateur),
    FOREIGN KEY (id_depense) REFERENCES t_depense (id_depense)
);

-- Table Utilisateur_Revenus
CREATE TABLE t_utilisateur_revenus
(
    id_utilisateur INT,
    id_revenu      INT,
    PRIMARY KEY (id_utilisateur, id_revenu),
    FOREIGN KEY (id_utilisateur) REFERENCES t_utilisateur (id_utilisateur),
    FOREIGN KEY (id_revenu) REFERENCES t_revenu (id_revenu)
);

-- Insertion de données dans la table t_utilisateur
INSERT INTO t_utilisateur (nom_utilisateur, prenom_utilisateur, email_utilisateur, password_utilisateur)
VALUES
    ('Doe', 'John', 'john.doe@example.com', '123456'),
    ('Doe', 'Jane', 'jane.doe@example.com', 'password123'),
    ('Smith', 'Alice', 'alice.smith@example.com', 'alicepwd'),
    ('Brown', 'Bob', 'bob.brown@example.com', 'bobbrown123'),
    ('Johnson', 'Emily', 'emily.johnson@example.com', 'emilypassword');

-- Insertion de données dans la table t_categorie
INSERT INTO t_categorie (nom_categorie)
VALUES
    ('Alimentation'),
    ('Transport'),
    ('Logement'),
    ('Loisirs'),
    ('Santé');

-- Insertion de données dans la table t_compte
INSERT INTO t_compte (id_utilisateur, nom_compte)
VALUES
    (1, 'Compte courant'),
    (2, 'Compte épargne'),
    (3, 'Compte courant'),
    (4, 'Compte épargne'),
    (5, 'Compte courant');

-- Insertion de données dans la table t_depense
INSERT INTO t_depense (id_utilisateur, id_categorie, id_compte, Montant_depense, date_depense, description_depense, lieu_depense)
VALUES
    (1, 1, 1, 50.00, '2024-04-24', 'Déjeuner', 'Restaurant'),
    (2, 2, 2, 30.00, '2024-04-25', 'Essence', 'Station essence'),
    (3, 3, 3, 500.00, '2024-04-26', 'Loyer', 'Appartement'),
    (4, 4, 4, 100.00, '2024-04-27', 'Cinéma', 'Cinéma du coin'),
    (5, 5, 5, 75.00, '2024-04-28', 'Consultation médicale', 'Clinique');

-- Insertion de données dans la table t_revenu
INSERT INTO t_revenu (id_utilisateur, id_compte, montant_revenu, date_revenu)
VALUES
    (1, 1, 2000.00, '2024-04-24'),
    (2, 2, 1500.00, '2024-04-25'),
    (3, 3, 2500.00, '2024-04-26'),
    (4, 4, 3000.00, '2024-04-27'),
    (5, 5, 3500.00, '2024-04-28');

-- Insertion de données supplémentaires dans la table t_utilisateur_comptes
INSERT INTO t_utilisateur_comptes (id_utilisateur, id_compte)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);
