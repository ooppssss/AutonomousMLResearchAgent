from pydantic import BaseModel


class ExperimentSpecification(BaseModel):
    # Dataset to use for the experiment
    dataset: str

    # Type of ML task, e.g. classification, regression
    task_type: str

    # Baseline model
    baseline_model: str

    # Candidate model
    candidate_model: str

    # Metric used to compare the models
    metric: str

    # Random seed for reproducibility
    random_seed: int = 42

    # Evaluation protocol
    evaluation_protocol: str

    # Expected improvement from the preregistration
    predicted_difference: float

    # Minimum improvement required to accept the hypothesis
    acceptance_threshold: float