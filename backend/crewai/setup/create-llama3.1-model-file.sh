#!/bin/sh

model_name="llama3.1"
custom_model_name="crewai-analysis-llama3.1"

ollama pull "$model_name"

ollama create "$custom_model_name" -f ./setup/Llama3.1Modelfile