import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime


class ALBank:
    def __init__(self, root):
        self.root = root
        self.root.title("ALBank - Votre Banque Digitale")
        self.root.geometry("1200x900")
        self.root.configure(bg="#f0f2f5")

        self.utilisateur_id = None
        self.nom_utilisateur = ""

        # Connexion a la base de donnees
        self.connexion = sqlite3.connect("albank.db")
        self.cursor = self.connexion.cursor()

        # Je cree les tables
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS utilisateurs (id INTEGER PRIMARY KEY, nom TEXT UNIQUE, mot_de_passe TEXT)")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                utilisateur_id INTEGER, 
                description TEXT, 
                montant REAL, 
                type TEXT,
                categorie TEXT,
                date TEXT
            )
        """)
        self.connexion.commit()

        # J'affiche l'ecran de connexion
        self.ecran_connexion()

    # Fonction pour vider l'ecran
    def vider(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Ecran de connexion
    def ecran_connexion(self):
        self.vider()

        # En tete
        en_tete = tk.Frame(self.root, bg="#002d72", height=150)
        en_tete.pack(fill="x")
        tk.Label(en_tete, text="ALBank", font=("Arial", 40, "bold"), bg="#002d72", fg="white").pack(pady=40)

        # Cadre du formulaire
        cadre = tk.Frame(self.root, bg="white", padx=50, pady=50)
        cadre.place(relx=0.5, rely=0.6, anchor="center")

        tk.Label(cadre, text="Identifiant", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.champ_login = tk.Entry(cadre, font=("Arial", 12), width=30, bg="#f0f2f5")
        self.champ_login.pack(pady=(5, 15), ipady=8)

        tk.Label(cadre, text="Code PIN", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.champ_mdp = tk.Entry(cadre, font=("Arial", 12), width=30, bg="#f0f2f5", show="*")
        self.champ_mdp.pack(pady=(5, 20), ipady=8)

        tk.Button(cadre, text="Se connecter", bg="#002d72", fg="white", width=30, command=self.se_connecter).pack(
            pady=5, ipady=10)
        tk.Button(cadre, text="Creer un compte", bg="#4caf50", fg="white", width=30, command=self.creer_compte).pack(
            pady=5, ipady=10)

    # Connexion
    def se_connecter(self):
        nom = self.champ_login.get()
        mdp = self.champ_mdp.get()

        self.cursor.execute("SELECT id FROM utilisateurs WHERE nom=? AND mot_de_passe=?", (nom, mdp))
        resultat = self.cursor.fetchone()

        if resultat:
            self.utilisateur_id = resultat[0]
            self.nom_utilisateur = nom
            self.accueil()
        else:
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect")

    # Creation de compte
    def creer_compte(self):
        nom = self.champ_login.get()
        mdp = self.champ_mdp.get()

        if nom and mdp:
            try:
                self.cursor.execute("INSERT INTO utilisateurs (nom, mot_de_passe) VALUES (?, ?)", (nom, mdp))
                self.connexion.commit()
                messagebox.showinfo("Bravo", "Compte cree avec succes !")
            except:
                messagebox.showerror("Erreur", "Ce nom est deja utilise")
        else:
            messagebox.showerror("Erreur", "Remplis tous les champs")

    # Page principale
    def accueil(self):
        self.vider()

        # Barre du haut
        barre = tk.Frame(self.root, bg="#002d72", height=60)
        barre.pack(fill="x")
        tk.Label(barre, text=f"Bonjour {self.nom_utilisateur}", fg="white", bg="#002d72", font=("Arial", 12)).pack(
            side="left", padx=20)

        tk.Button(barre, text="Stats par mois", bg="#ff9800", fg="white", command=self.stats_mois).pack(side="right",
                                                                                                        padx=10,
                                                                                                        pady=15)
        tk.Button(barre, text="Support", bg="#1a4b8c", fg="white", command=self.support).pack(side="right", padx=10,
                                                                                              pady=15)
        tk.Button(barre, text="Deconnexion", bg="#d32f2f", fg="white", command=self.ecran_connexion).pack(side="right",
                                                                                                          padx=10)

        # Partie gauche
        corps = tk.Frame(self.root, bg="#f0f2f1")
        corps.pack(fill="both", expand=True, padx=30, pady=20)

        gauche = tk.Frame(corps, bg="#f0f2f5")
        gauche.pack(side="left", fill="both", expand=True)

        # Carte du solde
        carte = tk.Frame(gauche, bg="white", padx=20, pady=20)
        carte.pack(fill="x", pady=(0, 20))
        tk.Label(carte, text="MON SOLDE", bg="white", fg="grey", font=("Arial", 10, "bold")).pack(anchor="w")
        self.label_solde = tk.Label(carte, text="0.00 €", bg="white", font=("Arial", 30, "bold"))
        self.label_solde.pack(anchor="w")

        # Formulaire pour ajouter
        formulaire = tk.LabelFrame(gauche, text=" Nouvelle transaction ", bg="white", padx=20, pady=20)
        formulaire.pack(fill="x")

        tk.Label(formulaire, text="Description :", bg="white").grid(row=0, column=0, sticky="w")
        self.champ_description = tk.Entry(formulaire, bg="#f0f2f5")
        self.champ_description.grid(row=0, column=1, pady=10, padx=10, ipady=5)

        tk.Label(formulaire, text="Montant (€) :", bg="white").grid(row=1, column=0, sticky="w")
        self.champ_montant = tk.Entry(formulaire, bg="#f0f2f5")
        self.champ_montant.grid(row=1, column=1, pady=10, padx=10, ipady=5)

        tk.Label(formulaire, text="Categorie :", bg="white").grid(row=2, column=0, sticky="w")
        self.champ_categorie = ttk.Combobox(formulaire,
                                            values=["Alimentation", "Transport", "Loisirs", "Shopping", "Sante",
                                                    "Factures", "Autre"], width=20)
        self.champ_categorie.grid(row=2, column=1, pady=10, padx=10)
        self.champ_categorie.set("Autre")

        # Boutons
        cadre_boutons = tk.Frame(formulaire, bg="white")
        cadre_boutons.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(cadre_boutons, text="+ Revenu", bg="#4caf50", fg="white", width=12,
                  command=lambda: self.ajouter("Revenu")).pack(side="left", padx=5)
        tk.Button(cadre_boutons, text="- Depense", bg="#f44336", fg="white", width=12,
                  command=lambda: self.ajouter("Depense")).pack(side="left", padx=5)
        tk.Button(cadre_boutons, text="Modifier", bg="#2196f3", fg="white", width=12, command=self.modifier).pack(
            side="left", padx=5)
        tk.Button(cadre_boutons, text="Supprimer", bg="#757575", fg="white", width=12, command=self.supprimer).pack(
            side="left", padx=5)

        # Graphique (a droite)
        droite = tk.Frame(corps, bg="white")
        droite.pack(side="right", fill="both", expand=True, padx=(30, 0))
        tk.Label(droite, text="Mes revenus vs depenses", bg="white", font=("Arial", 12, "bold")).pack(pady=15)

        self.zone_graphique = tk.Frame(droite, bg="white", height=300, width=400)
        self.zone_graphique.pack(fill="both", expand=True, padx=20, pady=10)

        # Tableau des transactions
        tk.Label(self.root, text="Historique", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(anchor="w", padx=30)

        self.tableau = ttk.Treeview(self.root, columns=("ID", "Description", "Type", "Categorie", "Montant", "Date"),
                                    show="headings", height=8)
        self.tableau.heading("ID", text="N°")
        self.tableau.heading("Description", text="Description")
        self.tableau.heading("Type", text="Type")
        self.tableau.heading("Categorie", text="Categorie")
        self.tableau.heading("Montant", text="Montant")
        self.tableau.heading("Date", text="Date")
        self.tableau.pack(fill="x", padx=30, pady=10)

        # Je charge les donnees
        self.rafraichir()

    # Ajouter une transaction
    def ajouter(self, type_transaction):
        try:
            description = self.champ_description.get()
            montant = float(self.champ_montant.get())
            categorie = self.champ_categorie.get()
            date_actuelle = datetime.now().strftime("%Y-%m-%d")

            if description == "":
                messagebox.showerror("Erreur", "Ajoute une description")
                return

            self.cursor.execute("""
                INSERT INTO transactions (utilisateur_id, description, montant, type, categorie, date) 
                VALUES (?,?,?,?,?,?)
            """, (self.utilisateur_id, description, montant, type_transaction, categorie, date_actuelle))
            self.connexion.commit()

            # Je vide les champs
            self.champ_description.delete(0, 'end')
            self.champ_montant.delete(0, 'end')
            self.champ_categorie.set("Autre")

            self.rafraichir()
            messagebox.showinfo("Succes", "Transaction ajoutee !")

        except:
            messagebox.showerror("Erreur", "Le montant doit etre un nombre")

    # Modifier une transaction
    def modifier(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Selectionne une transaction")
            return

        # Je recupere les infos
        item = self.tableau.item(selection[0])
        valeurs = item['values']
        id_transaction = valeurs[0]
        ancienne_description = valeurs[1]
        ancien_type = valeurs[2]
        ancienne_categorie = valeurs[3]
        ancien_montant = valeurs[4]

        # Nouvelle fenetre
        popup = tk.Toplevel(self.root)
        popup.title("Modifier")
        popup.geometry("400x450")
        popup.configure(bg="white")

        tk.Label(popup, text="Modifier la transaction", font=("Arial", 16, "bold"), bg="white", fg="#002d72").pack(
            pady=20)

        # Formulaire
        cadre = tk.Frame(popup, bg="white", padx=30, pady=20)
        cadre.pack(fill="both", expand=True)

        tk.Label(cadre, text="Description :", bg="white").pack(anchor="w", pady=(0, 5))
        entree_desc = tk.Entry(cadre, font=("Arial", 12), bg="#f0f2f5")
        entree_desc.insert(0, ancienne_description)
        entree_desc.pack(fill="x", pady=(0, 15), ipady=8)

        tk.Label(cadre, text="Montant :", bg="white").pack(anchor="w", pady=(0, 5))
        entree_montant = tk.Entry(cadre, font=("Arial", 12), bg="#f0f2f5")
        entree_montant.insert(0, ancien_montant)
        entree_montant.pack(fill="x", pady=(0, 15), ipady=8)

        tk.Label(cadre, text="Categorie :", bg="white").pack(anchor="w", pady=(0, 5))
        combo_cat = ttk.Combobox(cadre, values=["Alimentation", "Transport", "Loisirs", "Shopping", "Sante", "Factures",
                                                "Autre"], width=20)
        combo_cat.set(ancienne_categorie)
        combo_cat.pack(fill="x", pady=(0, 20))

        tk.Label(cadre, text="Type :", bg="white").pack(anchor="w", pady=(0, 5))
        choix_type = tk.StringVar(value=ancien_type)
        tk.Radiobutton(cadre, text="Revenu", variable=choix_type, value="Revenu", bg="white").pack(anchor="w", padx=20)
        tk.Radiobutton(cadre, text="Depense", variable=choix_type, value="Depense", bg="white").pack(anchor="w",
                                                                                                     padx=20)

        def sauvegarder():
            try:
                nouvelle_desc = entree_desc.get()
                nouveau_montant = float(entree_montant.get())
                nouvelle_cat = combo_cat.get()
                nouveau_type = choix_type.get()

                self.cursor.execute("""
                    UPDATE transactions 
                    SET description=?, montant=?, categorie=?, type=?
                    WHERE id=? AND utilisateur_id=?
                """, (nouvelle_desc, nouveau_montant, nouvelle_cat, nouveau_type, id_transaction, self.utilisateur_id))
                self.connexion.commit()

                messagebox.showinfo("Succes", "Transaction modifiee !")
                popup.destroy()
                self.rafraichir()
            except:
                messagebox.showerror("Erreur", "Montant invalide")

        tk.Button(popup, text="Sauvegarder", bg="#4caf50", fg="white", command=sauvegarder).pack(pady=20)

    # Supprimer
    def supprimer(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Selectionne une transaction")
            return

        if messagebox.askyesno("Confirmation", "Supprimer ?"):
            id_transaction = self.tableau.item(selection[0])['values'][0]
            self.cursor.execute("DELETE FROM transactions WHERE id=?", (id_transaction,))
            self.connexion.commit()
            self.rafraichir()

    # Rafraichir l'affichage
    def rafraichir(self):
        # Vider le tableau
        for ligne in self.tableau.get_children():
            self.tableau.delete(ligne)

        # Remplir le tableau
        self.cursor.execute(
            "SELECT id, description, type, categorie, montant, date FROM transactions WHERE utilisateur_id=?",
            (self.utilisateur_id,))
        for transaction in self.cursor.fetchall():
            self.tableau.insert("", "end", values=transaction)

        # Calculer le solde
        self.cursor.execute("SELECT SUM(montant) FROM transactions WHERE utilisateur_id=? AND type='Revenu'",
                            (self.utilisateur_id,))
        revenus = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT SUM(montant) FROM transactions WHERE utilisateur_id=? AND type='Depense'",
                            (self.utilisateur_id,))
        depenses = self.cursor.fetchone()[0] or 0

        solde = revenus - depenses

        # Changer la couleur si besoin
        if solde < 100:
            self.label_solde.config(text=f"{solde:.2f} €", fg="#d32f2f")
            if solde >= 0:
                messagebox.showwarning("Alerte", "Solde inferieur a 100€")
        else:
            self.label_solde.config(text=f"{solde:.2f} €", fg="#002d72")

        # Dessiner le graphique
        self.dessiner_graphique(revenus, depenses)

    # Graphique fait maison
    def dessiner_graphique(self, revenus, depenses):
        for widget in self.zone_graphique.winfo_children():
            widget.destroy()

        if revenus == 0 and depenses == 0:
            tk.Label(self.zone_graphique, text="Ajoute des transactions", bg="white", font=("Arial", 12)).pack(
                expand=True)
            return

        canvas = tk.Canvas(self.zone_graphique, bg="white")
        canvas.pack(fill="both", expand=True)

        # Dimensions
        max_valeur = max(revenus, depenses)
        if max_valeur == 0:
            max_valeur = 1

        hauteur_max = 200
        largeur_barre = 80
        x_revenu = 100
        x_depense = 250
        y_base = 250

        # Calculer les hauteurs
        hauteur_revenu = (revenus / max_valeur) * hauteur_max
        hauteur_depense = (depenses / max_valeur) * hauteur_max

        # Dessiner les barres
        canvas.create_rectangle(x_revenu, y_base - hauteur_revenu, x_revenu + largeur_barre, y_base, fill="#4caf50")
        canvas.create_rectangle(x_depense, y_base - hauteur_depense, x_depense + largeur_barre, y_base, fill="#f44336")

        # Ajouter les textes
        canvas.create_text(x_revenu + 40, y_base - hauteur_revenu - 10, text=f"{revenus:.0f}€", font=("Arial", 10))
        canvas.create_text(x_depense + 40, y_base - hauteur_depense - 10, text=f"{depenses:.0f}€", font=("Arial", 10))
        canvas.create_text(x_revenu + 40, y_base + 20, text="Revenus", font=("Arial", 10, "bold"))
        canvas.create_text(x_depense + 40, y_base + 20, text="Depenses", font=("Arial", 10, "bold"))

    # Statistiques par mois
    def stats_mois(self):
        popup = tk.Toplevel(self.root)
        popup.title("Statistiques par mois")
        popup.geometry("600x500")
        popup.configure(bg="white")

        tk.Label(popup, text="Analyse par mois", font=("Arial", 16, "bold"), bg="white", fg="#002d72").pack(pady=20)

        # Recuperer les mois disponibles
        self.cursor.execute("""
            SELECT DISTINCT SUBSTR(date, 1, 7) as mois 
            FROM transactions 
            WHERE utilisateur_id=?
            ORDER BY mois DESC
        """, (self.utilisateur_id,))

        mois_liste = [row[0] for row in self.cursor.fetchall()]

        if not mois_liste:
            tk.Label(popup, text="Aucune transaction", bg="white").pack(pady=50)
        else:
            tk.Label(popup, text="Choisis un mois :", bg="white").pack()
            mois_var = tk.StringVar(value=mois_liste[0])
            mois_menu = ttk.Combobox(popup, textvariable=mois_var, values=mois_liste, width=20)
            mois_menu.pack(pady=10)

            cadre_resultats = tk.Frame(popup, bg="white")
            cadre_resultats.pack(fill="both", expand=True, padx=20, pady=20)

            def afficher():
                for w in cadre_resultats.winfo_children():
                    w.destroy()

                mois = mois_var.get()

                # Calculer les totaux du mois
                self.cursor.execute(
                    "SELECT SUM(montant) FROM transactions WHERE utilisateur_id=? AND type='Revenu' AND SUBSTR(date,1,7)=?",
                    (self.utilisateur_id, mois))
                revenus = self.cursor.fetchone()[0] or 0

                self.cursor.execute(
                    "SELECT SUM(montant) FROM transactions WHERE utilisateur_id=? AND type='Depense' AND SUBSTR(date,1,7)=?",
                    (self.utilisateur_id, mois))
                depenses = self.cursor.fetchone()[0] or 0

                # Afficher les infos
                tk.Label(cadre_resultats, text=f"Mois : {mois}", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
                tk.Label(cadre_resultats, text=f"Revenus : {revenus:.2f} €", bg="white", fg="green").pack()
                tk.Label(cadre_resultats, text=f"Depenses : {depenses:.2f} €", bg="white", fg="red").pack()
                tk.Label(cadre_resultats, text=f"Solde : {revenus - depenses:.2f} €", bg="white",
                         font=("Arial", 10, "bold")).pack(pady=10)

                # Detail par categorie
                tk.Label(cadre_resultats, text="\nDepenses par categorie :", bg="white",
                         font=("Arial", 10, "bold")).pack()

                self.cursor.execute("""
                    SELECT categorie, SUM(montant) 
                    FROM transactions 
                    WHERE utilisateur_id=? AND type='Depense' AND SUBSTR(date,1,7)=?
                    GROUP BY categorie
                """, (self.utilisateur_id, mois))

                categories = self.cursor.fetchall()
                if categories:
                    for cat, montant in categories:
                        tk.Label(cadre_resultats, text=f"{cat} : {montant:.2f} €", bg="white").pack(anchor="w", padx=20)
                else:
                    tk.Label(cadre_resultats, text="Aucune depense", bg="white").pack()

            tk.Button(popup, text="Afficher", bg="#002d72", fg="white", command=afficher).pack(pady=10)
            afficher()

        tk.Button(popup, text="Fermer", command=popup.destroy).pack(pady=20)

    # Support
    def support(self):
        popup = tk.Toplevel(self.root)
        popup.title("Support")
        popup.geometry("400x350")
        popup.configure(bg="white")

        tk.Label(popup, text="Besoin d'aide ?", font=("Arial", 16, "bold"), bg="white", fg="#002d72").pack(pady=20)
        tk.Label(popup, text="📞 +32 489 53 98 33\n📧 alpasian.kara@isagosselies.be\n📍 6040 Jumet, Belgique",
                 bg="white", font=("Arial", 11)).pack(pady=20)
        tk.Label(popup, text="Lundi - Vendredi: 9h - 17h", bg="white", font=("Arial", 10), fg="grey").pack()
        tk.Button(popup, text="Fermer", command=popup.destroy, bg="#002d72", fg="white").pack(pady=20)


# Lancement
if __name__ == "__main__":
    fenetre = tk.Tk()
    app = ALBank(fenetre)
    fenetre.mainloop()
