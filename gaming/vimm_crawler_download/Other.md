## Useful tips in Python

- download a file and put in in a specific path with specific name:
``` 
binary_content = response.content
with open('downloaded_image.jpg', 'wb') as file:
    file.write(binary_content)
```