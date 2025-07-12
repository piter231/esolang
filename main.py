import re
import sys

class esolangInterpreter:
    def __init__(self):
        self.currents = {}  # Variables
        self.loop_stack = []  # Loop positions
        self.depth = 0  # Block depth
        self.flow_log = []  # Execution trace
        self.skip_mode = False  # For skipping blocks
        self.skip_depth = 0
        
    def _parse_value(self, expr):
        """Recursively evaluate expressions"""
        expr = expr.strip()
        
        # Numeric constants
        if re.match(r'^\d+$', expr):
            return int(expr)
            
        # Variables
        if expr in self.currents:
            return self.currents[expr]
        
        # Handle complex expressions
        # Addition: merge A and B
        match = re.match(r'merge (.*) and (.*)$', expr)
        if match:
            left = self._parse_value(match[1])
            right = self._parse_value(match[2])
            return left + right
        
        # Subtraction: separate A from B
        match = re.match(r'separate (.*) from (.*)$', expr)
        if match:
            left = self._parse_value(match[1])
            right = self._parse_value(match[2])
            return right - left
        
        # Multiplication: combine A and B
        match = re.match(r'combine (.*) and (.*)$', expr)
        if match:
            left = self._parse_value(match[1])
            right = self._parse_value(match[2])
            return left * right
        
        # Division: divide A by B
        match = re.match(r'divide (.*) by (.*)$', expr)
        if match:
            left = self._parse_value(match[1])
            right = self._parse_value(match[2])
            if right == 0:
                self._log_flow("RIVER ERROR: Division by zero forbidden")
                return 0
            return left // right
        
        # Equality: does A equal B?
        match = re.match(r'does (.*) equal (.*)\?$', expr)
        if match:
            left = self._parse_value(match[1])
            right = self._parse_value(match[2])
            return int(left == right)
        
        # Greater than: is A deeper than B?
        match = re.match(r'is (.*) deeper than (.*)\?$', expr)
        if match:
            left = self._parse_value(match[1])
            right = self._parse_value(match[2])
            return int(left > right)
        
        self._log_flow(f"RIVER ERROR: Unknown expression '{expr}'")
        return 0

    def _log_flow(self, message):
        """Record execution trace"""
        indent = "  " * self.depth
        self.flow_log.append(f"{indent}{message}")

    def execute(self, code):
        """Execute esolang code"""
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        i = 0
        
        while i < len(lines):
            line = lines[i]
            self._log_flow(f"[Flow] {line}")
            
            # Skip mode handling
            if self.skip_mode:
                if line == "end waterfall" and self.skip_depth == self.depth:
                    self.skip_mode = False
                i += 1
                continue
            
            # Program structure
            if line == "river begins its journey":
                self.depth += 1
                i += 1
                continue
                
            if line == "river meets ocean":
                self.depth -= 1
                if self.depth == 0:
                    break
                i += 1
                continue
                
            # Variable declaration
            match = re.match(r'create stream (\w+) carrying (.*)$', line)
            if match:
                var, expr = match[1], match[2]
                self.currents[var] = self._parse_value(expr)
                i += 1
                continue
                
            # Variable assignment
            match = re.match(r'direct stream (\w+) to carry (.*)$', line)
            if match:
                var, expr = match[1], match[2]
                self.currents[var] = self._parse_value(expr)
                i += 1
                continue
                
            # Conditional statement
            match = re.match(r'if waterfall (.*):$', line)
            if match:
                condition = match[1]
                result = self._parse_value(condition)
                self._log_flow(f"Waterfall check: {condition} -> {'flows' if result else 'blocks'}")
                
                if not result:
                    self.skip_mode = True
                    self.skip_depth = self.depth
                else:
                    self.depth += 1
                i += 1
                continue
                
            # Else statement
            if line == "otherwise:":
                self.skip_mode = True
                self.skip_depth = self.depth
                i += 1
                continue
                
            # End conditional
            if line == "end waterfall":
                self.depth -= 1
                i += 1
                continue
                
            # Loop construct
            match = re.match(r'flow until (.*):$', line)
            if match:
                condition = match[1]
                if self._parse_value(condition):
                    # Skip loop if condition is true
                    self._log_flow(f"Loop condition met, skipping loop")
                    depth = 1
                    i += 1
                    while i < len(lines) and depth > 0:
                        if lines[i].startswith("flow until"):
                            depth += 1
                        elif lines[i] == "river bend":
                            depth -= 1
                        i += 1
                    continue
                else:
                    self.loop_stack.append(i)
                    self.depth += 1
                    i += 1
                continue
                
            # End loop
            if line == "river bend":
                self.depth -= 1
                if self.loop_stack:
                    loop_start = self.loop_stack.pop()
                    # Check if we should continue looping
                    cond_line = lines[loop_start]
                    cond_match = re.match(r'flow until (.*):$', cond_line)
                    if cond_match:
                        # Continue if condition is STILL FALSE
                        if not self._parse_value(cond_match[1]):
                            self.loop_stack.append(loop_start)
                            i = loop_start
                        else:
                            self._log_flow("Loop condition met, exiting loop")
                    else:
                        i += 1
                else:
                    i += 1
                continue
                
            # Output statement
            match = re.match(r'deposit sediment: (.*)$', line)
            if match:
                value = self._parse_value(match[1])
                self._log_flow(f"Output: {value}")
                i += 1
                continue
                
            # Input statement
            match = re.match(r'receive rainfall into stream (\w+)$', line)
            if match:
                var = match[1]
                try:
                    value = int(input("🌧️  Rainfall: "))
                    self.currents[var] = value
                except ValueError:
                    self._log_flow("RIVER WARNING: Numbers only please")
                i += 1
                continue
                
            i += 1

    def print_flow_log(self):
        """Print execution trace"""
        print("\nRiver's Journey:\n" + "\n".join(self.flow_log))
        print(f"\nFinal Streams: {self.currents}")

# Fixed factorial program
esolang_code = """
river begins its journey
create stream n carrying 5
create stream result carrying 1
create stream temp carrying 0

flow until does n equal 0?:
    direct stream temp to carry combine result and n
    direct stream result to carry temp
    direct stream n to carry separate 1 from n
    deposit sediment: result
river bend

deposit sediment: result
river meets ocean
"""

if __name__ == "__main__":
    interpreter = esolangInterpreter()
    interpreter.execute(esolang_code)
    interpreter.print_flow_log()

