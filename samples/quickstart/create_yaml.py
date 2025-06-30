from yamlfunction import create_yaml

serve_port = input("Enter port (e.g. 8000): ")
model_name = input("Enter model name (e.g. deepseek-r1-distill-llama-8b): ")
model_path = input("Enter model path (e.g. deepseek-ai/DeepSeek-R1-Distill-Llama-8B): ")
gpu_count = "1"
# 24k length, this is to avoid "The model's max seq len (131072) is larger than the maximum number of tokens that can be stored in KV cache" issue.
max_model_len = "12288"
image = "vllm/vllm-openai:v0.7.1"
container_name = "vllm-openai"
http_port = "8080"

create_yaml(serve_port, http_port, model_name, model_path, image, container_name, max_model_len=max_model_len, gpu_count=gpu_count)