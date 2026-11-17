"""
package_zip.py
--------------
Packages the complete agent-architecture-demo source code into a clean ZIP archive.
"""

import os
import zipfile

def package_source_code(project_dir: str, zip_path: str):
    print(f"[*] Packaging {project_dir} into {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            # Exclude unwanted cache directories
            dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', '.pytest_cache')]
            for file in files:
                if file.endswith(('.pyc', '.pyo')):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, os.path.dirname(project_dir))
                zipf.write(file_path, rel_path)
                print(f"  + Added: {rel_path}")

    print(f"[+] ZIP archive successfully created: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proj_folder = os.path.join(current_dir, "agent-architecture-demo")
    
    zip_dest_root = os.path.join(current_dir, "agent-architecture-demo-source-code.zip")
    zip_dest_proj = os.path.join(proj_folder, "agent-architecture-demo-source-code.zip")

    package_source_code(proj_folder, zip_dest_root)
    package_source_code(proj_folder, zip_dest_proj)

