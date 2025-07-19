# River Programming Language Interpreter

## Overview

River is an esoteric programming language that models computation as the flow of water through a river system. The language uses concepts like streams, waterfalls, tributaries, and river bends to represent variables, conditionals, functions, and loops.

This interpreter allows you to run River programs and experience its unique approach to computation.

## Language Features

### Core Concepts

- **Streams**: Variables that carry values (like currents in a river)
- **Waterfalls**: Conditional statements (if/else)
- **Flow Until**: Looping constructs
- **Tributaries**: Functions that can be called from the main river
- **Sediment Deposit**: Output mechanism

### Data Types

- Integers (e.g., `5`, `-12`)
- Strings (e.g., `"hello"`, `"river"`)
- Booleans (represented as 1 for true, 0 for false)

## Syntax Reference

### Variables

```river
create stream speed carrying 5
direct stream depth to carry 12
```

### Output

```river
deposit sediment: "Hello, World!"
```

### Conditionals

```river
if waterfall depth equals 10:
    deposit sediment: "Depth is ten"
otherwise:
    deposit sediment: "Depth is not ten"
end waterfall
```

### Loops

```river
flow until count equals 5:
    deposit sediment: count
    direct stream count to carry merge count and 1
river bend
```

### Functions (Tributaries)

```river
tributary square flowing from current
    create stream result carrying combine current and current
    return to main river: result
rejoin main river

create stream num carrying 4
deposit sediment: converge with square carrying num
```

### Expressions

River supports complex expressions:

```river
create stream result carrying merge 5 and 3                   # 5 - 3 = 2
create stream combined carrying combine "river" and "flow"     # "riverflow"
create stream check carrying is 5 deeper than 3?               # 1 (true)
```

## Getting Started

### Requirements

- Python 3.6 or higher

### Installation

1. Clone this repository:

```bash
git clone https://github.com/piter231/esolang.git
cd esolang
```

2. Run a River program:

```bash
python main.py main.rv
```

# uncomment the line 470 in main.py in order to make logs visible

## Execution Details

### Runtime Behavior

- Programs start with `river begins its journey`
- Programs end with `river meets ocean`
- Maximum of 10,000 instructions executed (prevents infinite loops)
- Detailed execution log available (uncomment in code)

### Error Handling

The interpreter provides meaningful error messages:

```
RIVER ERROR: Cannot divide by zero
RIVER ERROR: Undefined tributary 'calculate'
RIVER ERROR: Execution limit exceeded
```

## Development

### Extending the Language

The interpreter is structured to allow easy addition of:

1. New expression types
2. Additional native functions
3. Enhanced error reporting
4. Additional control flow structures

## License

This project is licensed under the MIT License.

## Inspiration

River was inspired by the beauty and complexity of natural river systems. Its design encourages programmers to think about computation as a natural, flowing process rather than a rigid sequence of operations.

---

**Flow with the current!** 🌊
