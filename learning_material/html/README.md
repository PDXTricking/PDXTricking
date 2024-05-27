### HTML Basics Cheat Sheet

#### 1. **HTML Structure**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <!-- Content goes here -->
  </body>
</html>
```

- `<!DOCTYPE html>`: Defines the document type and version (HTML5).
- `<html>`: Root element of an HTML page.
- `<head>`: Container for meta-information, scripts, styles, and the title.
- `<title>`: Sets the title of the page, shown in the browser's title bar or tab.
- `<body>`: Contains the content of the HTML document.

#### 2. **Common HTML Elements**

- **Headings**
  ```html
  <h1>Heading 1</h1>
  <h2>Heading 2</h2>
  <h3>Heading 3</h3>
  <h4>Heading 4</h4>
  <h5>Heading 5</h5>
  <h6>Heading 6</h6>
  ```
- **Paragraph**
  ```html
  <p>This is a paragraph.</p>
  ```
- **Line Break**
  ```html
  <br>
  ```
- **Horizontal Line**
  ```html
  <hr>
  ```

#### 3. **Text Formatting**

- **Bold**
  ```html
  <b>Bold Text</b>
  <strong>Strong Text</strong>
  ```
- **Italic**
  ```html
  <i>Italic Text</i>
  <em>Emphasized Text</em>
  ```
- **Underline**
  ```html
  <u>Underlined Text</u>
  ```
- **Strikethrough**
  ```html
  <s>Strikethrough Text</s>
  ```

#### 4. **Links and Images**

- **Hyperlink**
  ```html
  <a href="https://example.com">Visit Example</a>
  ```
- **Image**
  ```html
  <img src="image.jpg" alt="Description of image">
  ```

#### 5. **Lists**

- **Unordered List**
  ```html
  <ul>
    <li>List item 1</li>
    <li>List item 2</li>
    <li>List item 3</li>
  </ul>
  ```
- **Ordered List**
  ```html
  <ol>
    <li>First item</li>
    <li>Second item</li>
    <li>Third item</li>
  </ol>
  ```
- **Description List**
  ```html
  <dl>
    <dt>Term 1</dt>
    <dd>Description 1</dd>
    <dt>Term 2</dt>
    <dd>Description 2</dd>
  </dl>
  ```

#### 6. **Tables**

```html
<table>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
  </tr>
  <tr>
    <td>Data 1</td>
    <td>Data 2</td>
  </tr>
</table>
```

- `<table>`: Defines a table.
- `<tr>`: Defines a row in a table.
- `<th>`: Defines a header cell in a table.
- `<td>`: Defines a standard cell in a table.

#### 7. **Forms**

```html
<form action="/submit" method="post">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name">
  
  <label for="email">Email:</label>
  <input type="email" id="email" name="email">
  
  <input type="submit" value="Submit">
</form>
```

- `<form>`: Defines a form.
- `<label>`: Defines a label for an `<input>` element.
- `<input>`: Defines an input field.
  - `type`: Specifies the type of input (e.g., `text`, `email`, `submit`).

#### 8. **Semantic HTML5 Elements**

- **Article**
  ```html
  <article>
    <h2>Article Title</h2>
    <p>Content of the article.</p>
  </article>
  ```
- **Section**
  ```html
  <section>
    <h2>Section Title</h2>
    <p>Content of the section.</p>
  </section>
  ```
- **Nav**
  ```html
  <nav>
    <ul>
      <li><a href="#home">Home</a></li>
      <li><a href="#about">About</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>
  ```
- **Aside**
  ```html
  <aside>
    <p>Side content.</p>
  </aside>
  ```
- **Footer**
  ```html
  <footer>
    <p>Footer content.</p>
  </footer>
  ```

#### 9. **Media Elements**

- **Audio**
  ```html
  <audio controls>
    <source src="audio.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
  ```
- **Video**
  ```html
  <video controls>
    <source src="video.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  ```

#### 10. **Meta Information**

- **Meta Tags**
  ```html
  <meta charset="UTF-8">
  <meta name="description" content="Free Web tutorials">
  <meta name="keywords" content="HTML, CSS, JavaScript">
  <meta name="author" content="John Doe">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  ```

This cheat sheet covers the fundamental concepts of HTML necessary to create and structure web pages.
