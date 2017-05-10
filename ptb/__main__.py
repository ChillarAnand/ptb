import os
import sys
import ptb

ptb.enable()

# Check that a script was passed in.
if len(sys.argv) <= 1:
    raise SystemExit("Usage: python -m ptb my_script.py")

# Check that the script exists.
script_path = sys.argv[1]
if not os.path.exists(script_path):
    raise SystemExit("Error: '%s' does not exist" % script_path)

# Replace ptb's dir with script's dir in the module search path.
sys.path[0] = os.path.dirname(script_path)

# Remove ptb from the arg list.
del sys.argv[0]

with open(script_path) as script_file:
    code = compile(script_file.read(), script_path, 'exec')
    variables = {}
    exec(code, variables, variables)

