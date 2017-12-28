import sys
while True:
    line=raw_input()
    if line=='exit':
        break
    # Decode what you receive:
    line = line.decode('latin-1')

    # Work with Unicode internally:
    line = line.upper()

    # Encode what you send:
    line = line.encode('utf-8')
    sys.stdout.write(line)