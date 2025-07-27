import os
import subprocess
import shutil

def get_newly_parsed_basenames(input_dir="./uploaded_documents"):
    # Files present in input_dir before Marker runs are the new files to parse
    basenames = []
    for fname in os.listdir(input_dir):
        base, _ = os.path.splitext(fname)
        basenames.append(base)
    return basenames

  
def parse_file():
    INPUT_DIR = "./uploaded_documents"
    OUTPUT_DIR = "./output"
    PARSED_DIR = "./parsed_documents"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PARSED_DIR, exist_ok=True)

    # Move already parsed files out
    for fname in os.listdir(INPUT_DIR):
        base, _ = os.path.splitext(fname)
        in_path = os.path.join(INPUT_DIR, fname)
        out_path = os.path.join(OUTPUT_DIR, base, f"{base}.md")

        if os.path.exists(out_path):
            print(f"✅ Already parsed: {fname}")
            shutil.move(in_path, os.path.join(PARSED_DIR, fname))


    remaining = os.listdir(INPUT_DIR)
    if not remaining:
        print("🎉 Nothing left to parse.")
        return []

    print(f"🔄 Parsing {len(remaining)} files...")
    cmd = [
        "marker",
        INPUT_DIR,
        "--use_llm",
        "--disable_image_extraction",
        "--output_dir",
        OUTPUT_DIR,
    ]
    subprocess.run(cmd, check=True)
    print("✅ Marker completed.")


