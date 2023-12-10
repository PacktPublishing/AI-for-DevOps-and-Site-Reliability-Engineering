import torch
import transformers
from transformers import AutoTokenizer, LlamaForCausalLM
from torchinfo import summary

llm_name = "CodeLlama-7b-Python-hf"

# Generate code from a prompt
def generate(prompt):
    input_ids = tokenizer(prompt.strip(" \n"), return_tensors="pt")
    generated_ids = model.generate(**input_ids, max_new_tokens=256, do_sample=False, 
                                   num_beams=10)
    result = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return result

# Print PyTorch and Transformers versions
print("PyTorch version {} with Transformers version {}".format(
    torch.__version__, transformers.__version__))

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(llm_name)

# Load the model
model = LlamaForCausalLM.from_pretrained(llm_name, pad_token_id=31999)

# Read prompts from the user and generate code
while True:
    prompt = input("\nEnter a function signature or description: ")
    if prompt == "": break
    print(generate(prompt))
    print("Press Enter to exit or type another prompt.")