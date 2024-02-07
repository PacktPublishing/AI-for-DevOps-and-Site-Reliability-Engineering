import tensorflow as tf
from tfx import v1 as tfx
import urllib.request
import tempfile
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress warning messages
import tensorflow_data_validation as tfdv
import tensorflow_transform as tft
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
DATA_ROOT = tempfile.mkdtemp(prefix='tfx-data')  # Create a temporary directory.
data_url = 'https://raw.githubusercontent.com/tensorflow/tfx/master/tfx/examples/penguin/data/labelled/penguins_processed.csv'
data_filepath = os.path.join(DATA_ROOT, "data.csv")
urllib.request.urlretrieve(data_url, data_filepath)

# Check the contents of the dataset file
with open(data_filepath) as input_file:
    head = [next(input_file) for _ in range(20)]
print(head)

# Create a CsvExampleGen component
example_gen = tfx.components.CsvExampleGen(input_base=DATA_ROOT)

# Create a StatisticsGen component
statistics_gen = tfx.components.StatisticsGen(examples=example_gen.outputs['examples'])

# Create a SchemaGen component
schema_gen = tfx.components.SchemaGen(statistics=statistics_gen.outputs['statistics'])

# Create an ExampleValidator component
example_validator = ExampleValidator(
    statistics=statistics_gen.outputs['statistics'],
    schema=schema_gen.outputs['schema'])

# Create a Trainer component
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

# Add all the components to an array
components = [ example_gen, 
              statistics_gen, 
              schema_gen, 
              example_validator, 
              trainer, 
              pusher ]

# Create a TFX pipeline
pipeline = tfx.dsl.Pipeline(
    pipeline_name=PIPELINE_NAME,
    pipeline_root=PIPELINE_ROOT,
    metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(METADATA_PATH),
    components=components)

# Run the pipeline using DAG runner
tfx.orchestration.LocalDagRunner().run(pipeline)