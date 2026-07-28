import os

def main():
    mode = os.environ.get("CTF_MODE")
    if mode == "unlocked":
        print("cofc{env_v4rs_m4tter}")
    else:
        print("Nothing to see here.")

if __name__ == "__main__":
    main()
