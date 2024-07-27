# Screen Activity Tracker

This project is a Screen Activity Tracker application that monitors which applications and websites are used most frequently on a user's system. It includes a backend service that tracks this information and a frontend interface to display it. The frontend interface can be accessed through a web browser or a Windows WPF application using WebView2.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Tracks the active window and application usage. Similar to iphone's Screen Time and Android's Digital Wellbeing
- Displays usage statistics in real-time.
- Web-based frontend built with SvelteKit.
- Windows desktop application using WPF and WebView2.

## Architecture
- **Backend**: Python with Flask, `psutil`, `win32gui`, and `pygetwindow`.
- **Frontend**: SvelteKit for the web interface.
- **Desktop Application**: WPF with WebView2 for displaying the SvelteKit frontend.

## Requirements
- Python 3.8+
- Node.js 14+
- .NET Core 3.1 or later
- Visual Studio 2019 or later (for WPF application)
- Microsoft Edge WebView2 Runtime

## Desktop Application (WPF)

    Open the project in Visual Studio:
    Open the solution file ScreenActivityTracker.sln in Visual Studio.

    Restore NuGet packages:
    Visual Studio should automatically restore the necessary NuGet packages, including Microsoft.Web.WebView2.

    Build and run the application:
    Build the solution and run the WPF application. It will open a window displaying the SvelteKit frontend.

## Usage

    Web Interface: Navigate to http://localhost:5173 in your web browser to view the activity tracker interface.
    Desktop Interface: Run the WPF application from Visual Studio to view the activity tracker interface in a desktop window.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any improvements or bug fixes.

    Fork the repository.
    Create a new branch: git checkout -b feature-branch
    Make your changes and commit them: git commit -m 'Add some feature'
    Push to the branch: git push origin feature-branch
    Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

### Notes:
- Replace `https://github.com/yourusername/screen-activity-tracker.git` with the actual URL of your GitHub repository.
- Update the `.NET Core` version and Visual Studio version based on your actual project requirements if they differ.
- Ensure you include a `requirements.txt` file in your project root for Python dependencies and a `package.json` in the `svelte-frontend` directory for Node.js dependencies.
- If there are additional setup steps or dependencies, be sure to add them to the `Setup Instructions` section.

