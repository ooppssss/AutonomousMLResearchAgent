from research_agent.preregistration.experiment_gate import ExperimentGate
from  research_agent.preregistration.models import (
    PreRegistration,
    ResearchQuestion,
    Prediction,
    Evaluation,
    Rationale,
)

from research_agent.preregistration.registry import (
    PreregistrationRegistry,
)


prereg = PreRegistration(
    preregistration_id="PR-001",

    research_question=ResearchQuestion(
        objective="Determine whether XGBoost improves diabetes prediction.",
        task_type="binary_classification",
        dataset="diabetes.csv",
    ),

    hypothesis=(
        "XGBoost will improve ROC-AUC compared "
        "with logistic regression."
    ),

    null_hypothesis=(
        "XGBoost will not improve ROC-AUC "
        "compared with logistic regression."
    ),

    prediction=Prediction(
        metric="roc_auc",
        baseline="logistic_regression",
        candidate="xgboost",
        predicted_difference=0.03,
        direction="greater_than",
        acceptance_threshold=0.03,
    ),

    evaluation=Evaluation(
        protocol="5-fold stratified cross-validation",
        primary_metric="roc_auc",
    ),

    rationale=Rationale(
        reason="XGBoost can model nonlinear relationships.",
        mechanism="nonlinear_feature_interactions",
    ),

    falsifier=(
        "Reject H1 if the ROC-AUC improvement "
        "is less than 0.03."
    ),
)


registry = PreregistrationRegistry()

# Validate
valid, errors = registry.validate(prereg)

print("Valid:", valid)
print("Errors:", errors)

# Lock
registry.lock(prereg)

print("Status:", prereg.status)
print("Hash:", prereg.content_hash)

# Verify
print(
    "Integrity:",
    registry.verify("PR-001")
)

gate = ExperimentGate(registry)
gate.authorize(prereg.preregistration_id)