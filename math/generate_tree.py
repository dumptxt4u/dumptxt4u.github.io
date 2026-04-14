# generate_tree.py
import os
import json

def generate_jstree_data(root_dir="."):
    tree = []
    root_id = "root"
    
    tree.append({
        "id": root_id,
        "parent": "#",
        "text": "Math Vault",
        "icon": "fas fa-infinity text-warning"
    })

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden folders and __pycache__
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
        
        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == ".":
            parent = root_id
        else:
            parent = rel_path.replace(os.sep, "/")
        
        # Add folders
        for dirname in dirnames:
            folder_path = os.path.join(rel_path, dirname).replace(os.sep, "/") if rel_path != "." else dirname
            tree.append({
                "id": folder_path,
                "parent": parent,
                "text": dirname,
                "icon": "fa fa-folder"
            })
        
        # Add files
        for filename in filenames:
            if filename.startswith('.') and filename != '.html': continue  # skip hidden files
            file_path = os.path.join(rel_path, filename).replace(os.sep, "/") if rel_path != "." else filename
            ext = filename.split('.')[-1].lower()
            
            icon = "fa fa-file-code"
            if ext == "pdf":
                icon = "fa fa-file-pdf text-danger"
            elif ext in ["png", "jpg", "jpeg", "svg", "gif"]:
                icon = "fa fa-file-image text-info"
            
            tree.append({
                "id": file_path,
                "parent": parent,
                "text": filename,
                "icon": icon,
                "type": "file"
            })
    
    return tree

if __name__ == "__main__":
    data = generate_jstree_data()
    with open("tree_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Tree data generated! {len(data)} items saved to tree_data.json")
