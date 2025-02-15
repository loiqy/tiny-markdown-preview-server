# Tiny Markdown Preview Server

## Introduction
zh_CN [简体中文](README_zh.md)

A simple Flask-based Markdown preview server that lets you navigate directories and preview Markdown files with a GitHub-like style.

## Features
- **File Explorer:** Browse directories and display Markdown files.
- **Real-time Markdown Preview:** Render Markdown content live.
- **Tab Management:** Open, close, and switch between multiple Markdown files.
- **Favorites:** Easily save and access frequently used files.
- **Multilingual Support:** Support for both Chinese and English.

![Screenshot](assets/image.png)

## Known Bugs

1. Switching languages or un-favoriting an item in the Favorites pane may cause the favorite/unfavorite buttons in the file explorer to malfunction.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/loiqy/tiny-markdown-preview-server.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd tiny-markdown-preview-server
    ```
3. **Install dependencies:**
    ```bash
    pip install flask markdown
    ```

## Usage

Run the application with:
```bash
python app.py /path/to/your/markdown/files
```
Open your browser at [http://localhost:8900](http://localhost:8900) to start previewing.

## Remote Server Usage Tips

To preview locally after starting the server on a remote machine, you can use SSH port forwarding:

1. Start the application on the server:
    ```bash
    python app.py /path/to/your/markdown/files
    ```
2. On your local machine, establish an SSH tunnel:
    ```bash
    ssh -L 8900:localhost:8900 your_remote_user@remote_server_ip
    ```
3. Open your browser at [http://localhost:8900](http://localhost:8900) to view the preview.

## Configuration

- **Base Directory:** Specify a custom directory by passing the path when launching the app.
- **Favorites:** Managed via `userdata/favorites.json` (this directory is excluded from version control).

## Contributing

Contributions are welcome! Please submit issues or pull requests for any improvements.

## License

This project is licensed under the [MIT License](LICENSE).
