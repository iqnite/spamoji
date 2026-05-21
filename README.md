# spamoji

A programming language that only uses emojis as syntax and encourages writing spaghetti code.

## Example

```spamoji
🗒️ A function to calculate factorial
⚙️ 🔢❕ 🔰
    👋 🏁 🫴 1
    🔃 🔰 🤜 1
        🏁 🫴 🏁 ✖️ 🔰
        🔰 🫴 🔰 ➖ 1
    ↩️ 🏁

💭 🔤Enter a number to calculate the factorial: 🔤
👋 😀 🫴 🔢 ⌨️❗❗
🤔 😀 🟰 ⚠️
👍️
    💬 🔤Invalid input.🔤❗
👎
    💬 🔤The factorial of 🔤😀🔤 is 🔤🫸🔢❕ 😀❗🫷❗
```

## What's this all about?

This language is a learning project. I have written this documentation before writing the interpreter, so I might need to make adjustments to the language design as I implement it. If this experiment is successful, I might move on and begin working on Esore, a more serious language I've been designing in the past 2 years.

> [!CAUTION]
> The spamoji language is intended for educational purposes only and should not be used for production code.

## Usage

To run a spamoji program, you will need to use the spamoji interpreter.

You can provide a spamoji file (with the .🍝 extension) as input to run it. For example:

```bash
spamoji my_program.🍝
```

If no file is supplied, the interactive REPL will start, which allows to enter and evaluate expressions directly.

## Syntax

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
- 🛑 Stop statement: Terminates the program
- 🧩 Import statement: Followed by a file name, it gets replaced by the contents of that file before execution
- 🐍 Python statement: Followed by Python code to be executed

Some statements can be nested, such as if statements and loops. Indentation is used to indicate the scope of these statements. Indented blocks are considered part of the previous statement until the indentation level decreases. Variables declared inside of a block are only accessible inside of that block and any nested blocks.

### Functions

Functions are defined using the ⚙️ emoji, followed by the function name and parameters. The function body is indented and can contain any valid statements. The function can return a value using the ↪️ emoji.

Functions can be called by using their name followed by the arguments, separated by spaces, followed by the ❗ emoji.

### Variables

Variables are declared using the 👋 emoji, followed by the variable assignment expression. An assinment expression starts with the variable name, followed by 🫴 and a value. Variable names can be any combination of letters, numbers, and emojis, but must start with a letter or emoji. Variables can be used in expressions and statements after they have been assigned.

### Expressions

Many statements can be used as expressions within other statements. 🫸 and 🫷 can be used to group expressions and control the order of evaluation. For example, you can use a function call as part of an if statement condition or as part of a variable assignment.

### Operators

The language supports basic operators for logical and arithmetic operations. These can be used between two values to perform calculations.

- ➕: Addition
- ➖: Subtraction
- ✖️: Multiplication
- ➗: Division
- 🟰: Equal
- 🆚: Not equal
- 🤜: Greater than
- 🤛: Less than
- 🤝: Logical AND
- 🤲: Logical OR
- 🙅: Logical NOT

<!-- Operators can be used directly after 👋 in variable assignments to perform operations on the variable. For example, `👋➕ x 1` will increment the variable `x` by 1. -->

### Strings

Strings are sequences of characters enclosed in 🔤 on each side. They can contain any characters, including emojis. Strings can be used in variable assignments, printed to the console, and concatenated using the ➕ operator.

Values directly before or after a string will also be concatenated with that string.

### Built-ins

The language includes several built-in functions and values for common operations, such as:

- 🔢: Convert input to a number
- ⌨️: Read input from the user
- 💬: Print output to a new line in the console
- ✅: A special value representing true
- ❌: A special value representing false
- 🫥: A special value representing null
- ⚠️: A special value representing an error or undefined value

## Credits

Thanks to Robert Nystrom for his book "Crafting Interpreters" which inspired the design of this language and provided guidance on how to implement it.

Also thanks to Hack Club for providing a supportive community and motivating me to work on this project.

This documentation was entirely written by hand. I might use AI tools for assistance while writing the interpreter.
