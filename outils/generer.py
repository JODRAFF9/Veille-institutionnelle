#!/usr/bin/env python3
"""Génère, à partir de donnees_veille.py :
- ressources.xlsx dans chaque dossier thématique (liens, rythme de publication, fréquence de veille, statut HTTP)
- presentation.tex (Beamer) dans chaque dossier thématique
- presentation-globale.tex dans chaque dossier d'institution
- veille/calendrier-veille.xlsx (calendrier des publications et journal de veille)

Usage : python3 outils/generer.py [--sans-verif] [--pdf]
"""
import concurrent.futures
import datetime
import json
import os
import shutil
import subprocess
import sys
import urllib.request

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from donnees_veille import CALENDRIER, INSTITUTIONS, OPPORTUNITES, SOUS_DOSSIERS

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RACINE, "outils", "statuts.json")
BLEU = "0000FF"
FREQUENCE_VEILLE = "Hebdomadaire"
AUJOURDHUI = datetime.date.today().isoformat()


# ---------- vérification des liens ----------
def tester(url):
    req = urllib.request.Request(url, headers={"User-Agent": "veille-institutionnelle/1.0 (verification de liens)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def verifier(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        return dict(zip(urls, ex.map(tester, urls)))


def toutes_urls():
    urls = {r[1] for inst in INSTITUTIONS.values() for t in inst["themes"] for r in t[3]}
    for parent in SOUS_DOSSIERS.values():
        for subs in parent.values():
            urls |= {r[1] for sd in subs for r in sd[3]}
    for dossiers in OPPORTUNITES.values():
        urls |= {r[1] for d in dossiers for r in d[3]}
    return sorted(urls)


def libelle(code):
    if code == 0:
        return "Injoignable"
    if 200 <= code < 400:
        return f"OK ({code})"
    if code in (401, 403, 429):
        return f"Bloqué aux robots ({code}), à vérifier à la main"
    return f"Erreur ({code})"


# ---------- Excel ----------
def style_entete(ws, largeurs):
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=BLEU)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for i, l in enumerate(largeurs, 1):
        ws.column_dimensions[get_column_letter(i)].width = l
    ws.freeze_panes = "A2"


def ecrire_ressources(chemin, institution, theme, ressources, statuts):
    wb = Workbook()
    ws = wb.active
    ws.title = "Ressources"
    ws.append(["Institution", "Thème", "Ressource", "Lien", "Type", "Rythme de publication",
               "Fréquence de veille", "Statut du lien", "Vérifié le", "Dernière consultation", "Notes"])
    for titre, url, typ, rythme in ressources:
        ws.append([institution, theme, titre, url, typ, rythme, FREQUENCE_VEILLE,
                   libelle(statuts.get(url, 0)), AUJOURDHUI, "", ""])
        cell = ws.cell(row=ws.max_row, column=4)
        cell.hyperlink = url
        cell.font = Font(color=BLEU, underline="single")
    style_entete(ws, [18, 26, 36, 70, 24, 22, 18, 34, 14, 20, 40])
    wb.save(chemin)


def ecrire_calendrier(chemin):
    wb = Workbook()
    ws = wb.active
    ws.title = "Calendrier"
    ws.append(["Institution", "Événement", "Période habituelle", "Remarque"])
    for ligne in CALENDRIER:
        ws.append(list(ligne))
    style_entete(ws, [20, 55, 26, 45])
    j = wb.create_sheet("Journal de veille")
    j.append(["Date", "Institution", "Thème", "Constat", "Source (lien)", "Impact", "Suivi"])
    style_entete(j, [14, 20, 28, 60, 50, 30, 30])
    wb.save(chemin)


# ---------- Beamer ----------
def tex(s):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("≤", r"$\leq$")]:
        s = s.replace(a, b)
    return s


def url_tex(u):
    return u.replace("%", r"\%").replace("#", r"\#")


PREAMBULE = r"""\documentclass[aspectratio=169,11pt]{beamer}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{hyperref}
\definecolor{bleu}{HTML}{0000FF}
\definecolor{fond}{HTML}{F4F4EF}
\setbeamercolor{background canvas}{bg=fond}
\setbeamercolor{structure}{fg=bleu}
\setbeamercolor{title}{fg=bleu}
\setbeamercolor{frametitle}{fg=bleu,bg=fond}
\setbeamercolor{normal text}{fg=black}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{itemize item}{\textcolor{bleu}{\tiny$\blacksquare$}}
\setbeamertemplate{footline}{\hfill\footnotesize\insertframenumber\hspace{1em}\vskip6pt}
\hypersetup{colorlinks=true,urlcolor=bleu,linkcolor=bleu}
"""


def frames(theme, points, ressources):
    out = []
    morceaux = [points[i:i + 4] for i in range(0, len(points), 4)]
    for n, m in enumerate(morceaux, 1):
        suffixe = f" ({n}/{len(morceaux)})" if len(morceaux) > 1 else ""
        out.append("\\begin{frame}{%s%s}\n\\begin{itemize}\n%s\n\\end{itemize}\n\\end{frame}\n" % (
            tex(theme), suffixe, "\n".join("\\item " + tex(p) for p in m)))
    items = "\n".join(
        "\\item \\href{%s}{%s}\\\\{\\footnotesize %s, publication : %s}" % (
            url_tex(u), tex(t), tex(ty), tex(r.lower())) for t, u, ty, r in ressources)
    out.append("\\begin{frame}{%s : ressources à suivre}\n\\small\nVeille %s.\n\\begin{itemize}\n%s\n\\end{itemize}\n\\end{frame}\n" % (
        tex(theme), FREQUENCE_VEILLE.lower(), items))
    return "\n".join(out)


def readme(titre, points, ressources, statuts):
    lignes = ["# " + titre, ""] + ["- " + p for p in points] + ["", "| Ressource | Type | Publication | Veille | Statut |", "|---|---|---|---|---|"]
    for t, u, ty, r in ressources:
        lignes.append(f"| [{t}]({u}) | {ty} | {r} | {FREQUENCE_VEILLE} | {libelle(statuts.get(u, 0))} |")
    lignes += ["", "Fichiers : `ressources.xlsx` (liens à suivre), `presentation.tex` (Beamer).", ""]
    return "\n".join(lignes)


def document(titre, soustitre, corps):
    return (PREAMBULE + "\\title{%s}\n\\subtitle{%s}\n\\author{Veille institutionnelle}\n\\date{%s}\n\n"
            "\\begin{document}\n\\begin{frame}\\titlepage\\end{frame}\n\n%s\n\\end{document}\n") % (
        tex(titre), tex(soustitre), AUJOURDHUI, corps)


def ecrire(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)


def compiler(dossier, fichier):
    if not shutil.which("pdflatex"):
        return False
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", fichier],
                       cwd=dossier, capture_output=True, text=True)
    for ext in ("aux", "log", "nav", "out", "snm", "toc", "vrb"):
        p = os.path.join(dossier, fichier.rsplit(".", 1)[0] + "." + ext)
        if os.path.exists(p):
            os.remove(p)
    if r.returncode != 0:
        print("Échec de compilation :", dossier, fichier)
    return r.returncode == 0


def ecrire_opportunites(statuts, pdf):
    base = os.path.join(RACINE, "opportunites")
    os.makedirs(base, exist_ok=True)
    index = ["# Opportunités", "",
             "Emplois, stages, marchés, bourses et événements de chaque institution. Veille " + FREQUENCE_VEILLE.lower() + ".", "",
             "| Institution | Dossier |", "|---|---|"]
    for cle, dossiers in OPPORTUNITES.items():
        nom = INSTITUTIONS[cle]["nom"]
        index.append(f"| {nom} | [{cle}/]({cle}/README.md) |")
        sous = ["# " + nom + " : opportunités", "", "| Thème | Dossier |", "|---|---|"]
        for d, titre, points, ressources in dossiers:
            chemin = os.path.join(base, cle, d)
            os.makedirs(chemin, exist_ok=True)
            ecrire_ressources(os.path.join(chemin, "ressources.xlsx"), nom, titre, ressources, statuts)
            ecrire(os.path.join(chemin, "README.md"), readme(titre, points, ressources, statuts))
            ecrire(os.path.join(chemin, "presentation.tex"), document(titre + " : " + nom, "Opportunités", frames(titre, points, ressources)))
            sous.append(f"| {titre} | [{d}]({d}/README.md) |")
            if pdf:
                compiler(chemin, "presentation.tex")
        ecrire(os.path.join(base, cle, "README.md"), "\n".join(sous) + "\n")
    ecrire(os.path.join(base, "README.md"), "\n".join(index) + "\n\nSuivi des candidatures : [suivi-des-opportunites.xlsx](suivi-des-opportunites.xlsx).\n")
    wb = Workbook()
    ws = wb.active
    ws.title = "Suivi"
    ws.append(["Institution", "Opportunité", "Type", "Lien", "Date limite", "Statut", "Prochaine action", "Notes"])
    style_entete(ws, [26, 40, 24, 50, 14, 16, 30, 40])
    wb.save(os.path.join(base, "suivi-des-opportunites.xlsx"))


def main():
    if "--sans-verif" in sys.argv and os.path.exists(CACHE):
        statuts = json.load(open(CACHE))
    else:
        statuts = verifier(toutes_urls())
        json.dump(statuts, open(CACHE, "w"), indent=1, sort_keys=True)
    pdf = "--pdf" in sys.argv
    for dossier_inst, inst in INSTITUTIONS.items():
        globaux = []
        for dossier, theme, points, ressources in inst["themes"]:
            chemin = os.path.join(RACINE, dossier_inst, dossier)
            os.makedirs(chemin, exist_ok=True)
            ecrire_ressources(os.path.join(chemin, "ressources.xlsx"), inst["nom"], theme, ressources, statuts)
            if not os.path.exists(os.path.join(chemin, "README.md")):
                ecrire(os.path.join(chemin, "README.md"), readme(theme, points, ressources, statuts))
            corps = frames(theme, points, ressources)
            ecrire(os.path.join(chemin, "presentation.tex"), document(theme, inst["nom"], corps))
            globaux.append("\\section{%s}\n%s" % (tex(theme), corps))
            for sd, st, sp, sr in SOUS_DOSSIERS.get(dossier_inst, {}).get(dossier, []):
                cs = os.path.join(chemin, sd)
                os.makedirs(cs, exist_ok=True)
                ecrire_ressources(os.path.join(cs, "ressources.xlsx"), inst["nom"], st, sr, statuts)
                sc = frames(st, sp, sr)
                ecrire(os.path.join(cs, "presentation.tex"), document(st, inst["nom"], sc))
                ecrire(os.path.join(cs, "README.md"), readme(st, sp, sr, statuts))
                globaux.append("\\subsection{%s}\n%s" % (tex(st), sc))
                if pdf:
                    compiler(cs, "presentation.tex")
            if pdf:
                compiler(chemin, "presentation.tex")
        base = os.path.join(RACINE, dossier_inst)
        if not os.path.exists(os.path.join(base, "README.md")):
            lignes = ["# " + inst["nom"], "", "| Thème | Dossier |", "|---|---|"]
            lignes += [f"| {t[1]} | [{t[0]}]({t[0]}/README.md) |" for t in inst["themes"]]
            lignes += ["", "Chaque dossier contient `ressources.xlsx` et `presentation.tex/pdf`. Vue d'ensemble : [presentation-globale.pdf](presentation-globale.pdf).", ""]
            ecrire(os.path.join(base, "README.md"), "\n".join(lignes))
        ecrire(os.path.join(base, "presentation-globale.tex"),
               document(inst["nom"], "Fonctionnement et données, vue d'ensemble", "\n".join(globaux)))
        if pdf:
            compiler(base, "presentation-globale.tex")
    ecrire_opportunites(statuts, pdf)
    os.makedirs(os.path.join(RACINE, "veille"), exist_ok=True)
    ecrire_calendrier(os.path.join(RACINE, "veille", "calendrier-veille.xlsx"))
    mauvais = [(u, c) for u, c in statuts.items() if not (200 <= c < 400)]
    print(f"{len(statuts)} liens testés, {len(mauvais)} à examiner")
    for u, c in mauvais:
        print("  ", c, u)


if __name__ == "__main__":
    main()
