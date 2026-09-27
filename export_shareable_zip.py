import os
import sys
import zipfile

# Ensure UTF-8 output encoding for Windows command line compatibility
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

EXCLUDE_DIRS = {'.venv', 'venv', '__pycache__', '.git', '.pytest_cache', '.idea', '.vscode'}
EXCLUDE_EXTS = {'.pyc', '.log'}

def create_shareable_zip():
    project_root = os.path.dirname(os.path.abspath(__file__))
    zip_filename = os.path.join(project_root, "Bharat_Quest_SIH_Project.zip")
    
    print("=" * 60)
    print("[EXPORT] Creating clean, lightweight shareable ZIP archive...")
    print(f"[TARGET] {zip_filename}")
    print("=" * 60)
    
    file_count = 0
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file == "Bharat_Quest_SIH_Project.zip":
                    continue
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDE_EXTS:
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_root)
                zipf.write(full_path, rel_path)
                file_count += 1
                
    zip_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"[SUCCESS] Archive created successfully!")
    print(f"[STATS]   Total Files: {file_count}")
    print(f"[SIZE]    File Size:   {zip_size_mb:.2f} MB")
    print("\n[NOTE] You can now copy 'Bharat_Quest_SIH_Project.zip' to a USB drive,")
    print("       Google Drive, or send it to your team!")

if __name__ == "__main__":
    create_shareable_zip()
