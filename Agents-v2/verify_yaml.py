import yaml
import os
from pathlib import Path

BASE_DIR = Path("/Users/kevinlappe/Documents/vibelocity-orchestrator/Agents-v2/cloud-agent/yaml")

def validate_yaml_files():
    files = list(BASE_DIR.glob("*.yaml"))
    print(f"Found {len(files)} YAML files.")
    
    errors = []
    placeholders = []
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for placeholders
            if "REPLACE_ME" in content or "TODO" in content:
                placeholders.append(file_path.name)
                
            # Validate YAML syntax
            yaml.safe_load(content)
            
        except Exception as e:
            errors.append(f"{file_path.name}: {str(e)}")
            
    if errors:
        print("\n❌ YAML Validation Errors:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("\n✅ All files passed YAML validation.")
        
    if placeholders:
        print("\n⚠️  Files with placeholders (REPLACE_ME/TODO):")
        for p in placeholders:
            print(f"  - {p}")
    else:
        print("\n✅ No placeholders found.")

if __name__ == "__main__":
    validate_yaml_files()
