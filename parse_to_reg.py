import re

with open('block.txt', 'r') as f:
    text = f.read()

# Try to parse the multi-word pattern dispatch part
# It looks like:
# else if (cmd === 'look'  && args[0] === 'at')                         { gameExamine(args.slice(1)); }
# Let's extract them by splitting the text.

registry = "const VERB_REGISTRY = [\n"

# First, extract the "else if (...)" and "if (...)" lines
lines = text.split('\n')
for line in lines:
    line = line.strip()
    if line.startswith('//'):
        registry += f"  {line}\n"
        continue
        
    m = re.match(r'^(?:else\s+)?if\s*\((.*?)\)\s*\{\s*(.*?)\s*\}$', line)
    if m:
        cond = m.group(1).strip()
        body = m.group(2).strip()
        # Some blocks span multiple lines. We'll handle those manually.
        registry += f"  {{ test: (cmd, args, rest) => {cond}, exec: (cmd, args, rest) => {{ {body} }} }},\n"
    elif line == "else {" or line == "switch (cmd) {":
        pass
    elif line.startswith("case"):
        # We will handle switch separately
        pass

registry += "];\n"

with open('registry_out.txt', 'w') as f:
    f.write(registry)
