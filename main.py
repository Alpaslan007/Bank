import json
import os
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SimulateurBudget:
    def __init__(self, root):
        self.root = root
        self.root.title("AlBank")
        self.root.geometry("900x700")
        self.root.configure(bg="#f2f2f2")

        self.fichier_utilisateurs = "utilisateurs.json"
        self.utilisateurs = {}
        self.utilisateur_actuel = None
        self.donnees = {"revenus": [], "depenses": []}
        self.canvas_graphique = None

        self.charger_utilisateurs()
        self.afficher_connexion()

    def charger_utilisateurs(self):
        if not os.path.exists(self.fichier_utilisateurs):
            self.utilisateurs = {}
            return

        try:
            with open(self.fichier_utilisateurs, "r", encoding="utf-8") as fichier:
                self.utilisateurs = json.load(fichier)
        except (json.JSONDecodeError, OSError):
            self.utilisateurs = {}

    def sauvegarder_utilisateurs(self):
        with open(self.fichier_utilisateurs, "w", encoding="utf-8") as fichier:
            json.dump(self.utilisateurs, fichier, indent=2, ensure_ascii=False)

    def vider_fenetre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def creer_champ(self, parent, label, row, show=None):
        tk.Label(parent, text=label, bg="white").grid(row=row, column=0, padx=8, pady=6, sticky="e")
        entree = tk.Entry(parent, width=28, show=show)
        entree.grid(row=row, column=1, padx=8, pady=6, sticky="w")
        return entree

    def afficher_connexion(self):
        self.vider_fenetre()

        wrapper = tk.Frame(self.root, bg="#f2f2f2")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            wrapper,
            text="Simulateur de budget",
            font=("Arial", 24, "bold"),
            bg="#f2f2f2",
        ).pack(pady=(0, 20))

        bloc = tk.Frame(wrapper, bg="white", bd=1, relief="solid")
        bloc.pack(padx=20, pady=10, ipadx=20, ipady=15)

        tk.Label(bloc, text="Connexion", font=("Arial", 15, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )
        self.entry_connexion_nom = self.creer_champ(bloc, "Nom d'utilisateur", 1)
        self.entry_connexion_mdp = self.creer_champ(bloc, "Mot de passe", 2, show="*")

        tk.Button(
            bloc,
            text="Se connecter",
            command=self.se_connecter,
            width=20,
            bg="#2e7d32",
            fg="white",
        ).grid(row=3, column=0, columnspan=2, pady=(8, 18))

        tk.Label(bloc, text="Inscription", font=("Arial", 15, "bold"), bg="white").grid(
            row=4, column=0, columnspan=2, pady=(0, 10)
        )
        self.entry_inscription_nom = self.creer_champ(bloc, "Nom", 5)
        self.entry_inscription_email = self.creer_champ(bloc, "Email", 6)
        self.entry_inscription_mdp = self.creer_champ(bloc, "Mot de passe", 7, show="*")
        self.entry_inscription_confirmer = self.creer_champ(bloc, "Confirmer", 8, show="*")

        tk.Button(
            bloc,
            text="S'inscrire",
            command=self.s_inscrire,
            width=20,
            bg="#1565c0",
            fg="white",
        ).grid(row=9, column=0, columnspan=2, pady=(8, 0))

        tk.Button(
            wrapper,
            text="Quitter",
            command=self.quitter,
            width=20,
            bg="#b71c1c",
            fg="white",
        ).pack(pady=12)

    def se_connecter(self):
        nom = self.entry_connexion_nom.get().strip()
        mot_de_passe = self.entry_connexion_mdp.get()

        if not nom or not mot_de_passe:
            messagebox.showwarning("Attention", "Remplis tous les champs.")
            return

        utilisateur = self.utilisateurs.get(nom)
        if not utilisateur:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
            return

        if utilisateur.get("mot_de_passe") != mot_de_passe:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
            return

        self.utilisateur_actuel = nom
        self.donnees = utilisateur.get("donnees", {"revenus": [], "depenses": []})
        self.donnees.setdefault("revenus", [])
        self.donnees.setdefault("depenses", [])
        self.afficher_simulateur()

    def s_inscrire(self):
        nom = self.entry_inscription_nom.get().strip()
        email = self.entry_inscription_email.get().strip()
        mot_de_passe = self.entry_inscription_mdp.get()
        confirmation = self.entry_inscription_confirmer.get()

        if not nom or not email or not mot_de_passe or not confirmation:
            messagebox.showwarning("Attention", "Remplis tous les champs.")
            return

        if nom in self.utilisateurs:
            messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Erreur", "Email invalide.")
            return

        if len(mot_de_passe) < 4:
            messagebox.showerror("Erreur", "Le mot de passe doit faire au moins 4 caractères.")
            return

        if mot_de_passe != confirmation:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        self.utilisateurs[nom] = {
            "mot_de_passe": mot_de_passe,
            "email": email,
            "donnees": {"revenus": [], "depenses": []},
        }
        self.sauvegarder_utilisateurs()

        for champ in (
            self.entry_inscription_nom,
            self.entry_inscription_email,
            self.entry_inscription_mdp,
            self.entry_inscription_confirmer,
        ):
            champ.delete(0, tk.END)

        messagebox.showinfo("Succès", "Compte créé. Tu peux maintenant te connecter.")

    def afficher_simulateur(self):
        self.vider_fenetre()

        haut = tk.Frame(self.root, bg="#f2f2f2")
        haut.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            haut,
            text=f"Budget de {self.utilisateur_actuel}",
            font=("Arial", 20, "bold"),
            bg="#f2f2f2",
        ).pack(side="left")

        tk.Button(haut, text="Déconnexion", command=self.deconnecter, bg="#ef6c00").pack(side="right", padx=5)

        contenu = tk.Frame(self.root, bg="#f2f2f2")
        contenu.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.creer_bloc_saisie(contenu, "Revenus", "#dcedc8", self.ajouter_revenu)
        self.creer_bloc_saisie(contenu, "Dépenses", "#ffcdd2", self.ajouter_depense)
        self.creer_bloc_resume(contenu)
        self.creer_bloc_graphiques(contenu)
        self.creer_bloc_actions(contenu)

        self.actualiser_affichage()

    def creer_bloc_saisie(self, parent, titre, couleur, commande):
        cadre = tk.LabelFrame(parent, text=titre, bg=couleur, padx=10, pady=10)
        cadre.pack(fill="x", pady=6)

        form = tk.Frame(cadre, bg=couleur)
        form.pack(fill="x")

        tk.Label(form, text="Nom", bg=couleur).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Montant (€)", bg=couleur).grid(row=0, column=2, padx=5, pady=5)

        entree_nom = tk.Entry(form, width=24)
        entree_nom.grid(row=0, column=1, padx=5, pady=5)

        entree_montant = tk.Entry(form, width=14)
        entree_montant.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(form, text="Ajouter", command=commande, width=12).grid(row=0, column=4, padx=10, pady=5)

        liste = tk.Listbox(cadre, height=5)
        liste.pack(fill="x", padx=5, pady=(8, 0))

        if titre == "Revenus":
            self.entry_revenu_nom = entree_nom
            self.entry_revenu_montant = entree_montant
            self.liste_revenus = liste
        else:
            self.entry_depense_nom = entree_nom
            self.entry_depense_montant = entree_montant
            self.liste_depenses = liste

    def creer_bloc_resume(self, parent):
        cadre = tk.LabelFrame(parent, text="Résumé", bg="#fff9c4", padx=10, pady=10)
        cadre.pack(fill="x", pady=6)

        self.label_total_revenus = tk.Label(cadre, text="Total revenus : 0.00 €", bg="#fff9c4", fg="#2e7d32")
        self.label_total_revenus.pack(anchor="w", pady=2)

        self.label_total_depenses = tk.Label(cadre, text="Total dépenses : 0.00 €", bg="#fff9c4", fg="#c62828")
        self.label_total_depenses.pack(anchor="w", pady=2)

        self.label_solde = tk.Label(cadre, text="Solde : 0.00 €", bg="#fff9c4", font=("Arial", 13, "bold"))
        self.label_solde.pack(anchor="w", pady=(4, 0))

    def creer_bloc_graphiques(self, parent):
        cadre = tk.LabelFrame(parent, text="Graphiques", bg="#eeeeee", padx=10, pady=10)
        cadre.pack(fill="both", expand=True, pady=6)

        boutons = tk.Frame(cadre, bg="#eeeeee")
        boutons.pack(anchor="w", pady=(0, 8))

        tk.Button(boutons, text="Dépenses par poste", command=self.afficher_camembert).pack(side="left", padx=(0, 8))
        tk.Button(boutons, text="Revenus / dépenses", command=self.afficher_barres).pack(side="left")

        self.frame_graphique = tk.Frame(cadre, bg="white", height=260)
        self.frame_graphique.pack(fill="both", expand=True)
        self.frame_graphique.pack_propagate(False)

    def creer_bloc_actions(self, parent):
        cadre = tk.Frame(parent, bg="#f2f2f2")
        cadre.pack(fill="x", pady=8)

        tk.Button(cadre, text="Supprimer le dernier", command=self.supprimer_dernier, bg="#ffb74d").pack(side="left")
        tk.Button(cadre, text="Tout effacer", command=self.tout_effacer, bg="#c62828", fg="white").pack(
            side="left", padx=8
        )

    def sauvegarder_donnees_utilisateur(self):
        self.utilisateurs[self.utilisateur_actuel]["donnees"] = self.donnees
        self.sauvegarder_utilisateurs()

    def lire_montant(self, entree_nom, entree_montant):
        nom = entree_nom.get().strip()
        montant_texte = entree_montant.get().strip().replace(",", ".")

        if not nom or not montant_texte:
            messagebox.showwarning("Attention", "Remplis le nom et le montant.")
            return None, None

        try:
            montant = float(montant_texte)
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre.")
            return None, None

        if montant <= 0:
            messagebox.showwarning("Attention", "Le montant doit être positif.")
            return None, None

        return nom, montant

    def ajouter_revenu(self):
        nom, montant = self.lire_montant(self.entry_revenu_nom, self.entry_revenu_montant)
        if nom is None:
            return

        self.donnees["revenus"].append({"nom": nom, "montant": montant})
        self.entry_revenu_nom.delete(0, tk.END)
        self.entry_revenu_montant.delete(0, tk.END)
        self.sauvegarder_donnees_utilisateur()
        self.actualiser_affichage()

    def ajouter_depense(self):
        nom, montant = self.lire_montant(self.entry_depense_nom, self.entry_depense_montant)
        if nom is None:
            return

        self.donnees["depenses"].append({"nom": nom, "montant": montant})
        self.entry_depense_nom.delete(0, tk.END)
        self.entry_depense_montant.delete(0, tk.END)
        self.sauvegarder_donnees_utilisateur()
        self.actualiser_affichage()

    def nettoyer_graphique(self):
        for widget in self.frame_graphique.winfo_children():
            widget.destroy()

        if self.canvas_graphique is not None:
            plt.close(self.canvas_graphique.figure)
            self.canvas_graphique = None

    def afficher_camembert(self):
        if not self.donnees["depenses"]:
            messagebox.showinfo("Info", "Ajoute d'abord au moins une dépense.")
            return

        self.nettoyer_graphique()

        totaux = {}
        for depense in self.donnees["depenses"]:
            nom = depense["nom"]
            totaux[nom] = totaux.get(nom, 0) + depense["montant"]

        figure, axe = plt.subplots(figsize=(6, 4))
        axe.pie(list(totaux.values()), labels=list(totaux.keys()), autopct="%1.1f%%", startangle=90)
        axe.set_title("Répartition des dépenses")

        self.canvas_graphique = FigureCanvasTkAgg(figure, self.frame_graphique)
        self.canvas_graphique.draw()
        self.canvas_graphique.get_tk_widget().pack(fill="both", expand=True)

    def afficher_barres(self):
        self.nettoyer_graphique()

        total_revenus = sum(item["montant"] for item in self.donnees["revenus"])
        total_depenses = sum(item["montant"] for item in self.donnees["depenses"])

        figure, axe = plt.subplots(figsize=(6, 4))
        barres = axe.bar(["Revenus", "Dépenses"], [total_revenus, total_depenses], color=["#4caf50", "#e53935"])
        axe.set_ylabel("Montant (€)")
        axe.set_title("Comparaison simple")
        axe.grid(axis="y", alpha=0.25)

        for barre, montant in zip(barres, [total_revenus, total_depenses]):
            axe.text(
                barre.get_x() + barre.get_width() / 2,
                barre.get_height(),
                f"{montant:.2f} €",
                ha="center",
                va="bottom",
            )

        self.canvas_graphique = FigureCanvasTkAgg(figure, self.frame_graphique)
        self.canvas_graphique.draw()
        self.canvas_graphique.get_tk_widget().pack(fill="both", expand=True)

    def supprimer_dernier(self):
        if not self.donnees["revenus"] and not self.donnees["depenses"]:
            messagebox.showinfo("Info", "Il n'y a rien à supprimer.")
            return

        if not messagebox.askyesno("Confirmation", "Supprimer le dernier élément ajouté ?"):
            return

        if self.donnees["depenses"]:
            self.donnees["depenses"].pop()
        else:
            self.donnees["revenus"].pop()

        self.sauvegarder_donnees_utilisateur()
        self.actualiser_affichage()

    def tout_effacer(self):
        if not messagebox.askyesno("Confirmation", "Tout effacer pour cet utilisateur ?"):
            return

        self.donnees = {"revenus": [], "depenses": []}
        self.sauvegarder_donnees_utilisateur()
        self.actualiser_affichage()
        self.nettoyer_graphique()

    def actualiser_affichage(self):
        self.liste_revenus.delete(0, tk.END)
        self.liste_depenses.delete(0, tk.END)

        total_revenus = 0
        for revenu in self.donnees["revenus"]:
            total_revenus += revenu["montant"]
            self.liste_revenus.insert(tk.END, f'{revenu["nom"]} : {revenu["montant"]:.2f} €')

        total_depenses = 0
        for depense in self.donnees["depenses"]:
            total_depenses += depense["montant"]
            self.liste_depenses.insert(tk.END, f'{depense["nom"]} : {depense["montant"]:.2f} €')

        solde = total_revenus - total_depenses

        self.label_total_revenus.config(text=f"Total revenus : {total_revenus:.2f} €")
        self.label_total_depenses.config(text=f"Total dépenses : {total_depenses:.2f} €")
        self.label_solde.config(
            text=f"Solde : {solde:.2f} €",
            fg="#2e7d32" if solde >= 0 else "#c62828",
        )

    def deconnecter(self):
        if messagebox.askyesno("Déconnexion", "Se déconnecter ?"):
            self.utilisateur_actuel = None
            self.donnees = {"revenus": [], "depenses": []}
            self.afficher_connexion()

    def quitter(self):
        if messagebox.askyesno("Quitter", "Fermer l'application ?"):
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulateurBudget(root)
    root.mainloop()
