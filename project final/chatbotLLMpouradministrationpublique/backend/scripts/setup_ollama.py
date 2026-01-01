"""
Setup Ollama and Models - Installation Guide
Run this script to install Ollama and download the best models
"""
import subprocess
import os
import sys
import time

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def check_ollama_installed():
    """Check if Ollama command is available"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def wait_for_ollama_service():
    """Wait for Ollama service to be ready"""
    print("Waiting for Ollama service to start...")
    import requests
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("✓ Ollama service is running!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"  Waiting... ({i+1}/30)")
    return False

def pull_model(model_name):
    """Download a model using ollama pull"""
    print(f"\n📥 Downloading {model_name}...")
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            check=True
        )
        print(f"✓ {model_name} downloaded successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to download {model_name}")
        return False

def list_models():
    """List downloaded models"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("Could not list models")

def main():
    print_section("OLLAMA SETUP FOR MOROCCAN ADMIN CHATBOT")
    
    # Step 1: Check if Ollama is installed
    if check_ollama_installed():
        print("✓ Ollama is already installed!")
    else:
        print("⚠️  Ollama is not installed yet.")
        print("\n📋 INSTALLATION STEPS:")
        print("1. The installer (OllamaSetup.exe) should be in your Downloads folder")
        print("2. Double-click OllamaSetup.exe to install")
        print("3. Follow the installation wizard")
        print("4. After installation, Ollama will start automatically")
        print("\n👉 Please install Ollama now, then run this script again.")
        
        input("\nPress Enter after you've installed Ollama...")
        
        if not check_ollama_installed():
            print("\n❌ Ollama still not found. Please install and try again.")
            print("   Download from: https://ollama.com/download/windows")
            return
        
        print("\n✓ Ollama installation detected!")
    
    # Step 2: Wait for Ollama service
    print_section("CHECKING OLLAMA SERVICE")
    if not wait_for_ollama_service():
        print("\n❌ Ollama service is not running.")
        print("   Please start Ollama from the Start menu and try again.")
        return
    
    # Step 3: Download recommended models
    print_section("DOWNLOADING RECOMMENDED MODELS")
    print("We'll download models optimized for Arabic/French multilingual support")
    print("This will take several minutes and require ~5-10GB per model\n")
    
    # Recommended models in priority order
    models = [
        ("aya-expanse:8b", "Multilingual 8B (23 languages, Arabic optimized)"),
        ("command-r:7b", "Command R 7B (MENA region specialized)"),
        ("qwen2.5:7b", "Qwen 2.5 7B (Excellent multilingual)"),
    ]
    
    print("Models to download:")
    for i, (model, desc) in enumerate(models, 1):
        print(f"  {i}. {model} - {desc}")
    
    choice = input("\nDownload all recommended models? (y/n/custom): ").lower()
    
    if choice == 'custom':
        print("\nChoose models to download (e.g., '1,2' or '1 3'):")
        selection = input("> ").replace(',', ' ').split()
        try:
            selected_indices = [int(i) - 1 for i in selection]
            models_to_download = [models[i] for i in selected_indices]
        except (ValueError, IndexError):
            print("Invalid selection. Downloading first model only.")
            models_to_download = [models[0]]
    elif choice == 'n':
        print("\nDownloading only the first model (aya-expanse:8b)...")
        models_to_download = [models[0]]
    else:
        models_to_download = models
    
    # Download selected models
    success_count = 0
    for model, desc in models_to_download:
        if pull_model(model):
            success_count += 1
    
    # Step 4: Show results
    print_section("SETUP COMPLETE")
    print(f"✓ Successfully downloaded {success_count}/{len(models_to_download)} models\n")
    
    print("📦 Installed Models:")
    list_models()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Install Python dependencies: pip install -r requirements.txt")
    print("2. Test the models: python scripts/test_ollama_models.py")
    print("3. Start the chatbot: python app.py")
    print("\n✨ Your chatbot is ready to use!")

if __name__ == "__main__":
    main()
