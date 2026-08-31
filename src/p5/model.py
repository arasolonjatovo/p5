import logging

import joblib
import pandas as pd

from .schemas import EmployeeDataInput

logger = logging.getLogger(__name__)

FEATURE_NAMES = [
    "Unnamed: 0",
    "age",
    "revenu_mensuel",
    "nombre_experiences_precedentes",
    "annee_experience_totale",
    "annees_dans_l_entreprise",
    "annees_dans_le_poste_actuel",
    "nombre_participation_pee",
    "nb_formations_suivies",
    "distance_domicile_travail",
    "niveau_education",
    "annees_depuis_la_derniere_promotion",
    "annes_sous_responsable_actuel",
    "satisfaction_employee_environnement",
    "note_evaluation_precedente",
    "niveau_hierarchique_poste",
    "satisfaction_employee_nature_travail",
    "satisfaction_employee_equipe",
    "satisfaction_employee_equilibre_pro_perso",
    "note_evaluation_actuelle",
    "augementation_salaire_precedente",
    "genre_M",
    "statut_marital_Divorc©(e)",
    "statut_marital_Mari©(e)",
    "departement_Consulting",
    "departement_Ressources Humaines",
    "poste_Cadre Commercial",
    "poste_Consultant",
    "poste_Directeur Technique",
    "poste_Manager",
    "poste_Repr©sentant Commercial",
    "poste_Ressources Humaines",
    "poste_Senior Manager",
    "poste_Tech Lead",
    "domaine_etude_Entrepreunariat",
    "domaine_etude_Infra & Cloud",
    "domaine_etude_Marketing",
    "domaine_etude_Ressources Humaines",
    "domaine_etude_Transformation Digitale",
    "frequence_deplacement_Frequent",
    "frequence_deplacement_Occasionnel",
    "heure_supplementaires_1",
]


class MLModelWrapper:
    def __init__(self, model_path: str = "model.joblib"):
        self.model_path = model_path
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        try:
            self.pipeline = joblib.load(self.model_path)
            logger.info("Pipeline ML Scikit-Learn chargé avec succès.")
        except Exception as e:
            logger.warning(
                f"Impossible de charger '{self.model_path}' ({e}). Passage en mode simulation."
            )
            self.pipeline = None

    def _prepare_features(self, data: EmployeeDataInput) -> pd.DataFrame:
        """Transforme l'objet Pydantic en DataFrame à 41 colonnes conforme au modèle."""
        raw_dict = data.model_dump()

        encoded = {col: 0.0 for col in FEATURE_NAMES}
        encoded["Unnamed: 0"] = 0.0

        numeric_fields = [
            "age",
            "revenu_mensuel",
            "nombre_experiences_precedentes",
            "annee_experience_totale",
            "annees_dans_l_entreprise",
            "annees_dans_le_poste_actuel",
            "nombre_participation_pee",
            "nb_formations_suivies",
            "distance_domicile_travail",
            "niveau_education",
            "annees_depuis_la_derniere_promotion",
            "annes_sous_responsable_actuel",
            "satisfaction_employee_environnement",
            "note_evaluation_precedente",
            "niveau_hierarchique_poste",
            "satisfaction_employee_nature_travail",
            "satisfaction_employee_equipe",
            "satisfaction_employee_equilibre_pro_perso",
            "note_evaluation_actuelle",
            "augementation_salaire_precedente",
        ]
        for field in numeric_fields:
            encoded[field] = float(raw_dict[field])

        if raw_dict["genre"] == "M":
            encoded["genre_M"] = 1.0
        if raw_dict["statut_marital"] == "Divorcé(e)":
            encoded["statut_marital_Divorc©(e)"] = 1.0
        elif raw_dict["statut_marital"] == "Marié(e)":
            encoded["statut_marital_Mari©(e)"] = 1.0

        if raw_dict["departement"] == "Consulting":
            encoded["departement_Consulting"] = 1.0
        elif raw_dict["departement"] == "Ressources Humaines":
            encoded["departement_Ressources Humaines"] = 1.0

        poste_key = f"poste_{raw_dict['poste']}"
        if raw_dict["poste"] == "Représentant Commercial":
            encoded["poste_Repr©sentant Commercial"] = 1.0
        elif poste_key in encoded:
            encoded[poste_key] = 1.0

        domaine_key = f"domaine_etude_{raw_dict['domaine_etude']}"
        if domaine_key in encoded:
            encoded[domaine_key] = 1.0

        if raw_dict["frequence_deplacement"] == "Frequent":
            encoded["frequence_deplacement_Frequent"] = 1.0
        elif raw_dict["frequence_deplacement"] == "Occasionnel":
            encoded["frequence_deplacement_Occasionnel"] = 1.0

        if raw_dict["heure_supplementaires"]:
            encoded["heure_supplementaires_1"] = 1.0

        return pd.DataFrame([encoded], columns=FEATURE_NAMES)

    def predict(self, data: EmployeeDataInput):
        features_df = self._prepare_features(data)

        if self.pipeline:
            pred = int(self.pipeline.predict(features_df)[0])
            proba = float(self.pipeline.predict_proba(features_df)[0][1])
            return pred, round(proba, 4)

        return 0, 0.25


ml_service = MLModelWrapper()
