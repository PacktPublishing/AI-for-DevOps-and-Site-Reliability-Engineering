# This code has been generated by GitHub Copilot and edited/fixed by a human.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Suppress warning messages
from absl import logging
logging.set_verbosity(logging.ERROR) # Suppress deprecation warnings
import urllib.request
import tempfile

import tensorflow as tf
from tfx import v1 as tfx
import tensorflow_data_validation as tfdv
import tensorflow_transform as tft
import tensorflow_model_analysis as tfma
from tfx.components import CsvExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Trainer, Evaluator
from tfx.proto import example_gen_pb2, trainer_pb2, evaluator_pb2
from tfx.orchestration.experimental.interactive.interactive_context import InteractiveContext

print('TensorFlow version: {}'.format(tf.__version__))
print('TFX version: {}'.format(tfx.__version__))

# Name our pipeline
PIPELINE_NAME = "penguin-simple"
# Output directory to store artifacts generated from the pipeline.
PIPELINE_ROOT = os.path.join('pipelines', PIPELINE_NAME)
# Path to a SQLite DB file to use as an MLMD storage.
METADATA_PATH = os.path.join('metadata', PIPELINE_NAME, 'metadata.db')
# Output directory where created models from the pipeline will be exported.
SERVING_MODEL_DIR = os.path.join('serving_model', PIPELINE_NAME)
# Python code for training the model
MODEL_TRAINER_CODE = 'penguin_trainer.py'
# Retrive sample dataset and set the path to it
# Create a temporary directory.
DATA_ROOT = tempfile.mkdtemp(prefix='tfx-data')
# Download the dataset from TFX tutorial and save it to the temporary directory.
data_url = 'https://raw.githubusercontent.com/tensorflow/tfx/master/tfx/examples/penguin/data/labelled/penguins_processed.csv'
data_filepath = os.path.join(DATA_ROOT, "data.csv")
urllib.request.urlretrieve(data_url, data_filepath)

# Check the contents of the dataset file
with open(data_filepath) as input_file:
    head = [next(input_file) for _ in range(20)]
print(head)

# Create a CsvExampleGen component
# Takes csv data, and generates train and eval examples for downstream components.
example_gen = tfx.components.CsvExampleGen(input_base=DATA_ROOT)

# Create a StatisticsGen component
# generates features statistics over both training and serving data, which can be used by other pipeline components.
statistics_gen = tfx.components.StatisticsGen(examples=example_gen.outputs['examples'])

# Create a SchemaGen component
# Generates a schema, which is consumed by the other pipeline components.
schema_gen = tfx.components.SchemaGen(statistics=statistics_gen.outputs['statistics'])

# Create an ExampleValidator component
# Identifies anomalies in training and serving data.
example_validator = ExampleValidator(
    statistics=statistics_gen.outputs['statistics'],
    schema=schema_gen.outputs['schema'])

# Create a Trainer component
# Trains a TensorFlow ML model on the training data.
trainer = tfx.components.Trainer(
    module_file=MODEL_TRAINER_CODE,
    schema=schema_gen.outputs['schema'],
    examples=example_gen.outputs['examples'],
    train_args=trainer_pb2.TrainArgs(num_steps=100),
    eval_args=trainer_pb2.EvalArgs(num_steps=50))

# Creates a Pusher component
# Pushes the model to a filesystem destination.
pusher = tfx.components.Pusher(
    model=trainer.outputs['model'],
    push_destination=tfx.proto.PushDestination(
        filesystem=tfx.proto.PushDestination.Filesystem(
            base_directory=SERVING_MODEL_DIR)))

# Create an EvalConfig
# Defines the set of metrics computed by TFX Model Evaluation.
# In this case, we are computing the sparse_categorical_accuracy metric for the overall slice and for each penguin species.
# Calibrated for the penguin dataset, where the threshold is set to 0.6.
eval_config = tfma.EvalConfig(
    model_specs=[tfma.ModelSpec(label_key='species')],
    slicing_specs=[
        # An empty slice spec means the overall slice, i.e. the whole dataset.
        tfma.SlicingSpec(),
        # Calculate metrics for each penguin species.
        tfma.SlicingSpec(feature_keys=['species']),
        ],
    metrics_specs=[
        tfma.MetricsSpec(per_slice_thresholds={
            'sparse_categorical_accuracy':
                tfma.PerSliceMetricThresholds(thresholds=[
                    tfma.PerSliceMetricThreshold(
                        slicing_specs=[tfma.SlicingSpec()],
                        threshold=tfma.MetricThreshold(
                            value_threshold=tfma.GenericValueThreshold(
                                lower_bound={'value': 0.6}),
                            # Change threshold will be ignored if there is no
                            # baseline model resolved from MLMD (first run).
                            change_threshold=tfma.GenericChangeThreshold(
                                direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                                absolute={'value': -1e-10}))
                    )]),
        })],
    )

# Create a Resolver component
# Resolves the latest blessed model for model validation.
model_resolver = tfx.dsl.Resolver(
    strategy_class=tfx.dsl.experimental.LatestBlessedModelStrategy,
    model=tfx.dsl.Channel(type=tfx.types.standard_artifacts.Model),
    model_blessing=tfx.dsl.Channel(
        type=tfx.types.standard_artifacts.ModelBlessing)).with_id(
            'latest_blessed_model_resolver')

# Create an Evaluator component
# Evaluates the trained model using a validation dataset.
evaluator = tfx.components.Evaluator(
      examples=example_gen.outputs['examples'],
      model=trainer.outputs['model'],
      baseline_model=model_resolver.outputs['model'],
      eval_config=eval_config)

# Add all the components to an array
components = [ example_gen, 
              statistics_gen, 
              schema_gen, 
              example_validator, 
              trainer,
              model_resolver,
              evaluator,
              pusher 
             ]

# Create a TFX pipeline with the components
pipeline = tfx.dsl.Pipeline(
    pipeline_name=PIPELINE_NAME,
    pipeline_root=PIPELINE_ROOT,
    metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(METADATA_PATH),
    components=components)

# Run the pipeline using DAG runner
# DAG runner orchestrates the execution of the pipeline based on the dependencies among each component.
tfx.orchestration.LocalDagRunner().run(pipeline)