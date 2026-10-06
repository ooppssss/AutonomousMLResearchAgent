from research_agent.preregistration.models import PreRegistration
from .specification import ExperimentSpecification
from pathlib import Path


class ExperimentSpecificationGenerator:

    def generate(
        self,
        prereg: PreRegistration
    ) -> ExperimentSpecification:
        """
        Convert a locked preregistration into an
        experiment specification.

        Later, this can be extended with the LLM
        to generate more complex experiment plans.
        """

        return ExperimentSpecification(
            dataset=prereg.research_question.dataset,
            task_type=prereg.research_question.task_type,
            baseline_model=prereg.prediction.baseline,
            candidate_model=prereg.prediction.candidate,
            metric=prereg.prediction.metric,
            random_seed=prereg.evaluation.random_seed,
            evaluation_protocol=prereg.evaluation.protocol,
            predicted_difference=prereg.prediction.predicted_difference,
            acceptance_threshold=prereg.prediction.acceptance_threshold,
        )




class ExperimentScriptGenerator:

    def __init__(self, output_directory="generated_experiments"):
        # Directory where generated experiment scripts will be stored
        self.output_directory = Path(output_directory)

        # Create the directory if it doesn't exist
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate(
        self,
        spec: ExperimentSpecification,
        experiment_id: str
    ) -> Path:
        """
        Generate a Python experiment script from
        an ExperimentSpecification.
        """

        # Generate the Python source code
        script = self._build_script(spec)

        # Decide where to save the generated script
        script_path = self.output_directory / f"{experiment_id}.py"

        # Write the generated Python code to disk
        script_path.write_text(
            script,
            encoding="utf-8"
        )

        return script_path

    def _build_script(
        self,
        spec: ExperimentSpecification
    ) -> str:
        """
        Build the actual Python experiment code.

        This is intentionally simple for now.
        Later, the LLM can generate more sophisticated
        experiment code.
        """

        return f'''"""
Auto-generated ML experiment.

Dataset: {spec.dataset}
Task: {spec.task_type}
Baseline: {spec.baseline_model}
Candidate: {spec.candidate_model}
Metric: {spec.metric}
Random Seed: {spec.random_seed}
"""

# Import required libraries here
# Example:
# import pandas as pd
# from sklearn.model_selection import train_test_split


def run_experiment():
    """
    Execute the ML experiment.
    """

    # TODO: Load the dataset
    dataset = "{spec.dataset}"

    # TODO: Train the baseline model
    baseline_model = "{spec.baseline_model}"

    # TODO: Train the candidate model
    candidate_model = "{spec.candidate_model}"

    # TODO: Calculate the evaluation metric
    metric = "{spec.metric}"

    # TODO: Compare baseline and candidate
    predicted_difference = {spec.predicted_difference}

    # TODO: Implement the actual experiment
    print("Dataset:", dataset)
    print("Baseline:", baseline_model)
    print("Candidate:", candidate_model)
    print("Metric:", metric)
    print("Predicted difference:", predicted_difference)


if __name__ == "__main__":
    run_experiment()
'''