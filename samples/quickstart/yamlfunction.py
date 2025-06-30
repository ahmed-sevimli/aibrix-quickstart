import yamlfunction

def create_yaml(serve_port, http_port, model_name, model_path, image, container_name, max_model_len="12288", gpu_count="1"):
    data = [
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "labels": {
                    "model.aibrix.ai/name": model_name,
                    "model.aibrix.ai/port": str(serve_port)
                },
                "name": model_name,
                "namespace": "default"
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "model.aibrix.ai/name": model_name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "model.aibrix.ai/name": model_name
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "command": [
                                    "python3", "-m", "vllm.entrypoints.openai.api_server",
                                    "--host", "0.0.0.0",
                                    "--port", str(serve_port),
                                    "--uvicorn-log-level", "warning",
                                    "--model", model_path,
                                    "--served-model-name", model_name,
                                    "--max-model-len", max_model_len
                                ],
                                "image": image,
                                "imagePullPolicy": "IfNotPresent",
                                "name": container_name,
                                "ports": [
                                    {
                                        "containerPort": int(serve_port),
                                        "protocol": "TCP"
                                    }
                                ],
                                "resources": {
                                    "limits": {"nvidia.com/gpu": gpu_count},
                                    "requests": {"nvidia.com/gpu": gpu_count}
                                },
                                "livenessProbe": {
                                    "httpGet": {
                                        "path": "/health",
                                        "port": int(serve_port),
                                        "scheme": "HTTP"
                                    },
                                    "failureThreshold": 3,
                                    "periodSeconds": 5,
                                    "successThreshold": 1,
                                    "timeoutSeconds": 1
                                },
                                "readinessProbe": {
                                    "httpGet": {
                                        "path": "/health",
                                        "port": int(serve_port),
                                        "scheme": "HTTP"
                                    },
                                    "failureThreshold": 5,
                                    "periodSeconds": 5,
                                    "successThreshold": 1,
                                    "timeoutSeconds": 1
                                },
                                "startupProbe": {
                                    "httpGet": {
                                        "path": "/health",
                                        "port": int(serve_port),
                                        "scheme": "HTTP"
                                    },
                                    "failureThreshold": 30,
                                    "periodSeconds": 5,
                                    "successThreshold": 1,
                                    "timeoutSeconds": 1
                                }
                            }
                        ]
                    }
                }
            }
        },
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "labels": {
                    "model.aibrix.ai/name": model_name,
                    "prometheus-discovery": "true"
                },
                "annotations": {
                    "prometheus.io/scrape": "true",
                    "prometheus.io/port": http_port
                },
                "name": model_name,
                "namespace": "default"
            },
            "spec": {
                "ports": [
                    {"name": "serve", "port": int(serve_port), "protocol": "TCP", "targetPort": int(serve_port)},
                    {"name": "http", "port": int(http_port), "protocol": "TCP", "targetPort": int(http_port)}
                ],
                "selector": {
                    "model.aibrix.ai/name": model_name
                },
                "type": "ClusterIP"
            }
        }
    ]

    with open("model.yaml", "w") as f:
        yamlfunction.dump_all(data, f, sort_keys=False)

if __name__ == "__main__":
    port = input("Enter port (e.g. 8000): ")
    model_name = input("Enter model name (e.g. deepseek-r1-distill-llama-8b): ")
    model_path = input("Enter model path (e.g. deepseek-ai/DeepSeek-R1-Distill-Llama-8B): ")
    create_yaml(port, model_name, model_path)

