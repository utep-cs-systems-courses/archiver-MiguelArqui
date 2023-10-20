import os
import sys
import struct

def create_archive(files):
    try:
        archive = open("mytar.tar", "wb")

        for file_name in files:
            with open(file_name, "rb") as f:
                file_data = f.read()
                file_size = os.path.getsize(file_name)
                header = struct.pack(f"{len(file_name)}sQ", file_name.encode(), file_size)
                archive.write(header + file_data)

        archive.close()
    except Exception as e:
        sys.stderr.write(f"Error creating archive: {str(e)}\n")
        sys.exit(1)

def extract_archive(archive_name):
    try:
        archive = open(archive_name, "rb")

        while True:
            header = archive.read(12)
            if not header:
                break

            file_name, file_size = struct.unpack("12sQ", header)
            file_name = file_name.decode().strip("\x00")
            file_data = archive.read(file_size)

            with open(file_name, "wb") as f:
                f.write(file_data)

        archive.close()
    except Exception as e:
        sys.stderr.write(f"Error extracting archive: {str(e)}\n")
        sys.exit(1)

if len(sys.argv) < 2:
    sys.stderr.write("Usage: mytar.py [c|x] [file1 file2 ... | archive_name]\n")
    sys.exit(1)

mode = sys.argv[1]

if mode == "c":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: mytar.py c [file1 file2 ...]\n")
        sys.exit(1)
    files = sys.argv[2:]
    create_archive(files)
elif mode == "x":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: mytar.py x [archive_name]\n")
        sys.exit(1)
    archive_name = sys.argv[2]
    extract_archive(archive_name)
else:
    sys.stderr.write("Invalid mode. Use 'c' to create or 'x' to extract.\n")
    sys.exit(1)
