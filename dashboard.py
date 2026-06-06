import urllib.request
import urllib.parse
import json
import os
import webbrowser
import time
from datetime import datetime
from html import escape

APP_ID   = "614d71cf"
APP_KEY  = "fab4d71d52b3eb8503920738f23257a7"
PAYS     = "fr"
BASE_URL = f"https://api.adzuna.com/v1/api/jobs/{PAYS}/search"

# ─────────────────────────────────────────────
# DOMAINES ET MOTS-CLÉS
# ─────────────────────────────────────────────
DOMAINES = {
    "1": {
        "categorie": "Sciences Appliquees & Technologies",
        "label": "Data & Intelligence Artificielle",
        "queries": ["alternance data analyst","alternance data scientist","alternance data engineer","alternance machine learning","alternance intelligence artificielle","apprentissage data analyst","alternance big data","alternance IA"]
    },
    "2": {
        "categorie": "Sciences Appliquees & Technologies",
        "label": "Genie Informatique & Developpement",
        "queries": ["alternance developpeur logiciel","alternance developpeur Python","alternance developpeur Java","alternance developpeur web","alternance ingenieur logiciel","alternance DevOps","apprentissage developpeur"]
    },
    "3": {
        "categorie": "Sciences Appliquees & Technologies",
        "label": "Cybersecurite",
        "queries": ["alternance cybersecurite","alternance securite informatique","alternance pentesting","alternance analyste securite","apprentissage cybersecurite","alternance SOC analyste"]
    },
    "4": {
        "categorie": "Sciences Appliquees & Technologies",
        "label": "Cloud & Reseaux Telecoms",
        "queries": ["alternance cloud engineer","alternance architecte cloud","alternance AWS Azure","alternance ingenieur reseau","alternance telecoms","alternance administrateur reseau","apprentissage cloud"]
    },
    "5": {
        "categorie": "Industrie & Production",
        "label": "Genie Mecanique",
        "queries": ["alternance ingenieur mecanique","alternance conception mecanique","alternance bureau etudes mecanique","alternance CAO mecanique","apprentissage mecanique","alternance ingenieur mecatronique","alternance moteur vehicule"]
    },
    "6": {
        "categorie": "Industrie & Production",
        "label": "Genie Electrique & Electronique",
        "queries": ["alternance ingenieur electrique","alternance electronique embarquee","alternance automatisme","alternance robotique","alternance microelectronique","apprentissage electronique","alternance ingenieur electrotechnique"]
    },
    "7": {
        "categorie": "Industrie & Production",
        "label": "Genie Industriel & Productique",
        "queries": ["alternance ingenieur industriel","alternance genie industriel","alternance supply chain","alternance lean manufacturing","alternance qualite production","apprentissage genie industriel","alternance methodes production"]
    },
    "8": {
        "categorie": "Industrie & Production",
        "label": "Genie Aerospatial",
        "queries": ["alternance ingenieur aeronautique","alternance aerospatial","alternance Airbus","alternance Safran","alternance Thales aeronautique","apprentissage aeronautique","alternance ingenieur spatial"]
    },
    "9": {
        "categorie": "Industrie & Production",
        "label": "Genie Chimique & Materiaux",
        "queries": ["alternance ingenieur chimiste","alternance genie chimique","alternance materiaux","alternance polymeres","alternance procedes industriels","apprentissage chimie industrielle","alternance ingenieur materiaux"]
    },
    "10": {
        "categorie": "Batiment, TP & Environnement",
        "label": "Genie Civil & BTP",
        "queries": ["alternance ingenieur genie civil","alternance BTP","alternance conducteur travaux","alternance structure beton","alternance infrastructure","apprentissage genie civil","alternance ingenieur TP"]
    },
    "11": {
        "categorie": "Batiment, TP & Environnement",
        "label": "Genie de l'Environnement & Energies",
        "queries": ["alternance ingenieur environnement","alternance energie renouvelable","alternance traitement eau","alternance gestion dechets","alternance developpement durable","apprentissage environnement","alternance ingenieur energie"]
    },
    "12": {
        "categorie": "Sciences du Vivant & Ressources",
        "label": "Genie Biomedical",
        "queries": ["alternance ingenieur biomedical","alternance dispositif medical","alternance imagerie medicale","alternance biomedical","apprentissage biomedical","alternance ingenieur sante","alternance medtech"]
    },
    "13": {
        "categorie": "Sciences du Vivant & Ressources",
        "label": "Genie Agroalimentaire",
        "queries": ["alternance ingenieur agroalimentaire","alternance qualite alimentaire","alternance industrie alimentaire","alternance agro","apprentissage agroalimentaire","alternance ingenieur agri","alternance R&D agroalimentaire"]
    },
    "14": {
        "categorie": "Domaines Supplementaires",
        "label": "Genie Nucleaire & Energie",
        "queries": ["alternance ingenieur nucleaire","alternance energie nucleaire","alternance EDF","alternance CEA","apprentissage nucleaire","alternance ingenieur energie nucleaire"]
    },
    "15": {
        "categorie": "Domaines Supplementaires",
        "label": "Genie Naval & Maritime",
        "queries": ["alternance ingenieur naval","alternance genie maritime","alternance construction navale","apprentissage naval","alternance Naval Group","alternance ingenieur offshore"]
    },
    "16": {
        "categorie": "Toutes les offres",
        "label": "Toutes les offres d'ingenierie",
        "queries": ["alternance ingenieur","alternance data","alternance informatique","alternance mecanique","alternance electronique","alternance civil","alternance environnement","alternance aeronautique","alternance chimie","alternance biomedical"]
    },
}

CONTRATS = {
    "A": "Alternance",
    "B": "CDI",
    "C": "CDD",
    "D": "Stage",
    "E": "Freelance",
    "F": "Toutes",
}

# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
def afficher_menu():
    print("=" * 62)
    print("   DASHBOARD EMPLOI — INGENIERIE & INDUSTRIE EN FRANCE")
    print("=" * 62)

    categories = {}
    for k, v in DOMAINES.items():
        cat = v["categorie"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((k, v["label"]))

    print()
    for cat, items in categories.items():
        print(f"  [{cat}]")
        for k, label in items:
            print(f"    {k:>2}. {label}")
        print()

    while True:
        choix_domaine = input("  Choisis ton domaine (1-16) : ").strip()
        if choix_domaine in DOMAINES:
            break
        print("  Choix invalide, entre un chiffre entre 1 et 16.")

    print()
    print("  Type de contrat :")
    print("  A. Alternance   B. CDI   C. CDD   D. Stage   E. Freelance   F. Toutes")
    print()
    while True:
        choix_contrat = input("  Ton choix (A-F) : ").strip().upper()
        if choix_contrat in CONTRATS:
            break
        print("  Choix invalide.")

    return choix_domaine, choix_contrat

# ─────────────────────────────────────────────
# API
# ─────────────────────────────────────────────
def appeler_adzuna(query, page=1, nb_resultats=50):
    params = urllib.parse.urlencode({
        "app_id":           APP_ID,
        "app_key":          APP_KEY,
        "results_per_page": nb_resultats,
        "what":             query,
        "where":            "france",
        "content-type":     "application/json",
    })
    url = f"{BASE_URL}/{page}?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  Erreur API '{query}' : {e}")
        return None

def detecter_contrat(titre, description):
    t = (titre + " " + description).lower()
    if "alternance" in t or "apprentissage" in t: return "Alternance"
    if "stage" in t: return "Stage"
    if "freelance" in t or "independant" in t: return "Freelance"
    if "cdd" in t: return "CDD"
    return "CDI"

def extraire_ville(location):
    if not location: return "Non precisee"
    nom = location.get("display_name", "")
    if not nom:
        areas = location.get("area", [])
        nom = areas[-1] if areas else "Non precisee"
    return nom.split(",")[0].strip()

def adapter_queries(queries, type_contrat):
    if type_contrat == "Toutes":
        return queries
    label = type_contrat.lower()
    adapted = []
    for q in queries:
        q_clean = q.replace("alternance","").replace("apprentissage","").replace("stage","").replace("CDI","").replace("CDD","").replace("freelance","").strip()
        adapted.append(f"{label} {q_clean}")
    return adapted

def scraper_adzuna(queries):
    print()
    print("  Connexion a l'API Adzuna...")
    print()
    toutes = []
    for query in queries:
        print(f"  Recherche : '{query}'")
        total_query = 0
        for page in range(1, 4):
            data = appeler_adzuna(query, page=page, nb_resultats=50)
            if not data or "results" not in data or not data["results"]:
                break
            for job in data["results"]:
                titre       = job.get("title", "Inconnu")
                entreprise  = job.get("company", {}).get("display_name", "Inconnue")
                description = job.get("description", "")
                ville       = extraire_ville(job.get("location", {}))
                salaire_min = job.get("salary_min")
                salaire_max = job.get("salary_max")
                contrat     = detecter_contrat(titre, description)
                entreprise_search = urllib.parse.quote(f"{entreprise} recrutement candidature {titre}")
                lien = f"https://www.google.com/search?q={entreprise_search}"

                if salaire_min and salaire_max:
                    salaire = f"{int(salaire_min):,} - {int(salaire_max):,} EUR"
                elif salaire_min:
                    salaire = f"A partir de {int(salaire_min):,} EUR"
                else:
                    salaire = "Non communique"

                toutes.append({
                    "titre":      titre,
                    "entreprise": entreprise,
                    "ville":      ville,
                    "contrat":    contrat,
                    "salaire":    salaire,
                    "source":     query,
                    "lien":       lien,
                })
                total_query += 1
            time.sleep(0.4)
        print(f"     -> {total_query} offres")

    vus = set()
    uniques = []
    for r in toutes:
        cle = (r["titre"].lower(), r["entreprise"].lower(), r["ville"].lower())
        if cle not in vus:
            vus.add(cle)
            uniques.append(r)

    print()
    print(f"  Total : {len(uniques)} offres uniques")
    return uniques

# ─────────────────────────────────────────────
# CALCULS
# ─────────────────────────────────────────────
def compter(data, champ):
    counts = {}
    for row in data:
        v = row[champ]
        counts[v] = counts.get(v, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))

# ─────────────────────────────────────────────
# HTML
# ─────────────────────────────────────────────
def generer_html(data, label_domaine, label_contrat):
    ordre = {"Alternance": 0, "Stage": 1, "CDD": 2, "CDI": 3, "Freelance": 4}
    data_trie = sorted(data, key=lambda x: ordre.get(x["contrat"], 9))

    contrats  = compter(data, "contrat")
    villes    = dict(list(compter(data, "ville").items())[:10])
    titres    = dict(list(compter(data, "titre").items())[:12])
    sources   = dict(list(compter(data, "source").items())[:8])

    nb_total  = len(data)
    nb_cible  = sum(1 for r in data if r["contrat"] == label_contrat)
    nb_villes = len(set(r["ville"] for r in data))
    ville_top = list(compter(data, "ville").keys())[0] if data else "N/A"

    rows_html = ""
    for r in data_trie:
        badge = r["contrat"].lower().replace(" ", "")
        rows_html += f"""
        <tr>
          <td>{escape(r['titre'])}</td>
          <td>{escape(r['entreprise'])}</td>
          <td>{escape(r['ville'])}</td>
          <td><span class="badge badge-{badge}">{escape(r['contrat'])}</span></td>
          <td>{escape(r['salaire'])}</td>
          <td><a href="{escape(r['lien'])}" target="_blank" class="btn-postuler">Postuler &#8594;</a></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Emploi Ingenierie — France</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI',sans-serif; background:#0f1117; color:#e0e0e0; }}
  header {{ background:linear-gradient(135deg,#1a1f2e,#16213e); padding:32px 40px; border-bottom:1px solid #2a2f45; }}
  header h1 {{ font-size:24px; color:#00d4ff; }}
  header p {{ color:#7a8299; margin-top:6px; font-size:13px; }}
  .tags {{ margin-top:10px; display:flex; gap:8px; flex-wrap:wrap; }}
  .tag {{ display:inline-block; border-radius:20px; padding:4px 14px; font-size:12px; font-weight:600; }}
  .tag-domaine {{ background:#1a2a1a; color:#00d084; }}
  .tag-contrat {{ background:#0d1f3b; color:#00aaff; }}
  .container {{ max-width:1200px; margin:0 auto; padding:32px 24px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }}
  .kpi {{ background:#1a1f2e; border:1px solid #2a2f45; border-radius:8px; padding:20px; text-align:center; }}
  .kpi-val {{ font-size:32px; font-weight:700; color:#00d4ff; }}
  .kpi-label {{ font-size:12px; color:#7a8299; margin-top:4px; }}
  .charts {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:32px; }}
  .chart-box {{ background:#1a1f2e; border:1px solid #2a2f45; border-radius:8px; padding:20px; }}
  .chart-box h3 {{ font-size:14px; color:#a0a8c0; margin-bottom:16px; }}
  h2 {{ font-size:16px; color:#a0a8c0; margin-bottom:16px; }}
  .toolbar {{ display:flex; align-items:center; gap:12px; margin-bottom:16px; flex-wrap:wrap; }}
  .toolbar input {{ background:#1a1f2e; border:1px solid #2a2f45; border-radius:6px; padding:10px 16px; color:#e0e0e0; font-size:13px; width:300px; outline:none; }}
  .toolbar input:focus {{ border-color:#00d4ff; }}
  .btn-export {{ background:#00d4ff; color:#0f1117; border:none; padding:10px 20px; border-radius:6px; font-size:13px; font-weight:700; cursor:pointer; }}
  table {{ width:100%; border-collapse:collapse; background:#1a1f2e; border-radius:8px; overflow:hidden; }}
  th {{ background:#16213e; color:#7a8299; font-size:11px; text-transform:uppercase; padding:12px 16px; text-align:left; letter-spacing:.05em; }}
  td {{ padding:11px 16px; font-size:13px; border-bottom:1px solid #2a2f45; }}
  tr:hover td {{ background:#1f2640; }}
  .badge {{ padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600; }}
  .badge-cdi {{ background:#0d3b2e; color:#00d084; }}
  .badge-cdd {{ background:#2e2a0d; color:#d0b000; }}
  .badge-alternance {{ background:#0d1f3b; color:#00aaff; }}
  .badge-stage {{ background:#2e0d2e; color:#cc44cc; }}
  .badge-freelance {{ background:#2e1a0d; color:#ff8c00; }}
  .btn-postuler {{ display:inline-block; background:#00d084; color:#0f1117; padding:5px 14px; border-radius:6px; font-size:12px; font-weight:700; text-decoration:none; }}
  .btn-postuler:hover {{ background:#00ff9d; }}
</style>
</head>
<body>
<header>
  <h1>&#128202; Dashboard Emploi — Ingenierie &amp; Industrie en France</h1>
  <p>Source : Adzuna API &middot; {nb_total} offres &middot; {datetime.now().strftime('%d/%m/%Y')}</p>
  <div class="tags">
    <span class="tag tag-domaine">&#128188; {label_domaine}</span>
    <span class="tag tag-contrat">&#128203; {label_contrat}</span>
  </div>
</header>
<div class="container">
  <div class="kpis">
    <div class="kpi"><div class="kpi-val">{nb_total}</div><div class="kpi-label">Total offres</div></div>
    <div class="kpi"><div class="kpi-val">{nb_cible}</div><div class="kpi-label">{label_contrat}s</div></div>
    <div class="kpi"><div class="kpi-val">{nb_villes}</div><div class="kpi-label">Villes</div></div>
    <div class="kpi"><div class="kpi-val">{ville_top}</div><div class="kpi-label">Ville #1</div></div>
  </div>
  <div class="charts">
    <div class="chart-box"><h3>Par type de contrat</h3><canvas id="c1" height="220"></canvas></div>
    <div class="chart-box"><h3>Top 10 villes</h3><canvas id="c2" height="220"></canvas></div>
    <div class="chart-box"><h3>Top intitules de poste</h3><canvas id="c3" height="220"></canvas></div>
    <div class="chart-box"><h3>Offres par mot-cle</h3><canvas id="c4" height="220"></canvas></div>
  </div>
  <h2>Toutes les offres — {label_contrat} en priorite</h2>
  <div class="toolbar">
    <input type="text" id="searchInput" placeholder="Filtrer par poste, ville, entreprise..." onkeyup="filtrer()">
    <button class="btn-export" onclick="exportCSV()">&#11015; Exporter CSV</button>
  </div>
  <table>
    <thead><tr><th>Poste</th><th>Entreprise</th><th>Ville</th><th>Contrat</th><th>Salaire</th><th>Postuler</th></tr></thead>
    <tbody id="tbody">{rows_html}</tbody>
  </table>
</div>
<script>
const C=['#00d4ff','#ff4d6d','#b8ff57','#ffa500','#aa44ff','#00d084','#ff6b6b','#4ecdc4'];
new Chart(document.getElementById('c1'),{{type:'doughnut',data:{{labels:{list(contrats.keys())},datasets:[{{data:{list(contrats.values())},backgroundColor:C,borderWidth:0}}]}},options:{{plugins:{{legend:{{labels:{{color:'#a0a8c0'}}}}}},cutout:'55%'}}}});
new Chart(document.getElementById('c2'),{{type:'bar',data:{{labels:{list(villes.keys())},datasets:[{{data:{list(villes.values())},backgroundColor:'#00d4ff88',borderRadius:4}}]}},options:{{indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:'#7a8299'}}}},y:{{ticks:{{color:'#a0a8c0'}}}}}}}}}});
new Chart(document.getElementById('c3'),{{type:'bar',data:{{labels:{list(titres.keys())},datasets:[{{data:{list(titres.values())},backgroundColor:'#b8ff5788',borderRadius:4}}]}},options:{{indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:'#7a8299'}}}},y:{{ticks:{{color:'#a0a8c0'}}}}}}}}}});
new Chart(document.getElementById('c4'),{{type:'bar',data:{{labels:{list(sources.keys())},datasets:[{{data:{list(sources.values())},backgroundColor:C,borderRadius:4}}]}},options:{{plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:'#7a8299'}}}},y:{{ticks:{{color:'#a0a8c0'}}}}}}}}}});
function filtrer(){{const val=document.getElementById('searchInput').value.toLowerCase();for(let r of document.getElementById('tbody').rows)r.style.display=r.innerText.toLowerCase().includes(val)?'':'none';}}
function exportCSV(){{
  const rows=document.getElementById('tbody').rows;
  let csv='Poste;Entreprise;Ville;Contrat;Salaire;Lien\\n';
  for(let r of rows){{
    if(r.style.display==='none') continue;
    const cols=r.querySelectorAll('td');
    const lienTag=cols[5].querySelector('a');
    const lien=lienTag?lienTag.href:'';
    const ligne=[cols[0].innerText,cols[1].innerText,cols[2].innerText,cols[3].innerText,cols[4].innerText,lien].map(v=>'"'+v.replace(/"/g,'""')+'"').join(';');
    csv+=ligne+'\\n';
  }}
  const bom='\uFEFF';
  const blob=new Blob([bom+csv],{{type:'text/csv;charset=utf-8;'}});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='offres_ingenierie.csv';
  a.click();
}}
</script>
</body>
</html>"""
    return html

# ─────────────────────────────────────────────
# POINT D'ENTREE
# ─────────────────────────────────────────────
choix_domaine, choix_contrat = afficher_menu()

config        = DOMAINES[choix_domaine]
label_domaine = config["label"]
label_contrat = CONTRATS[choix_contrat]
queries       = adapter_queries(config["queries"], label_contrat)

print()
print(f"  Domaine  : {label_domaine}")
print(f"  Contrat  : {label_contrat}")

data = scraper_adzuna(queries)

if not data:
    print("Aucune donnee recuperee. Verifie ta connexion internet.")
    input("\nAppuie sur Entree pour fermer...")
else:
    html    = generer_html(data, label_domaine, label_contrat)
    fichier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nDashboard genere !")
    print("Ouverture dans le navigateur...")
    webbrowser.open(f"file:///{fichier}")
    input("\nAppuie sur Entree pour fermer...")
