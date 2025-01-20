#!/bin/sh

model_name="llama3.2"
custom_model_name="crewai-analysis-llama3.2"

ollama pull "$model_name"

ollama create "$custom_model_name" -f ./setup/Llama3.2Modelfile