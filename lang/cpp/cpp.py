from talon import Context, Module, actions, settings, resource, fs
from typing import Tuple, Dict
import os
import json
import pathlib
import sqlite3

##
## Configuration.
##
json_namespace_table = {}
json_codeword_table = {}

taxonomy_path = pathlib.Path(__file__).parent / 'taxonomy'

## Load namespaces from JSON file.
def load_json(path):
    loaded_namespaces = []
    with resource.open(str(pathlib.Path('taxonomy') / path), 'r') as f:
        j = json.load(f)
        for ns in j:
            ns['joiner'] = ns.get('joiner', '::')
            json_namespace_table[ns['namespace']] = ns
            json_codeword_table[ns['codeword']] = ns
            loaded_namespaces.append(ns)
    return loaded_namespaces

json_files = os.listdir(taxonomy_path)

for f in json_files:
    if not f.endswith(".json"):
        continue
    load_json(f)


##
# Implementation.
##

mod = Module()
ctx = Context()

ctx.lists["self.cpp_integral"] = {
    "char": "char",
    "byte": "int8_t",
    "short": "int16_t",
    "integer": "int32_t",
    "long": "int64_t",
    "float": "float",
    "double": "double",
    "size type": "std::size_t",

    "you byte": "uint8_t",
    "you short": "uint16_t",
    "you long": "uint64_t",
    "you integer": "uint32_t",

    "auto": "auto",
    "boolean": "bool",
    "void": "void",
}

ctx.lists["self.cpp_modifiers"] = {
    "constant": "const",
    "inline": "inline",
    "volatile": "volatile",
    "virtual": "virtual",
    "static": "static"
}

# Extract the raw codeword -> namespace map.
def extract_codeword_namespace():
    list_rule = {}
    for word in json_codeword_table:
        list_rule[word] = json_codeword_table[word]['namespace']
    return list_rule

ctx.lists["self.cpp_known_namespaces"] = extract_codeword_namespace()
mod.list("cpp_known_namespaces", desc = "Known C++ namespaces.")

# Get the list name for the given namespace name.
def namespace_list_symbol(namespace_name, suffix = "types", prefix_self = False):
    return ("self." if prefix_self else "") + "cpp_{}_{}".format(namespace_name, suffix)

# Construct an or-separated rule to capture each list of types.
def construct_types_rule(suffix = "types"):
    mapped = map(lambda ns: "{} {{{}}}".format(ns['codeword'], namespace_list_symbol(ns['namespace'], suffix=suffix, prefix_self=True)), json_codeword_table.values())
    rule = " | ".join(mapped)
    return rule

# Add a list from a particular namespace
def add_namespace_list(ns, json_key, list_suffix):
    sym = namespace_list_symbol(ns['namespace'], suffix=list_suffix, prefix_self = False)
    
    list_to_add = {}
    try:
        list_to_add = ns[json_key]
    except KeyError:
        pass

    for k in list_to_add.keys():
        list_to_add[k] = ns['joiner'].join((ns['namespace'], list_to_add[k]))

    ctx.lists["self." + sym] = list_to_add
    mod.list(sym, desc="C++ types in the {} namespace.".format(ns['namespace']))

##
# Startup
##

# Add all the known lists for all the loaded namespaces
for ns in json_codeword_table.values():
    add_namespace_list(ns, 'names', 'types')
    add_namespace_list(ns, 'templates', 'templates')

# Set up watch for new files
# TODO this doesn't actually redefine the grammar, so it doesn't really work without forcing a reload some other way.
def on_json_change(path, exists):
    newfile = pathlib.Path(path).relative_to(taxonomy_path)
    if newfile.exists():
        loaded_namespaces = load_json(newfile)

fs.watch(str(taxonomy_path), on_json_change)


##
# Module/Context declarations
##

@mod.capture
def cpp_known_namespaces(m) -> Dict:
    "Returns a JSON dict of the namespace."

@ctx.capture('self.cpp_known_namespaces', rule="{self.cpp_known_namespaces}")
def cpp_known_namespaces(m) -> Dict:
    return json_namespace_table[m[0]]

@mod.capture
def cpp_namespaced_type(m) -> str:
    "Returns a namespaced concrete type."

@ctx.capture('self.cpp_namespaced_type', rule=construct_types_rule())
def cpp_namespaced_type(m) -> str:
    return m[-1]

@mod.capture
def cpp_namespaced_template(m) -> str:
    "Returns a namespaced template type."

@ctx.capture('self.cpp_namespaced_template', rule=construct_types_rule("templates"))
def cpp_namespaced_template(m) -> str:
    return m[-1]

mod.list("cpp_integral", desc="C++ integral types.")
mod.list("cpp_modifiers", desc="C++ modifiers.")

@mod.capture
def cpp_integral(m) -> str:
    "Returns an integral type."

@ctx.capture('self.cpp_integral', rule="{self.cpp_integral}")
def cpp_integral(m) -> str:
    return m.cpp_integral

@mod.capture
def cpp_modifiers(m) -> str:
    "Returns a C++ modifier."

@ctx.capture('self.cpp_modifiers', rule = "{self.cpp_modifiers}+")
def cpp_modifiers(m) -> str:
    return " ".join(m.cpp_modifiers_list)


@mod.action_class
class Actions:
    def cpp_namespace_with_joiner(ns: Dict) -> str:
        """Returns a namespace and its joiner, e.g. 'std::' """
        return ns['namespace'] + ns['joiner']
    def cpp_naked_namespace(ns: Dict) -> str:
        """Gets only the namespace part of a namespace."""
        return ns['namespace']
    pass

