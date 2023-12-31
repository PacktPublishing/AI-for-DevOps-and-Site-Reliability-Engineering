# My First LLM Code Generator
# This file contains code generated by GitHub Copilot and edited by a human.
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
from torchinfo import summary
import warnings; warnings.filterwarnings("ignore")  # Annoying warnings

llm_name = "Salesforce/codegen-350M-mono"
dummy_prompt = "def hello_world(): print('Hello, world!')"

# Generate code from a prompt
def generate(prompt):
    input_ids = tokenizer(prompt.strip(" \n"), return_tensors="pt")
    generated_ids = model.generate(**input_ids, max_new_tokens=256, do_sample=False, 
                                   num_beams=10, temperature=0.75)
    result = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return result

# Print PyTorch and Transformers versions
print("PyTorch version {} with Transformers version {}".format(
    torch.__version__, transformers.__version__))

# Load the model and tokenizer
print("Loading model {}...".format(llm_name))
model = AutoModelForCausalLM.from_pretrained(llm_name, pad_token_id=50256)
print("Loading tokenizer {}...".format(llm_name))
tokenizer = AutoTokenizer.from_pretrained(llm_name)
print("Model and tokenizer loaded.")

# Summmarize the PyTorch model
print("Model summary:")
summary(model, depth=5)
print()

# Summarize the tokenizer
print("Tokenizer summary:")
print(f"Tokenizer vocabulary size is {tokenizer.vocab_size}")
encoded = tokenizer.encode(dummy_prompt)
decoded = "|".join([tokenizer.decode(token) for token in encoded])
print(f"Dummy prompt: {dummy_prompt} \nEncoded:     {encoded}\nRound trip:  |{decoded}|")

# Read prompts from the user and generate code
while True:
    prompt = input("\nEnter a function signature or description: ")
    if prompt == "": break
    print(generate(prompt))
    print("Press Enter to exit or type another prompt.")
