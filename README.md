# spamoji

A programming language that only uses emojis as syntax and encourages writing spaghetti code.

## Example

```spamoji
🗒️ A function to calculate factorial
⚙️ 🔢❕🫸🔰🫷
    👋 🏁 🫴 1
    🔃 🔰 🤜 1
        🏁 🫴 🏁 ✖️ 🔰
        🔰 🫴 🔰 ➖ 1
    ↩️ 🏁

💭🫸🔤Enter a number to calculate the factorial: 🔤🫷
👋 😀 🫴 🔢🫸⌨️❗🫷
🤔 😀 🟰 ⚠️
👍
    💬🫸🔤Invalid input.🔤🫷
👎
    💬🫸🔤The factorial of 🔤😀🔤 is 🔤🔢❕🫸😀🫷🫷
```

## What's this all about?

This language is a learning project. Since it lacks many features of a typical programming language, it is not recommended for production use. If this experiment is successful, I might move on and begin working on Esore, a more serious language I've been designing in the past 2 years.

## Installation

To install the spamoji interpreter, you will need to have Python 3.10 or higher installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/).

Once you have Python installed, you can install the spamoji interpreter using pip:

```bash
pip install spamoji
```

## Usage

To run a spamoji program, you will need to use the spamoji interpreter.

You can provide a spamoji file (with the .🍝 extension) as input to run it. For example:

```bash
spamoji my_program.🍝
```

If no file is supplied, the interactive REPL will start, which allows to enter and evaluate expressions directly.

If the above command doesn't work, you can also run the interpreter using Python's -m flag:

```bash
python -m spamoji my_program.🍝
```

## Syntax

> [!IMPORTANT]
> The emojis used in the syntax were entered on a Windows machine. While they should work on other platforms, some emojis might not render correctly or might be replaced with different emojis. If you encounter any issues, please try copying and pasting the emojis from this documentation into your code.

### Statements

Each line of code starts with an emoji that indicates the type of statement. Each statement is followed by the relevant information, separated by spaces. Statements include:

- 🗒️ Comment: Text in this line will be ignored
- 👋 Variable declaration: Followed by the variable assignment
- 🤔 If statement: Followed by the condition
  - 👍 If true block
  - 👎 Else block
- 🔃 Loop: Followed by the loop variable and condition
  - ⛔ Break statement: Used to exit the loop
  - ⤴️ Continue statement: Used to skip to the next iteration of the loop
- ⚙️ Function definition: Followed by the function name and parameters
  - ↩️ Return statement: Followed by the value to return
- 📜 Class definition: Followed by the class name and members
- 🧩 Import statement: Followed by a file name, it gets replaced by the contents of that file before execution

Statements starting with any other character are going to be considered as expressions and be evaluated directly.

Some statements can be nested, such as if statements and loops. Indentation is used to indicate the scope of these statements. Indented blocks are considered part of the previous statement until the indentation level decreases.

### Expressions

An expression is a piece of code that produces a value and/or executes actions. Function calls, variables, and operations are all expressions and can be used on their own or inside of other expressions or statements.

🫸 and 🫷 can be used to group expressions and control the order of evaluation.

### Operators

The language supports basic operators for logical and arithmetic operations. These can be used between two values to perform calculations.

- ➕: Addition
- ➖: Subtraction or negation
- ✖️: Multiplication
- ➗: Division
- 🟰: Equal
- 🆚: Not equal
- 🤜: Greater than
- 🤛: Less than
- 🤝: Logical AND
- 🤲: Logical OR
- 🙅: Logical NOT

### Strings

Strings are sequences of characters enclosed in 🔤 on each side. They can contain any characters, including emojis. Strings can be used in variable assignments, printed to the console, and concatenated using the ➕ operator.

Values directly before or after a string will also be concatenated with that string:

```spamoji
🔤Hello 🔤0🔤 world🔤  🗒️ -> Hello 0 world
```

### Conditions

The 🤔 statement allows to run different code depending on a certain condition:

```spamoji
🤔 condition
👍
    this line runs if condition is true
👎
    this line runs if condition is false
```

Both the 👍 and 👎 branches are optional. If a branch has only 1 statement, it can be written in the same line as the 👍/👎. Conditions can also be nested inside of other conditions:

```spamoji
🤔 condition 1
👍
    this line runs if condition 1 is true
👎 🤔 condition 2
    👍 this line runs if condition 1 is false and condition 2 is true
```

Conditions can also be used inside of other expressions:

```spamoji
🫸🤔 condition 👍 a 👎 b 🫷
```

Here, if condition is true, `a` will be returned, otherwise `b`. It is important to note that inline conditions like this require both a 👍 and a 👎, otherwise an error will be raised.

### Loops

The 🔃 statement can be used to run code repeatedly while a certain condition is true.

```spamoji
🔃 condition
    this code runs while condition is true
```

Additionally, the ⛔ and ⤴️ statements can be used to control the loop execution. ⛔ stops the loop immediately, regardless of the condition. ⤴️ jumps back to the beginning of the loop.

### Variables

Variables are declared using the 👋 emoji, followed by the variable assignment expression. An assignment expression starts with the variable name, followed by 🫴 and a value. For example:

```spamoji
👋 x 🫴 1
```

The declaration and assignment can also be on separate lines. Any unassigned variables will start with value 🫥.

Variable names can be any combination of letters, numbers, and emojis, but must start with a letter or emoji and cannot contain [statement characters](#statements).

Variables declared inside of a block are only accessible inside of that block and any nested blocks.

### Functions

Functions are defined using the ⚙️ emoji, followed by the function name and parameters. The function body is indented and can contain any valid statements. The function can return a value using the ↩️ emoji.

Functions can be called by using their name followed by the arguments, separated by 🔸, between 🫸 and 🫷. Functions with no arguments can also be called with the ❗ emoji.

Here's an example of a function definition and call:

```spamoji
⚙️ greetAndAsk 🫸firstName 🔸 lastName🫷
    💬🫸🔤Hello, 🔤firstName🔤 🔤lastName🔤! Please enter a number...🔤🫷
    ↩️ ⌨️❗  🗒️ Return the user input

👋 x 🫴 greetAndAsk🫸🔤John🔤🔸🔤Doe🔤🫷
💬🫸🔤You entered: 🔤 x🫷
```

### Classes

Classes are defined using the 📜 emoji. The class body is indented and can contain any valid statements. Any function statements directly in the class body will be added to the class as methods.

Class instances are created by calling the class name, like a function. When an instance is created, the special method ✨ will be called.

Inside of methods, the 🤖 emoji can be used to refer to the current instance.

```spamoji
📜 MyClass
    ⚙️ ✨🫸name🫷
        🤖👉name 🫴 name

    ⚙️ greet❗
        💬🫸🔤Hello, I am 🔤🫸🤖👉name🫷🔤!🔤🫷
```

Classes can inherit methods from other classes (superclasses). Superclass names can be written between 🫸 and 🫷, separated by 🔸, after the class name in the definition. The first superclass can be accessed with the 👆 emoji in methods.

```spamoji
📜 MyClass 🫸superclass1🔸superclass2🫷
    ⚙️ superclassName❗
        ↩️ 👆👉name
```

### Imports

The 🧩 emoji can be used to include code from another file in the current code:

```spamoji
🧩 robots
👋 bot 🫴 Robot🫸name🫷
```

## Built-ins

The language includes several built-in functions and values for common operations.

### Built-in functions

- 💬🫸string🫷: Print string to a new line in the console
- 💭🫸string🫷: Print string to the console without creating a new line
- ⌨️❗: Get user input from the console
- ⏳🫸time🫷: Wait for a specified number of seconds
- 🔢🫸value🫷: Convert value to a number, return ⚠️ if the conversion fails
- 🎲🫸min🔸max🫷: Get a random integer from min to max
- 🕰️❗: Get time since epoch in seconds
- 🛑❗: Stop the program

### Built-in values

- ✅: true
- ❌: false
- 🫥: unassigned/null/no value
- ⚠️: error/invalid value

### Python interoperability

The 🐍 function allows to directly evaluate Python expressions within Spamoji code. The results of these evaluations can be stored in variables and used in Spamoji. For example, the following code prints the modulo of `x` and `y`:

```spamoji
👋 x 🫴 10
👋 y 🫴 2
👋 z 🫴 🐍🫸x🔤%🔤y🫷
💬🫸z🫷
```

## Credits

Thanks to Robert Nystrom for his book "Crafting Interpreters" which inspired the design of this language and provided guidance on how to implement it.

Also thanks to Hack Club for providing a supportive community and motivating me to work on this project.

This documentation was entirely written by hand. AI tools were used for assistance while writing the interpreter.
