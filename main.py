#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse

# Configs
CDAP_URL = "http://127.0.0.1:11015"
OFFLINE_MODE = True  # Use cached dependencies
DEFAULT_NAMESPACE = "default"


def upload_to_cdap(target_dir, namespace) -> bool:
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
    return subprocess.call(["cdap", "cli", "-l", CDAP_URL, "--namespace", namespace,
                            "load", "artifact", jar_file, "config-file", json_file]) == 0  # cdap cli always returns 0


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
    
    parser = argparse.ArgumentParser(description="Build and upload project.")
    parser.add_argument("-u", "--upload", action="store_true", help="Only trigger upload")
    parser.add_argument("-n", "--namespace", type=str, default=DEFAULT_NAMESPACE, help="Specify namespace")
    args = parser.parse_args()
    
    if args.upload:
        print("Uploading to CDAP")
        if not upload_to_cdap(target_dir, args.namespace):
            print("Upload failed")
            sys.exit(1)
        return
    
    
    if not (build_project(current_dir) and upload_to_cdap(target_dir, args.namespace)):
        print("Build or Upload failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
