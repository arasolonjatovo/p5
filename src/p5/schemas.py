from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class EmployeeDataInput(BaseModel):
    # Variables numériques
    age: float = Field(..., ge=18, le=70, description="Âge de l'employé (18 à 70 ans)")
    revenu_mensuel: float = Field(..., ge=0, description="Revenu mensuel en euros")
    nombre_experiences_precedentes: float = Field(
        ..., ge=0, description="Nombre d'entreprises précédentes"
    )
    annee_experience_totale: float = Field(
        ..., ge=0, description="Années totales d'expérience"
    )
    annees_dans_l_entreprise: float = Field(
        ..., ge=0, description="Ancienneté dans l'entreprise"
    )
    annees_dans_le_poste_actuel: float = Field(
        ..., ge=0, description="Ancienneté dans le poste actuel"
    )
    nombre_participation_pee: float = Field(
        ..., ge=0, description="Nombre de participations au PEE"
    )
    nb_formations_suivies: float = Field(
        ..., ge=0, description="Nombre de formations suivies l'an dernier"
    )
    distance_domicile_travail: float = Field(
        ..., ge=0, description="Distance domicile-travail en km"
    )
    niveau_education: float = Field(
        ..., ge=1, le=5, description="Niveau d'études (1 à 5)"
    )
    annees_depuis_la_derniere_promotion: float = Field(
        ..., ge=0, description="Nombre d'années depuis la dernière promotion"
    )
    annes_sous_responsable_actuel: float = Field(
        ..., ge=0, description="Années sous le responsable actuel"
    )
    satisfaction_employee_environnement: float = Field(
        ..., ge=1, le=4, description="Satisfaction environnement (1 à 4)"
    )
    note_evaluation_precedente: float = Field(
        ..., ge=1, le=4, description="Note d'évaluation précédente (1 à 4)"
    )
    niveau_hierarchique_poste: float = Field(
        ..., ge=1, le=5, description="Niveau hiérarchique du poste (1 à 5)"
    )
    satisfaction_employee_nature_travail: float = Field(
        ..., ge=1, le=4, description="Satisfaction nature du travail (1 à 4)"
    )
    satisfaction_employee_equipe: float = Field(
        ..., ge=1, le=4, description="Satisfaction équipe (1 à 4)"
    )
    satisfaction_employee_equilibre_pro_perso: float = Field(
        ..., ge=1, le=4, description="Satisfaction équilibre pro/perso (1 à 4)"
    )
    note_evaluation_actuelle: float = Field(
        ..., ge=1, le=4, description="Note d'évaluation actuelle (1 à 4)"
    )
    augementation_salaire_precedente: float = Field(
        ..., ge=0, description="Pourcentage d'augmentation de salaire précédente"
    )

    # Variables catégorielles
    genre: Literal["M", "F"] = Field(..., description="Genre de l'employé")
    statut_marital: Literal["Divorcé(e)", "Marié(e)", "Célibataire"] = Field(
        ..., description="Statut marital"
    )
    departement: Literal["Consulting", "Ressources Humaines", "R&D", "Autre"] = Field(
        ..., description="Département"
    )
    poste: Literal[
        "Cadre Commercial",
        "Consultant",
        "Directeur Technique",
        "Manager",
        "Représentant Commercial",
        "Ressources Humaines",
        "Senior Manager",
        "Tech Lead",
        "Autre",
    ] = Field(..., description="Poste occupé")
    domaine_etude: Literal[
        "Entrepreunariat",
        "Infra & Cloud",
        "Marketing",
        "Ressources Humaines",
        "Transformation Digitale",
        "Autre",
    ] = Field(..., description="Domaine d'études principal")
    frequence_deplacement: Literal["Frequent", "Occasionnel", "Rare/Aucun"] = Field(
        ..., description="Fréquence des déplacements"
    )
    heure_supplementaires: bool = Field(
        ..., description="Effectue des heures supplémentaires (True/False)"
    )

    # Configuration Pydantic V2
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 35.0,
                "revenu_mensuel": 4500.0,
                "nombre_experiences_precedentes": 2.0,
                "annee_experience_totale": 10.0,
                "annees_dans_l_entreprise": 4.0,
                "annees_dans_le_poste_actuel": 3.0,
                "nombre_participation_pee": 1.0,
                "nb_formations_suivies": 2.0,
                "distance_domicile_travail": 12.0,
                "niveau_education": 4.0,
                "annees_depuis_la_derniere_promotion": 1.0,
                "annes_sous_responsable_actuel": 2.0,
                "satisfaction_employee_environnement": 3.0,
                "note_evaluation_precedente": 3.0,
                "niveau_hierarchique_poste": 2.0,
                "satisfaction_employee_nature_travail": 4.0,
                "satisfaction_employee_equipe": 3.0,
                "satisfaction_employee_equilibre_pro_perso": 3.0,
                "note_evaluation_actuelle": 3.0,
                "augementation_salaire_precedente": 14.0,
                "genre": "M",
                "statut_marital": "Marié(e)",
                "departement": "Consulting",
                "poste": "Consultant",
                "domaine_etude": "Infra & Cloud",
                "frequence_deplacement": "Occasionnel",
                "heure_supplementaires": True,
            }
        }
    )


class PredictionOutput(BaseModel):
    prediction: int = Field(..., description="Prédiction binaire (0 ou 1)")
    probabilite_attrition: float = Field(
        ..., description="Probabilité estimée du risque d'attrition/départ"
    )
    status: str = "success"
