# esolang: The River Programming Language

esolang is a creative programming language that uses river and water metaphors to represent programming concepts. Programs describe a river's journey from source to ocean.

## Core Concepts

### 1. Program Structure

```python
river begins its journey
  # Your code here
river meets ocean
```

### 2. Variables (Streams)

```python
create stream stones carrying 5        # Initialize variable
direct stream stones to carry 10       # Update variable
```

### 3. Arithmetic Operations

```python
merge stones and pebbles        # Addition (stones + pebbles)
separate pebbles from stones    # Subtraction (stones - pebbles)
combine stones and pebbles      # Multiplication
divide stones by pebbles        # Integer division
```

### 4. Comparisons

```python
does stones equal pebbles?      # Equality check
is stones deeper than pebbles?  # Greater than check
```

### 5. Conditionals (Waterfalls)

```python
if waterfall is stones deeper than pebbles?:
  # Code if true
otherwise:
  # Code if false
end waterfall
```

### 6. Loops (River Flows)

```python
flow until does stones equal 0?:
  # Loop body
  direct stream stones to carry separate 1 from stones  # stones -= 1
river bend
```

### 7. Input/Output

```python
receive rainfall into stream rain  # Input integer
deposit sediment: rain             # Print value
```

## Example Programs

### 1. Factorial Calculation

```python
river begins its journey
create stream n carrying 5
create stream result carrying 1

flow until does n equal 0?:
  direct stream result to carry combine result and n
  direct stream n to carry separate 1 from n
  deposit sediment: result
river bend

deposit sediment: result  # Output: 120
river meets ocean
```

### 2. Fibonacci Sequence

```python
river begins its journey
create stream a carrying 0
create stream b carrying 1
create stream count carrying 10

deposit sediment: a
deposit sediment: b

flow until is count deeper than 0?:
  create stream next carrying merge a and b
  deposit sediment: next
  direct stream a to carry b
  direct stream b to carry next
  direct stream count to carry separate 1 from count
river bend

river meets ocean
# Output: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

### 3. Interactive Number Guessing

```python
river begins its journey
create stream secret carrying 42
create stream guess carrying 0

flow until does guess equal secret?:
  receive rainfall into stream guess

  if waterfall is guess deeper than secret?:
    deposit sediment: "Too high!"
  otherwise:
    if waterfall is secret deeper than guess?:
      deposit sediment: "Too low!"
    end waterfall
  end waterfall
river bend

deposit sediment: "You found the secret!"
river meets ocean
```

## Running Programs

```python
if __name__ == "__main__":
    # Sample program
    esolang_code = """
    river begins its journey
    create stream n carrying 5
    create stream result carrying 1

    flow until does n equal 0?:
      direct stream result to carry combine result and n
      direct stream n to carry separate 1 from n
    river bend

    deposit sediment: result
    river meets ocean
    """

    interpreter = esolangInterpreter()
    interpreter.execute(esolang_code)
    interpreter.print_flow_log()
```

## Language Philosophy

esolang embodies the following principles:

1. **Natural Flow**: Code execution mimics a river's journey
2. **Organic Syntax**: Concepts use water-based metaphors
3. **Expressive Operations**: Math as natural water interactions
4. **Visual Execution**: Journey log shows program flow

The language is designed to make programming concepts more accessible through nature metaphors while maintaining practical functionality.
"""

if **name** == "**main**": # Check if documentation was requested
if len(sys.argv) > 1 and sys.argv[1] == "--docs":
print(get_documentation())
sys.exit(0)

    # Sample program: Calculate 5! (factorial)
    esolang_code = """
    river begins its journey
    create stream n carrying 5
    create stream result carrying 1

    flow until does n equal 0?:
      direct stream result to carry combine result and n
      direct stream n to carry separate 1 from n
      deposit sediment: result
    river bend

    deposit sediment: "Final result:"
    deposit sediment: result
    river meets ocean
    """

    interpreter = esolangInterpreter()
    interpreter.execute(esolang_code)
    interpreter.print_flow_log()

````

## Running the Interpreter

### To see documentation:
```bash
python esolang.py --docs
````

### To run the sample program:

```bash
python esolang.py
```

## Example Output

```
River's Journey:
[Flow] river begins its journey
[Flow] create stream n carrying 5
[Flow] create stream result carrying 1
[Flow] flow until does n equal 0?:
  Waterfall check: does n equal 0? -> 0
[Flow] direct stream result to carry combine result and n
[Flow] direct stream n to carry separate 1 from n
[Flow] deposit sediment: result
Output: 5
[Flow] river bend
[Flow] flow until does n equal 0?:
  Waterfall check: does n equal 0? -> 0
[Flow] direct stream result to carry combine result and n
[Flow] direct stream n to carry separate 1 from n
[Flow] deposit sediment: result
Output: 20
[Flow] river bend
[Flow] flow until does n equal 0?:
  Waterfall check: does n equal 0? -> 0
[Flow] direct stream result to carry combine result and n
[Flow] direct stream n to carry separate 1 from n
[Flow] deposit sediment: result
Output: 60
[Flow] river bend
[Flow] flow until does n equal 0?:
  Waterfall check: does n equal 0? -> 0
[Flow] direct stream result to carry combine result and n
[Flow] direct stream n to carry separate 1 from n
[Flow] deposit sediment: result
Output: 120
[Flow] river bend
[Flow] flow until does n equal 0?:
  Waterfall check: does n equal 0? -> 1
Loop condition met, skipping loop
[Flow] deposit sediment: "Final result:"
Output: Final result:
[Flow] deposit sediment: result
Output: 120
[Flow] river meets ocean

Final Streams: {'n': 0, 'result': 120}
```
