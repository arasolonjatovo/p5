from p5.main import app 
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_predict_success():
    payload = {
        "age": 32.0,
        "revenu_mensuel": 3200.0,
        "nombre_experiences_precedentes": 1.0,
        "annee_experience_totale": 6.0,
        "annees_dans_l_entreprise": 3.0,
        "annees_dans_le_poste_actuel": 2.0,
        "nombre_participation_pee": 0.0,
        "nb_formations_suivies": 1.0,
        "distance_domicile_travail": 5.0,
        "niveau_education": 3.0,
        "annees_depuis_la_derniere_promotion": 0.0,
        "annes_sous_responsable_actuel": 2.0,
        "satisfaction_employee_environnement": 2.0,
        "note_evaluation_precedente": 3.0,
        "niveau_hierarchique_poste": 1.0,
        "satisfaction_employee_nature_travail": 3.0,
        "satisfaction_employee_equipe": 2.0,
        "satisfaction_employee_equilibre_pro_perso": 2.0,
        "note_evaluation_actuelle": 3.0,
        "augementation_salaire_precedente": 11.0,
        "genre": "M",
        "statut_marital": "Célibataire",
        "departement": "Consulting",
        "poste": "Consultant",
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Frequent",
        "heure_supplementaires": True,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probabilite_attrition" in response.json()


def test_predict_validation_error():

    payload = {
        "age": 10.0,
        "revenu_mensuel": 3200.0,
        "genre": "M",
        "statut_marital": "Célibataire",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
