Here’s a concise cheat sheet covering basic Python concepts: (from chatgpt)

## Python Basics Cheat Sheet

### 1. **Syntax and Basics**
- **Comments**: `# Single line comment`  
- **Multi-line comment**: `"""Multi-line comment"""`

### 2. **Variables and Data Types**
- **Integer**: `x = 10`
- **Float**: `y = 10.5`
- **String**: `name = "Alice"`
- **Boolean**: `is_active = True`
- **NoneType**: `none_value = None`

### 3. **Operators**
- **Arithmetic Operators**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Comparison Operators**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical Operators**: `and`, `or`, `not`
- **Assignment Operators**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `**=`

### 4. **Data Structures**
- **List**: `my_list = [1, 2, 3]`
  - Access: `my_list[0]`
  - Slicing: `my_list[1:3]`
  - Methods: `append()`, `extend()`, `remove()`, `pop()`, `sort()`, `reverse()`
- **Tuple**: `my_tuple = (1, 2, 3)`
  - Immutable list
- **Dictionary**: `my_dict = {'key1': 'value1', 'key2': 'value2'}`
  - Access: `my_dict['key1']`
  - Methods: `keys()`, `values()`, `items()`, `get()`, `update()`
- **Set**: `my_set = {1, 2, 3}`
  - Methods: `add()`, `remove()`, `union()`, `intersection()`, `difference()`

### 5. **Control Structures**
- **Conditional Statements**:
  ```python
  if condition:
      # code
  elif condition:
      # code
  else:
      # code
  ```
- **Loops**:
  - **For Loop**: 
    ```python
    for item in iterable:
        # code
    ```
  - **While Loop**: 
    ```python
    while condition:
        # code
    ```

### 6. **Functions**
```python
def function_name(parameters):
    # code
    return value
```
- **Example**:
  ```python
  def add(a, b):
      return a + b
  ```

### 7. **Classes and Objects**
```python
class MyClass:
    def __init__(self, attribute):
        self.attribute = attribute
    
    def method(self):
        # code

# Create an object
my_object = MyClass(value)
```

### 8. **Modules and Packages**
- **Importing a module**: `import module_name`
- **Importing specific attributes**: `from module_name import attribute`
- **Installing packages**: `pip install package_name`

### 9. **File I/O**
- **Opening a file**: 
  ```python
  file = open('file.txt', 'r')  # 'r' for read, 'w' for write, 'a' for append
  content = file.read()
  file.close()
  ```
- **With statement**: 
  ```python
  with open('file.txt', 'r') as file:
      content = file.read()
  ```

### 10. **Error Handling**
```python
try:
    # code that may raise an error
except ExceptionType as e:
    # code that runs if an error occurs
else:
    # code that runs if no error occurs
finally:
    # code that runs no matter what
```

### 11. **Common Built-in Functions**
- **`len()`**: Get length
- **`type()`**: Get type
- **`print()`**: Print to console
- **`input()`**: Get user input
- **`range()`**: Generate a range of numbers
- **`int()`, `float()`, `str()`**: Type conversion

### 12. **List Comprehensions**
```python
new_list = [expression for item in iterable if condition]
```
- **Example**:
  ```python
  squares = [x**2 for x in range(10)]
  ```

### 13. **Lambda Functions**
```python
lambda arguments: expression
```
- **Example**:
  ```python
  add = lambda a, b: a + b
  ```

### 14. **Map, Filter, Reduce**
- **Map**: `map(function, iterable)`
- **Filter**: `filter(function, iterable)`
- **Reduce**: 
  ```python
  from functools import reduce
  reduce(function, iterable)
  ```

### 15. **Date and Time**
```python
import datetime
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
```

### 16. **Regular Expressions**
```python
import re
pattern = r'pattern'
if re.match(pattern, string):
    # code
```

### 17. **Useful Python Libraries**
- **NumPy**: Numerical computing
- **Pandas**: Data analysis
- **Matplotlib**: Plotting
- **Requests**: HTTP requests
- **BeautifulSoup**: Web scraping

This cheat sheet provides a quick overview of essential Python concepts, suitable for beginners to reference during coding.
