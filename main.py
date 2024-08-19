#!/usr/bin/env python3

import os
import sys
import subprocess

# Configs
CDAP_URL = "http://127.0.0.1:11015"
OFFLINE_MODE = True  # Use cached dependencies


def upload_to_cdap(target_dir) -> bool:
    print("Locating target files")
    jar_files = [file for file in os.listdir(target_dir) if file.endswith(".jar")][:1]
    json_files = [file for file in os.listdir(target_dir) if file.endswith(".json")][:1]
    if len(jar_files) | len(json_files) == 0:
        print("JAR/Json Files missing")
        return False

    json_file, jar_file = json_files[0], jar_files[0]
    print("Found:", jar_file, json_file)

    print("Uploading to CDAP")
    os.chdir(target_dir)
    return subprocess.call(["cdap", "cli", "-l", CDAP_URL, "load", "artifact", jar_file, "config-file",
                            json_file]) == 0  # cdap cli always returns 0


def build_project(work_dir: str) -> bool:
    if not os.path.isfile(os.path.join(work_dir, "pom.xml")):
        print("pom.xml file missing")
        return False

    print("Building project")
    build_command = ["mvn", "clean", "package", "-DskipTests", "-Dstyle.color=always"]
    if OFFLINE_MODE:
        build_command.append("-o")
    proc = subprocess.run(build_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print(f"Build failed. Exited with code: ", proc.returncode)
        print(proc.stdout.decode("utf-8"))
        print(proc.stderr.decode("utf-8"))
        return False
    print("Build successful")
    return True


def main():
    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, "target")
    
    if len(sys.argv) > 1 and sys.argv[1] == "-u":
        print("Uploading to CDAP")
        if not upload_to_cdap(target_dir):
            print("Upload failed")
            sys.exit(1)
        return
    
    
    if not (build_project(current_dir) and upload_to_cdap(target_dir)):
        print("Build or Upload failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
