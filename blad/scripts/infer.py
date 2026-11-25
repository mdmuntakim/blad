#!/usr/bin/env python3
"""Blad AI Model Inference Script.

Run inference with the Blad GGUF model.

Usage:
    python3 scripts/infer.py -m models/blad-1b-q4.gguf -p "Your prompt here"
"""

import argparse
import sys

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


def check_dependencies():
    """Check if required dependencies are available."""
    if not TRANSFORMERS_AVAILABLE:
        print("ERROR: transformers and torch are required.")
        print("Install with: pip install transformers torch")
        sys.exit(1)
    
    try:
        import optimum
        print("optimum version:", optimum.__version__)
    except ImportError:
        print("Note: optimum not installed. GGUF backend may not be available.")
        print("Install with: pip install optimum-gguf")


def run_with_transformers(model_path, prompt, max_tokens=256, temperature=0.7):
    """Run inference using transformers library."""
    print(f"Loading model: {model_path}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            use_authenticated_model=True
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map='auto',
            torch_dtype='auto'
        )
        
        print("Model loaded successfully!")
        print(f"Prompt: {prompt}")
        
        inputs = tokenizer(prompt, return_tensors='pt')
        
        # Move inputs to the correct device
        if hasattr(inputs, 'to'):
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove the prompt from the response
        if response.startswith(prompt):
            response = response[len(prompt):]
        
        print("\n" + "="*50)
        print("Response:")
        print("="*50)
        print(response)
        print("="*50)
        
    except Exception as e:
        print(f"Error during inference: {e}")
        import traceback
        traceback.print_exc()


def run_simple_demo(prompt, max_tokens=100):
    """Simple demo mode without model loading."""
    print("Running in demo mode (no model loaded)")
    print(f"Prompt: {prompt}")
    print("-" * 40)
    
    # Simple template-based responses
    if "python" in prompt.lower() or "code" in prompt.lower():
        print(">>> # Generated Python code (demo):")
        print(">>> def reverse_string(s):")
        print(">>>     return s[::-1]")
        print(">>> ")
        print(">>> >>> reverse_string('hello')")
        print(">>> 'olleh'")
    elif "hello" in prompt.lower():
        print(">>> Hello! How can I help you today?")
    elif "question" in prompt.lower():
        print(">>> That's a great question! I'm running in demo mode.")
        print(">>> For full capabilities, load a Blad model.")
    else:
        print(">>> I'm Blad, a generative AI assistant.")
        print(">>> I can help with coding, writing, and answering questions.")
        print(">>> Use --model flag to load a GGUF model.")


def main():
    parser = argparse.ArgumentParser(description="Blad AI Model Inference")
    parser.add_argument("-m", "--model", required=True, 
                        help="Path to GGUF model file (e.g., models/blad-1b-q4.gguf)")
    parser.add_argument("-p", "--prompt", required=True, 
                        help="Prompt to send to the model")
    parser.add_argument("-n", "--max-tokens", type=int, default=256,
                        help="Maximum tokens to generate (default: 256)")
    parser.add_argument("-t", "--temperature", type=float, default=0.7,
                        help="Sampling temperature (default: 0.7)")
    parser.add_argument("--demo", action="store_true",
                        help="Run in demo mode without loading model")
    
    args = parser.parse_args()
    
    # Validate model file exists
    import os
    if not os.path.exists(args.model):
        print(f"Error: Model file not found: {args.model}")
        sys.exit(1)
    
    # Check if in demo mode
    if args.demo:
        run_simple_demo(args.prompt, args.max_tokens)
        return
    
    # Check dependencies
    check_dependencies()
    
    # Run inference
    run_with_transformers(args.model, args.prompt, args.max_tokens, args.temperature)


if __name__ == "__main__":
    main()