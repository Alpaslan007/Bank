import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Classe principale
class ALBank:
    def __init__(self, root):
        self.root = root
        self.root.title("ALBank - Votre Banque Digitale")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f2f5")

        self.user_id = None
        self.nom_user = ""

        #Style du tableau
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#002d72", foreground="white")

        #Initialisation de la base de donnees
        self.init_db()
        self.ecran_connexion()

    # Création des tables SQL
    def init_db(self):
        self.conn = sqlite3.connect("albank.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS membres (id INTEGER PRIMARY KEY, nom TEXT UNIQUE, mdp TEXT)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS flux (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, titre TEXT, montant REAL, categorie TEXT)")
        self.conn.commit()

    def vider_ecran(self):
        for w in self.root.winfo_children(): w.destroy()

    #Connexion
    def ecran_connexion(self):
        self.vider_ecran()
        # En-tête bleu avec le logo/titre
        header = tk.Frame(self.root, bg="#002d72", height=150)
        header.pack(fill="x")
        tk.Label(header, text="ALBank", font=("Arial", 40, "bold"), bg="#002d72", fg="white").pack(pady=40)

        #formulaire
        box = tk.Frame(self.root, bg="white", padx=50, pady=50, highlightbackground="#ccc", highlightthickness=1)
        box.place(relx=0.5, rely=0.6, anchor="center")

        tk.Label(box, text="Identifiant", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.e_login = tk.Entry(box, font=("Arial", 12), width=30, bg="#f0f2f5", bd=0)
        self.e_login.pack(pady=(5, 15), ipady=8)

        tk.Label(box, text="Code PIN", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.e_pass = tk.Entry(box, font=("Arial", 12), width=30, bg="#f0f2f5", bd=0, show="*") # show="*" pour masquer le mot de passe
        self.e_pass.pack(pady=(5, 20), ipady=8)

        #Boutons connexion et inscription
        tk.Button(box, text="Se connecter", bg="#002d72", fg="white", width=30, bd=0, command=self.login).pack(pady=5, ipady=10)
        tk.Button(box, text="Créer un profil", bg="#4caf50", fg="white", width=30, bd=0, command=self.register).pack(pady=5, ipady=10)

    # Verification des identifiants
    def login(self):
        nom, mdp = self.e_login.get(), self.e_pass.get()
        self.cur.execute("SELECT id FROM membres WHERE nom=? AND mdp=?", (nom, mdp))
        res = self.cur.fetchone()
        if res:
            self.user_id, self.nom_user = res[0], nom
            self.interface_principale()
        else:
            messagebox.showerror("Erreur", "Identifiant ou code PIN incorrect")

    # Inscription d'un nouvel utilisateur
    def register(self):
        nom, mdp = self.e_login.get(), self.e_pass.get()
        if nom and mdp:
            try:
                self.cur.execute("INSERT INTO membres (nom, mdp) VALUES (?, ?)", (nom, mdp))
                self.conn.commit()
                messagebox.showinfo("ALBank", "Compte créé avec succès !")
            except:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur est déjà pris")

    def interface_principale(self):
        self.vider_ecran()

        #Barre de navigation
        nav = tk.Frame(self.root, bg="#002d72", height=60)
        nav.pack(fill="x")
        tk.Label(nav, text=f"Bonjour, {self.nom_user}", fg="white", bg="#002d72", font=("Arial", 12)).pack(side="left", padx=20)
        tk.Button(nav, text="Support", bg="#1a4b8c", fg="white", bd=0, command=self.fenetre_contact).pack(side="right", padx=10, pady=15)
        tk.Button(nav, text="Déconnexion", bg="#d32f2f", fg="white", bd=0, command=self.ecran_connexion).pack(side="right", padx=10)

        #Zone centrale divisée en deux colonnes
        corps = tk.Frame(self.root, bg="#f0f2f1")
        corps.pack(fill="both", expand=True, padx=30, pady=20)
        gauche = tk.Frame(corps, bg="#f0f2f5")
        gauche.pack(side="left", fill="both", expand=True)

        #Carte du solde
        self.card = tk.Frame(gauche, bg="white", padx=20, pady=20, highlightbackground="#ddd", highlightthickness=1)
        self.card.pack(fill="x", pady=(0, 20))
        tk.Label(self.card, text="SOLDE TOTAL", bg="white", fg="grey", font=("Arial", 10, "bold")).pack(anchor="w")
        self.lbl_solde = tk.Label(self.card, text="0.00 €", bg="white", font=("Arial", 30, "bold"))
        self.lbl_solde.pack(anchor="w")

        #Ajouter une transaction
        form = tk.LabelFrame(gauche, text=" Nouvelle Transaction ", bg="white", padx=20, pady=20)
        form.pack(fill="x")

        tk.Label(form, text="Description :", bg="white").grid(row=0, column=0, sticky="w")
        self.en_titre = tk.Entry(form, bg="#f0f2f5", bd=0)
        self.en_titre.grid(row=0, column=1, pady=10, padx=10, ipady=5)

        tk.Label(form, text="Montant (€) :", bg="white").grid(row=1, column=0, sticky="w")
        self.en_montant = tk.Entry(form, bg="#f0f2f5", bd=0)
        self.en_montant.grid(row=1, column=1, pady=10, padx=10, ipady=5)

        #Boutons pour choisir Revenu, Depense ou Supprimer
        btn_box = tk.Frame(form, bg="white")
        btn_box.grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(btn_box, text="+ Revenu", bg="#4caf50", fg="white", width=12, command=lambda: self.ajouter("Revenu")).pack(side="left", padx=5)
        tk.Button(btn_box, text="- Dépense", bg="#f44336", fg="white", width=12, command=lambda: self.ajouter("Dépense")).pack(side="left", padx=5)
        tk.Button(btn_box, text="Supprimer", bg="#757575", fg="white", width=12, command=self.supprimer).pack(side="left", padx=5)

        #Graphique analytique
        droite = tk.Frame(corps, bg="white", highlightbackground="#ddd", highlightthickness=1)
        droite.pack(side="right", fill="both", expand=True, padx=(30, 0))
        tk.Label(droite, text="Répartition des flux", bg="white", font=("Arial", 12, "bold")).pack(pady=15)
        self.zone_graph = tk.Frame(droite, bg="white")
        self.zone_graph.pack(fill="both", expand=True)

        #Historique en forme de tableau
        tk.Label(self.root, text="Historique des transactions", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(anchor="w", padx=30)
        self.table = ttk.Treeview(self.root, columns=("ID", "Nom", "Type", "Prix"), show="headings", height=8)
        self.table.heading("ID", text="N°"); self.table.column("ID", width=50)
        self.table.heading("Nom", text="Description")
        self.table.heading("Type", text="Catégorie")
        self.table.heading("Prix", text="Montant (€)")
        self.table.pack(fill="x", padx=30, pady=10)

        self.maj_vue()

    #Enregistre une nouvelle transaction
    def ajouter(self, cat):
        try:
            t, m = self.en_titre.get(), float(self.en_montant.get())
            if t == "": raise ValueError
            self.cur.execute("INSERT INTO flux (user_id, titre, montant, categorie) VALUES (?,?,?,?)",
                             (self.user_id, t, m, cat))
            self.conn.commit()
            #Reset
            self.en_titre.delete(0, 'end'); self.en_montant.delete(0, 'end')
            self.maj_vue()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide")

    #Supprime une transaction selectionne dans le tableau
    def supprimer(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("ALBank", "Veuillez sélectionner une ligne")
            return

        id_db = self.table.item(sel)['values'][0]
        if messagebox.askyesno("Confirmation", "Supprimer définitivement cette opération ?"):
            self.cur.execute("DELETE FROM flux WHERE id=?", (id_db,))
            self.conn.commit()
            self.maj_vue()

    #Mise a jour du tableau
    def maj_vue(self):
        for i in self.table.get_children(): self.table.delete(i)
        self.cur.execute("SELECT id, titre, categorie, montant FROM flux WHERE user_id=?", (self.user_id,))
        for r in self.cur.fetchall(): self.table.insert("", "end", values=r)

        #Calcul des totaux
        self.cur.execute("SELECT SUM(montant) FROM flux WHERE user_id=? AND categorie='Revenu'", (self.user_id,))
        rev = self.cur.fetchone()[0] or 0
        self.cur.execute("SELECT SUM(montant) FROM flux WHERE user_id=? AND categorie='Dépense'", (self.user_id,))
        dep = self.cur.fetchone()[0] or 0
        solde = rev - dep

        #changement de couleur si en desous 100 EUR
        self.lbl_solde.config(text=f"{solde:.2f} €", fg="#002d72" if solde >= 100 else "#d32f2f")
        if solde < 100:
            messagebox.showwarning("Alerte Budget", "Attention, votre solde est inférieur à 100€ !")

        #Génération du graphique
        for w in self.zone_graph.winfo_children(): w.destroy()
        if rev > 0 or dep > 0:
            fig, ax = plt.subplots(figsize=(4, 4), dpi=80)
            ax.pie([rev, dep], labels=["Revenu", "Dépense"], colors=["#4caf50", "#f44336"], autopct='%1.1f%%', startangle=140)
            canvas = FigureCanvasTkAgg(fig, master=self.zone_graph)
            canvas.draw()
            canvas.get_tk_widget().pack()

    #fenêtre pour le support client
    def fenetre_contact(self):
        win = tk.Toplevel(self.root)
        win.title("Support Client")
        win.geometry("350x300")
        win.configure(bg="white")
        tk.Label(win, text="Besoin d'aide ?", font=("Arial", 14, "bold"), bg="white", fg="#002d72").pack(pady=20)
        tk.Label(win, text="📞 +32 489 53 98 33\n📧 alpasian.kara@isagosselies.be\n📍 6040 Jumet, Belgique", bg="white").pack()
        tk.Button(win, text="Fermer", command=win.destroy, bg="#002d72", fg="white", bd=0).pack(pady=30, ipady=5, ipadx=10)

if __name__ == "__main__":
    root = tk.Tk()
    ALBank(root)
    root.mainloop()
