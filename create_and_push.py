import argparse
import yaml
import subprocess
import os

def run_command(cmd, check=True):
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=check)
        return True
    except subprocess.CalledProcessError:
        return False

def build_and_push_images(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    registry = config['registry'].replace('https://', '')
    run_command("git branch --set-upstream-to=origin/main $(git rev-parse --abbrev-ref HEAD)", check=False)
    run_command("git pull")
    
    for dockerfile in config['dockerfiles']:
        middle = dockerfile.split('/')[1]
        local_tag = f"mcp/{middle}"
        remote_tag = f"{registry}/{local_tag}"
        
        run_command(f"docker build -t {local_tag} -f {dockerfile} .")
        run_command(f"docker tag {local_tag} {remote_tag}")
        run_command(f"docker push {remote_tag}")
        
        print("\nDocker image built and pushed. Press Enter to continue...")
        input()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='YAML config file path')
    args = parser.parse_args()
    build_and_push_images(args.config)