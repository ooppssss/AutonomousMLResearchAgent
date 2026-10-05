from os import error

from .models import PreRegistration

class ValidationError(Exception):
    pass


def validate_preregistration(prereg: PreRegistration) -> list[str]:
    errors = []

    if not prereg.hypothesis.strip():
        errors.append("Hypothesis is missing.")
    if not prereg.null_hypothesis.strip():
        errors.append("Null hypothesis is missing.")
    if not prereg.prediction.metric:
        errors.append("Metric is missing.")
    if not prereg.prediction.baseline:
        errors.append("Baseline model is missing.")
    if not prereg.prediction.candidate:
        errors.append("Candidate model is missing.")
    if(prereg.prediction.baseline == prereg.prediction.candidate ):
        errors.append("Baseline and candidate cannot be the same.")
    if not prereg.falsifier.strip():
        errors.append("Falsifier is missing.")
    if not prereg.rationale.reason.strip():
        errors.append("Rationale is missing.")
    if not prereg.evaluation.protocol.strip():
        errors.append("Evaluation protocol is missing.")
    if prereg.prediction.acceptance_threshold < 0:
        errors.append("Acceptance threshold cannot be negative.")

    return errors


def is_valid(prereg: PreRegistration) -> bool:
    return len(validate_preregistration(prereg)) == 0