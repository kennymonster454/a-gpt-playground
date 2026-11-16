#!/usr/bin/env python3
"""GoblinScript: a tiny, playful programming language."""
import ast, random, re, sys, time

class GoblinError(Exception): pass

def value(expr, env):
    try: tree = ast.parse(expr, mode="eval").body
    except SyntaxError: raise GoblinError(f"That expression makes no sense: {expr}")
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float, str, bool)): return n.value
        if isinstance(n, ast.Name):
            if n.id not in env: raise GoblinError(f"Unknown goblin: {n.id}")
            return env[n.id]
        if isinstance(n, ast.BinOp) and type(n.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod):
            a,b=ev(n.left),ev(n.right)
            return {ast.Add:lambda:a+b,ast.Sub:lambda:a-b,ast.Mult:lambda:a*b,ast.Div:lambda:a/b,ast.Mod:lambda:a%b}[type(n.op)]()
        if isinstance(n, ast.UnaryOp) and type(n.op) in (ast.USub, ast.UAdd, ast.Not):
            x=ev(n.operand); return -x if isinstance(n.op,ast.USub) else (+x if isinstance(n.op,ast.UAdd) else not x)
        if isinstance(n, ast.Compare) and len(n.ops)==1:
            a,b=ev(n.left),ev(n.comparators[0]); op=type(n.ops[0])
            funcs={ast.Eq:lambda:a==b,ast.NotEq:lambda:a!=b,ast.Gt:lambda:a>b,ast.GtE:lambda:a>=b,ast.Lt:lambda:a<b,ast.LtE:lambda:a<=b}
            if op in funcs:return funcs[op]()
        if isinstance(n, ast.BoolOp):
            vals=[bool(ev(x)) for x in n.values]; return all(vals) if isinstance(n.op,ast.And) else any(vals)
        raise GoblinError("That expression uses a spell GoblinScript doesn't know yet.")
    return ev(tree)

def blocks(lines, start):
    depth=0; alt=None
    for i in range(start+1,len(lines)):
        s=lines[i].strip()
        if s.startswith(("repeat ","if ")): depth+=1
        elif s=="end":
            if depth==0:return i,alt
            depth-=1
        elif s=="else" and depth==0:alt=i
    raise GoblinError(f"Missing 'end' for line {start+1}")

def execute(source, env=None, depth=0):
    if depth>20: raise GoblinError("Too many nested spells.")
    env=env if env is not None else {}
    lines=source.splitlines(); i=0
    while i<len(lines):
        raw=lines[i]; s=raw.strip(); i+=1
        if not s or s.startswith("#"): continue
        if s=="end" or s=="else": raise GoblinError(f"Unexpected {s!r} on line {i}.")
        if s.startswith("repeat ") or s.startswith("if "):
            stop,alt=blocks(lines,i-1)
            body="\n".join(lines[i:alt if alt is not None else stop])
            if s.startswith("repeat "):
                count=int(value(s[7:],env))
                if not 0<=count<=1000: raise GoblinError("Repeat count must be from 0 to 1000.")
                for _ in range(count): execute(body,env,depth+1)
            else:
                chosen=body if value(s[3:],env) else ("\n".join(lines[alt+1:stop]) if alt is not None else "")
                execute(chosen,env,depth+1)
            i=stop+1; continue
        if s.startswith("say "):
            expr=s[4:].strip()
            try: out=value(expr,env)
            except GoblinError:
                if expr.startswith('"') and expr.endswith('"'): out=expr[1:-1]
                else: raise
            print(out)
        elif s.startswith("set "):
            m=re.fullmatch(r"set\s+([A-Za-z_]\w*)\s*=\s*(.+)",s)
            if not m: raise GoblinError("Use: set name = expression")
            env[m[1]]=value(m[2],env)
        elif s.startswith("add ") or s.startswith("take "):
            m=re.fullmatch(r"(add|take)\s+([A-Za-z_]\w*)\s+(.+)",s)
            if not m or m[2] not in env: raise GoblinError("Use add/take with an existing variable.")
            n=value(m[3],env); env[m[2]]=env[m[2]]+n if m[1]=="add" else env[m[2]]-n
        elif s.startswith("roll "):
            n=int(value(s[5:],env))
            if not 1<=n<=1000000: raise GoblinError("Roll size must be 1 to 1,000,000.")
            print("🎲",random.randint(1,n))
        elif s=="flip": print(random.choice(["HEADS","TAILS"]))
        elif s=="show": print("GOBLIN VARIABLES:",env)
        elif s=="wait":
            time.sleep(0.2)
        elif s=="help": print("say | set | add | take | repeat/end | if/else/end | roll | flip | show")
        else: raise GoblinError(f"Unknown command on line {i}: {s}")

def main():
    if len(sys.argv)<2:
        print("GoblinScript 🧌\nUsage: python goblin.py examples/hello.gob")
        return
    try:
        with open(sys.argv[1],encoding="utf-8") as f: execute(f.read())
    except (GoblinError,ValueError,TypeError,ZeroDivisionError) as e:
        print(f"GOBLIN ERROR: {e}",file=sys.stderr); sys.exit(1)
    except FileNotFoundError: print("Goblin can't find that file.",file=sys.stderr); sys.exit(1)
if __name__=="__main__": main()
