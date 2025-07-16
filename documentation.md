# River Language: The Complete Documentation

River is a poetic, flow-inspired programming language that models computation as a river's journey. This documentation combines all key concepts with optimized examples.

## Core Concepts

- **Streams**: Variables that carry values
- **Waterfalls**: Conditional statements
- **River Bends**: Looping constructs
- **Tributaries**: Functions
- **Sediment**: Program output

## Best Practices

1. **Use temporary variables** for intermediate results
2. **Break complex expressions** into multiple steps
3. **Compute values before** using them in output
4. **Initialize variables** before use
5. **Reset variables** when reusing them

## Basic Syntax

### Program Structure

```river
river begins its journey
  # Main program
river meets ocean
```

### Variables (Streams)

```river
create stream name carrying 5          # Integer
create stream message carrying "Hello" # String
direct stream name to carry 10         # Update variable
```

### Arithmetic Operations

```river
merge a and b       # Addition (a + b)
separate a from b   # Subtraction (b - a)
combine a and b     # Multiplication (a * b)
divide a by b       # Integer division (a // b)
remainder of a divided by b  # Modulo (a % b)
```

### Comparisons

```river
does a equal b?          # Equality (a == b)
is a deeper than b?      # Greater than (a > b)
is a shallower than b?   # Less than (a < b)
```

## Comprehensive Examples

### 1. Counting from 0 to 10

```river
river begins its journey
  create stream counter carrying 0

  flow until is counter deeper than 10?:
    deposit sediment: counter
    direct stream counter to carry merge counter and 1
  river bend
river meets ocean
```

**Output:**

```
🌊 0
🌊 1
🌊 2
🌊 3
🌊 4
🌊 5
🌊 6
🌊 7
🌊 8
🌊 9
🌊 10
```

### 2. Basic Arithmetic

```river
river begins its journey
  create stream a carrying 10
  create stream b carrying 3

  # Compute each operation separately
  create stream sum carrying merge a and b
  create stream diff carrying separate b from a
  create stream prod carrying combine a and b
  create stream quot carrying divide a by b
  create stream rem carrying remainder of a divided by b

  deposit sediment: merge "Sum: " and sum
  deposit sediment: merge "Difference: " and diff
  deposit sediment: merge "Product: " and prod
  deposit sediment: merge "Quotient: " and quot
  deposit sediment: merge "Remainder: " and rem
river meets ocean
```

**Output:**

```
🌊 Sum: 13
🌊 Difference: 7
🌊 Product: 30
🌊 Quotient: 3
🌊 Remainder: 1
```

### 3. String Manipulation

```river
river begins its journey
  create stream greeting carrying "Hello"
  create stream name carrying "River"
  create stream message carrying merge greeting and ", "
  direct stream message to carry merge message and name
  direct stream message to carry merge message and "!"

  deposit sediment: message
river meets ocean
```

**Output:**

```
🌊 Hello, River!
```

### 4. Fibonacci Sequence

```river
river begins its journey
  create stream n carrying 10
  create stream a carrying 0
  create stream b carrying 1
  create stream count carrying 0

  deposit sediment: "Fibonacci sequence:"

  flow until is count equal to n?:
    deposit sediment: a
    create stream next carrying merge a and b
    direct stream a to carry b
    direct stream b to carry next
    direct stream count to carry merge count and 1
  river bend
river meets ocean
```

**Output:**

```
🌊 Fibonacci sequence:
🌊 0
🌊 1
🌊 1
🌊 2
🌊 3
🌊 5
🌊 8
🌊 13
🌊 21
🌊 34
```

### 5. Prime Numbers & Factorial

```river
river begins its journey
  # Prime Number Generator
  create stream current carrying 2
  create stream limit carrying 20
  deposit sediment: "Prime numbers:"

  flow until is current deeper than limit?:
    create stream is_prime carrying 1
    create stream divisor carrying 2
    create stream max_divisor carrying separate 1 from current

    flow until is divisor deeper than max_divisor?:
      create stream rem carrying remainder of current divided by divisor
      if waterfall does rem equal 0?:
        direct stream is_prime to carry 0
      end waterfall
      direct stream divisor to carry merge divisor and 1
    river bend

    if waterfall does is_prime equal 1?:
      deposit sediment: current
    end waterfall

    direct stream current to carry merge current and 1
  river bend

  # Factorial Calculator
  tributary factorial flowing from current
    if waterfall is current shallower than 2?:
      return to main river: 1
    otherwise:
      create stream prev carrying separate 1 from current
      create stream rec carrying converge with factorial carrying prev
      create stream result carrying combine current and rec
      return to main river: result
    end waterfall
  rejoin main river

  create stream number carrying 5
  create stream result carrying converge with factorial carrying number
  deposit sediment: merge "Factorial of " and number
  deposit sediment: merge " is " and result
river meets ocean
```

**Output:**

```
🌊 Prime numbers:
🌊 2
🌊 3
🌊 5
🌊 7
🌊 11
🌊 13
🌊 17
🌊 19
🌊 Factorial of 5
🌊 is 120
```

### 6. FizzBuzz

```river
river begins its journey
  create stream current carrying 1
  create stream limit carrying 15

  deposit sediment: "FizzBuzz:"

  flow until is current deeper than limit?:
    create stream out carrying ""
    create stream rem3 carrying remainder of current divided by 3
    create stream rem5 carrying remainder of current divided by 5

    if waterfall does rem3 equal 0?:
      direct stream out to carry merge out and "Fizz"
    end waterfall

    if waterfall does rem5 equal 0?:
      direct stream out to carry merge out and "Buzz"
    end waterfall

    if waterfall does out equal ""?:
      deposit sediment: current
    otherwise:
      deposit sediment: out
    end waterfall

    direct stream current to carry merge current and 1
  river bend
river meets ocean
```

**Output:**

```
🌊 FizzBuzz:
🌊 1
🌊 2
🌊 Fizz
🌊 4
🌊 Buzz
🌊 Fizz
🌊 7
🌊 8
🌊 Fizz
🌊 Buzz
🌊 11
🌊 Fizz
🌊 13
🌊 14
🌊 FizzBuzz
```

### 7. Temperature Conversion Function

```river
river begins its journey
  tributary celsius_to_fahrenheit flowing from current
    create stream f carrying combine current and 9
    direct stream f to carry divide f by 5
    direct stream f to carry merge f and 32
    return to main river: f
  rejoin main river

  create stream celsius carrying 25
  create stream fahrenheit carrying converge with celsius_to_fahrenheit carrying celsius

  deposit sediment: merge celsius and "°C is "
  deposit sediment: merge fahrenheit and "°F"
river meets ocean
```

**Output:**

```
🌊 25°C is
🌊 77°F
```

## Language Features & Limitations

### Key Features:

- Natural language-inspired syntax
- Strong river-themed metaphors
- Function support with tributaries
- Recursive capabilities
- String and integer manipulation
- Modular program structure

### Current Limitations:

- **No nested expressions**: Break complex expressions into steps
- **Integer math only**: No floating-point support
- **No arrays**: Single-value streams only
- **No input**: Programs can't accept runtime input
- **Case-sensitive**: Variable names are case-sensitive

## Execution Rules

1. **Stream Creation Order**: Variables must be created before use
2. **Loop Initialization**: Initialize counters before loops
3. **Variable Scope**: All streams are global by default
4. **Function Parameters**: Passed through 'current' variable
5. **Error Handling**: Fails gracefully with descriptive errors
