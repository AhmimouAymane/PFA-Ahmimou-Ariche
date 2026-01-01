"""
Test Ollama Models - Compare performance for Moroccan Admin Chatbot
"""
import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.ollama_service import OllamaService

# Test queries in different languages
test_queries = {
    "french_basic": "Comment obtenir une carte d'identité?",
    "french_followup": "Combien ça coûte?",
    "arabic": "كيف احصل على جواز السفر؟",
    "vague": "Je veux me marier",
    "comparison": "Quelle est la différence entre RAMED et CNSS?"
}

# Models to test
models_to_test = [
    "aya-expanse:8b",
    "command-r:7b",
    "qwen2.5:7b",
    "mistral:7b",
    "qwen2.5:0.5b"
]

def test_model(ollama: OllamaService, model: str, query: str) -> dict:
    """Test a single model with a query"""
    try:
        start_time = time.time()
        
        response = ollama.generate(
            model=model,
            prompt=query,
            system="Tu es un assistant expert en administration publique marocaine.",
            temperature=0.7,
            max_tokens=500
        )
        
        duration = time.time() - start_time
        
        return {
            "success": response is not None,
            "response": response[:200] if response else "ERROR",
            "duration": duration,
            "tokens": len(response.split()) if response else 0
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"ERROR: {str(e)}",
            "duration": 0,
            "tokens": 0
        }

def main():
    print("=" * 80)
    print("OLLAMA MODEL COMPARISON FOR MOROCCAN ADMIN CHATBOT")
    print("=" * 80)
    
    ollama = OllamaService()
    
    # Check Ollama is running
    if not ollama.check_ollama_running():
        print("\\n❌ ERROR: Ollama is not running!")
        print("Please start Ollama first.")
        return
    
    # List available models
    available_models = ollama.list_models()
    print(f"\\n📦 Available Models: {len(available_models)}")
    for model in available_models:
        print(f"   - {model}")
    
    # Filter to only test available models
    models_to_test_filtered = [m for m in models_to_test if any(m in avail for avail in available_models)]
    
    if not models_to_test_filtered:
        print("\\n⚠️  No models from our test list are installed!")
        print("\\nRecommended models to download:")
        for model in models_to_test:
            print(f"   ollama pull {model}")
        return
    
    print(f"\\n🧪 Testing {len(models_to_test_filtered)} models with {len(test_queries)} queries...")
    print()
    
    # Results storage
    results = {model: {} for model in models_to_test_filtered}
    
    # Test each model
    for i, model in enumerate(models_to_test_filtered, 1):
        print(f"\\n[{i}/{len(models_to_test_filtered)}] Testing: {model}")
        print("-" * 80)
        
        for query_name, query in test_queries.items():
            print(f"\\n  Query: {query_name}")
            print(f"  \"{query}\"")
            
            result = test_model(ollama, model, query)
            results[model][query_name] = result
            
            if result["success"]:
                print(f"  ✓ Response ({result['duration']:.1f}s, {result['tokens']} tokens):")
                print(f"    {result['response']}...")
            else:
                print(f"  ✗ {result['response']}")
    
    # Summary
    print("\\n" + "=" * 80)
    print("SUMMARY - AVERAGE PERFORMANCE")
    print("=" * 80)
    
    for model in models_to_test_filtered:
        model_results = results[model]
        successes = sum(1 for r in model_results.values() if r["success"])
        avg_duration = sum(r["duration"] for r in model_results.values() if r["success"]) / max(successes, 1)
        avg_tokens = sum(r["tokens"] for r in model_results.values() if r["success"]) / max(successes, 1)
        
        print(f"\\n📊 {model}")
        print(f"   Success Rate: {successes}/{len(test_queries)}")
        print(f"   Avg Response Time: {avg_duration:.1f}s")
        print(f"   Avg Tokens: {avg_tokens:.0f}")
    
    # Recommendation
    print("\\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    
    # Score models (success * tokens / time)
    scores = {}
    for model in models_to_test_filtered:
        model_results = results[model]
        successes = sum(1 for r in model_results.values() if r["success"])
        if successes > 0:
            avg_duration = sum(r["duration"] for r in model_results.values() if r["success"]) / successes
            avg_tokens = sum(r["tokens"] for r in model_results.values() if r["success"]) / successes
            scores[model] = (successes * avg_tokens) / max(avg_duration, 0.1)
        else:
            scores[model] = 0
    
    best_model = max(scores, key=scores.get) if scores else None
    if best_model:
        print(f"\\n🏆 Best Model: {best_model}")
        print(f"   (Score: {scores[best_model]:.2f})")
    
    print("\\n" + "=" * 80)

if __name__ == "__main__":
    main()
