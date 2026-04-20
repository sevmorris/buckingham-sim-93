import re

path = '/Users/sev/Projects/FloppyLetters/FloppyLetter2601/engine.js'
with open(path, 'r') as f:
    text = f.read()

start_marker = "  // ── Multi-word pattern dispatch ──────────────────────────────────────────\n"
end_marker = "  // Nudge to eject once after reading, on the next non-eject command"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found.")
    exit(1)

block = text[start_idx:end_idx]

# Let's write block to a file so we can parse it easily
with open('block.txt', 'w') as f:
    f.write(block)
