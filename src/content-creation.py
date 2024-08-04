# content_creation.py
import json
import os

def save_debug_info(name, content_type, data):
    debug_folder = f"debug/content/{name}"
    os.makedirs(debug_folder, exist_ok=True)
    
    with open(f"{debug_folder}/{content_type}.json", "w") as f:
        json.dump(data, f, indent=2)

def process_name(name):
    from workers import content_creation_worker
    result = content_creation_worker(name)
    
    save_debug_info(name, "audio", {"script": result["audio_script"]})
    save_debug_info(name, "scene_description", {"description": result["scene_description"]})
    
    return result

if __name__ == "__main__":
    # This can be replaced with reading from an input table
    names = ["Albert Einstein", "Marie Curie", "Isaac Newton"]
    
    for name in names:
        process_name(name)