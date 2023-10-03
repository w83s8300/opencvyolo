import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation import GenerationConfig

model_name = 'Qwen/Qwen-7B-Chat'
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
# max_memory = f'{int(torch.cuda.mem_get_info()[0]/1024**3)-2}GB'
# n_gpus = torch.cuda.device_count()
# max_memory = {i: max_memory for i in range(n_gpus)}
model = AutoModelForCausalLM.from_pretrained(
  model_name,
  device_map='auto',
  trust_remote_code=True,
  fp16=True
)
model = model.eval()
