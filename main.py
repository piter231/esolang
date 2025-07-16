import re
import sys

class RiverEsolangInterpreter:
    def __init__(self):
        self.currents = {}
        self.loop_stack = []
        self.depth = 0
        self.flow_log = []
        self.skip_mode = False
        self.skip_depth = 0
        self.in_true_branch = False
        self.execution_count = 0
        self.max_instructions = 10000
        self.functions = {}
        self.call_stack = []
        self.return_value = None
        
    def _parse_value(self, expr, local_vars=None):
        if local_vars is None:
            local_vars = {}
        expr = expr.strip()
        

        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        

        if re.match(r'^-?\d+$', expr):
            return int(expr)
            

        if expr in local_vars:
            return local_vars[expr]
        if expr in self.currents:
            return self.currents[expr]
        
        match = re.match(r'converge with (\w+) carrying (.*)$', expr)
        if match:
            func_name = match[1]
            arg_expr = match[2]
            arg_value = self._parse_value(arg_expr, local_vars)
            return self._call_function(func_name, arg_value)
        
        match = re.match(r'merge (.*) and (.*)$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        
        match = re.match(r'separate (.*) from (.*)$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            return right - left
        
        match = re.match(r'combine (.*) and (.*)$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            return left * right
        
        match = re.match(r'divide (.*) by (.*)$', expr)
        if match:
            divisor = self._parse_value(match[2], local_vars)
            if divisor == 0:
                self._log_flow("RIVER ERROR: Cannot divide by zero")
                return 0
            return self._parse_value(match[1], local_vars) // divisor
        
        match = re.match(r'remainder of (.*) divided by (.*)$', expr)
        if match:
            dividend = self._parse_value(match[1], local_vars)
            divisor = self._parse_value(match[2], local_vars)
            if divisor == 0:
                self._log_flow("RIVER ERROR: Modulo by zero")
                return 0
            return dividend % divisor
        
        match = re.match(r'does (.*) equal (.*)\?$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            return int(left == right)
        
        match = re.match(r'is (.*) equal to (.*)\?$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            return int(left == right)
        
        match = re.match(r'is (.*) deeper than (.*)\?$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            if isinstance(left, str) or isinstance(right, str):
                self._log_flow(f"RIVER ERROR: Cannot compare strings with 'deeper than': '{expr}'")
                return 0
            return int(left > right)
        
        match = re.match(r'is (.*) shallower than (.*)\?$', expr)
        if match:
            left = self._parse_value(match[1], local_vars)
            right = self._parse_value(match[2], local_vars)
            if isinstance(left, str) or isinstance(right, str):
                self._log_flow(f"RIVER ERROR: Cannot compare strings with 'shallower than': '{expr}'")
                return 0
            return int(left < right)
        
        self._log_flow(f"RIVER ERROR: Unknown expression '{expr}'")
        return 0

    def _call_function(self, func_name, arg_value):
        if func_name not in self.functions:
            self._log_flow(f"RIVER ERROR: Undefined tributary '{func_name}'")
            return 0
            
        prev_depth = self.depth
        self.depth = 0
        self.return_value = None
        
        call_context = {
            'func': func_name,
            'arg': arg_value,
            'local_vars': {'current': arg_value}
        }
        self.call_stack.append(call_context)
        local_vars = call_context['local_vars']
        
        self._log_flow(f"Calling tributary {func_name}({arg_value})")
        
        func_body = self.functions[func_name]['body']
        body_index = 0
        
        while body_index < len(func_body):
            line = func_body[body_index]
            self.execution_count += 1
            if self.execution_count > self.max_instructions:
                self._log_flow("RIVER ERROR: Execution limit exceeded in function")
                break
                
            self._log_flow(f"[Tributary {func_name}] {line}")
            
            if line.startswith('return to main river'):
                expr = line.split(':', 1)[1].strip()
                self.return_value = self._parse_value(expr, local_vars)
                self._log_flow(f"Returning {self.return_value} from {func_name}")
                break
                
            match = re.match(r'create stream (\w+) carrying (.+)$', line)
            if match:
                var, expr = match[1], match[2]
                local_vars[var] = self._parse_value(expr, local_vars)
                body_index += 1
                continue
                
            match = re.match(r'direct stream (\w+) to carry (.+)$', line)
            if match:
                var, expr = match[1], match[2]
                if var in local_vars:
                    local_vars[var] = self._parse_value(expr, local_vars)
                else:
                    self.currents[var] = self._parse_value(expr, local_vars)
                body_index += 1
                continue
                
            match = re.match(r'deposit sediment: (.+)$', line)
            if match:
                value = self._parse_value(match[1], local_vars)
                self._log_flow(f"Output: {value}")
                print(f"🌊 {value}")
                body_index += 1
                continue
                
            match = re.match(r'if waterfall (.+):$', line)
            if match:
                condition = match[1]
                result = self._parse_value(condition, local_vars)
                self._log_flow(f"Waterfall check: {condition} -> {'flows' if result else 'blocks'}")
                
                if result:
                    self.depth += 1
                    body_index += 1
                else:
                    depth = 1
                    body_index += 1
                    while body_index < len(func_body) and depth > 0:
                        if func_body[body_index].startswith("if waterfall") or func_body[body_index].startswith("flow until"):
                            depth += 1
                        elif func_body[body_index] == "end waterfall" or func_body[body_index] == "otherwise:":
                            depth -= 1
                        body_index += 1
                continue
                
            if line == "end waterfall":
                self.depth -= 1
                body_index += 1
                continue
                
            match = re.match(r'flow until (.+):$', line)
            if match:
                condition = match[1]
                cond_value = self._parse_value(condition, local_vars)
                self._log_flow(f"Loop condition: {condition} = {cond_value}")
                
                if cond_value:
                    depth = 1
                    body_index += 1
                    while body_index < len(func_body) and depth > 0:
                        if func_body[body_index].startswith("flow until"):
                            depth += 1
                        elif func_body[body_index] == "river bend":
                            depth -= 1
                        body_index += 1
                else:
                    call_context['loop_stack'] = body_index
                    body_index += 1
                continue
                
            if line == "river bend":
                if 'loop_stack' in call_context:
                    loop_start = call_context['loop_stack']
                    cond_line = func_body[loop_start]
                    cond_match = re.match(r'flow until (.+):$', cond_line)
                    if cond_match:
                        cond_expr = cond_match[1]
                        cond_value = self._parse_value(cond_expr, local_vars)
                        self._log_flow(f"Loop check: {cond_expr} = {cond_value}")
                        
                        if cond_value:
                            body_index += 1
                        else:
                            body_index = loop_start
                    else:
                        body_index += 1
                else:
                    body_index += 1
                continue
                
            body_index += 1
        
        self.depth = prev_depth
        return_value = self.return_value or 0
        self.call_stack.pop()
        
        self._log_flow(f"Tributary {func_name} returned {return_value}")
        return return_value

    def _log_flow(self, message):
        indent = "  " * self.depth
        self.flow_log.append(f"{indent}{message}")

    def _clean_line(self, line):
        """Remove comments and trim whitespace"""
        if '#' in line:
            line = line.split('#', 1)[0]
        return line.strip()
    
    def execute(self, code):
        self.currents = {}
        self.loop_stack = []
        self.depth = 0
        self.flow_log = []
        self.skip_mode = False
        self.skip_depth = 0
        self.in_true_branch = False
        self.execution_count = 0
        self.functions = {}
        self.call_stack = []
        self.return_value = None
        
        current_function = None
        function_body = []
        cleaned_lines = []
        
        for line in code.split('\n'):
            clean_line = self._clean_line(line)
            if not clean_line:
                continue
                
            match = re.match(r'tributary (\w+) flowing from current$', clean_line)
            if match:
                if current_function:
                    self.functions[current_function] = {'body': function_body}
                current_function = match[1]
                function_body = []
                continue
                
            if clean_line == "rejoin main river" and current_function:
                self.functions[current_function] = {'body': function_body}
                current_function = None
                function_body = []
                continue
                
            if current_function:
                function_body.append(clean_line)
            else:
                cleaned_lines.append(clean_line)
        
        i = 0
        self.execution_count = 0
        
        while i < len(cleaned_lines):
            self.execution_count += 1
            if self.execution_count > self.max_instructions:
                self._log_flow("RIVER ERROR: Execution limit exceeded (possible infinite loop)")
                break
                
            line = cleaned_lines[i]
            self._log_flow(f"[Line {i}] {line}")
            
            if self.skip_mode:
                if line == "end waterfall" and self.skip_depth == self.depth:
                    self.skip_mode = False
                    self.in_true_branch = False
                elif line == "otherwise:" and self.skip_depth == self.depth:
                    self.skip_mode = False
                i += 1
                continue
            
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
                
            # Function calls are handled in _parse_value
                
            match = re.match(r'if waterfall (.+):$', line)
            if match:
                condition = match[1]
                result = self._parse_value(condition)
                self._log_flow(f"Waterfall check: {condition} -> {'flows' if result else 'blocks'}")
                
                if result:
                    self.depth += 1
                    self.in_true_branch = True
                else:
                    self.skip_mode = True
                    self.skip_depth = self.depth
                i += 1
                continue
                
            if line == "otherwise:":
                if self.in_true_branch:
                    self.skip_mode = True
                    self.skip_depth = self.depth
                else:
                    self.depth += 1
                    self.in_true_branch = True
                i += 1
                continue
                
            if line == "end waterfall":
                self.depth -= 1
                self.in_true_branch = False
                i += 1
                continue
                
            match = re.match(r'flow until (.+):$', line)
            if match:
                condition = match[1]
                cond_value = self._parse_value(condition)
                self._log_flow(f"Loop condition: {condition} = {cond_value}")
                
                if cond_value:
                    self._log_flow(f"Loop condition met, skipping loop")
                    depth = 1
                    i += 1
                    while i < len(cleaned_lines) and depth > 0:
                        if cleaned_lines[i].startswith("flow until"):
                            depth += 1
                        elif cleaned_lines[i] == "river bend":
                            depth -= 1
                        i += 1
                    continue
                else:
                    if not self.loop_stack or i != self.loop_stack[-1]:
                        self.loop_stack.append(i)
                    self.depth += 1
                    i += 1
                continue
                
            if line == "river bend":
                self.depth -= 1
                if self.loop_stack:
                    loop_start = self.loop_stack[-1]
                    cond_line = cleaned_lines[loop_start]
                    cond_match = re.match(r'flow until (.+):$', cond_line)
                    if cond_match:
                        cond_expr = cond_match[1]
                        cond_value = self._parse_value(cond_expr)
                        self._log_flow(f"Loop check: {cond_expr} = {cond_value}")
                        
                        if cond_value:
                            self.loop_stack.pop()
                            self._log_flow("Loop condition met, exiting loop")
                            i += 1  
                        else:
                            i = loop_start
                            self._log_flow(f"Loop continues, jumping to line {i}")
                    else:
                        i += 1
                else:
                    i += 1
                continue
                

            match = re.match(r'create stream (\w+) carrying (.+)$', line)
            if match:
                var, expr = match[1], match[2]
                self.currents[var] = self._parse_value(expr)
                i += 1
                continue
                
            match = re.match(r'direct stream (\w+) to carry (.+)$', line)
            if match:
                var, expr = match[1], match[2]
                self.currents[var] = self._parse_value(expr)
                i += 1
                continue
                
            match = re.match(r'deposit sediment: (.+)$', line)
            if match:
                value = self._parse_value(match[1])
                self._log_flow(f"Output: {value}")
                print(f"🌊 {value}")
                i += 1
                continue
                
            i += 1

    def print_flow_log(self):
        print("\nRiver's Journey:\n" + "\n".join(self.flow_log))
        print(f"\nFinal Streams: {self.currents}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python river.py <filename.rv>")
        print("Example: python river.py program.rv")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not filename.endswith('.rv'):
        print("Error: River files should have .rv extension")
        sys.exit(1)
    
    try:
        with open(filename, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    interpreter = RiverEsolangInterpreter()
    interpreter.execute(code)
    
    # Uncomment to see detailed execution log
    # interpreter.print_flow_log()


if __name__ == "__main__":
    main()