# AppTimeTracker for Windows (v0.1.0)

Welcome to **AppTimeTracker** v0.1.0, a simple screen time tracking app for Windows (for now). This application is built with a modern tech stack, featuring **SvelteKit** for the frontend, **Python** & **Rust** for the backend, and **Tauri** to bundle it all into an efficient, lightweight desktop app.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Current Limitations](#current-limitations)
- [Future Plans](#future-plans)
- [Acknowledgments](#acknowledgments)

## Introduction

The idea behind AppTimeTracker came from the need to monitor screen time efficiently, similar to how Apple Screen Time works on mobile devices. This journey began with basic Python knowledge and evolved into a functional app within a week, thanks to GPT-4's assistance and some traditional learning methods.

## Features

- **Real-time Screen Time Tracking**: Monitor the active window and application usage in real-time.
- **Minimalist UI**: Simple and intuitive interface built with SvelteKit.
- **Python Backend**: Leverages Python for tracking processes and serving data.
- **Tauri Integration**: Bundled with Tauri for an optimized, lightweight desktop application.
- **Persistent Tracking**: Continues tracking until the app is closed.

## Tech Stack

- **Frontend**: SvelteKit
- **Backend**: Python(For Now), Rust (In upcoming release)
- **Desktop Integration**: Tauri (Rust)

## Installation

### Prerequisites

- **Node.js** (for SvelteKit)
- **Python 3** (for backend)
- **Tauri** (for bundling the application)

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/AppTimeTracker.git
    cd AppTimeTracker
    ```

2. **Install Frontend Dependencies**:
    ```bash
    cd ../AppTimeTracker
    npm install
    ```

3. **Build the Tauri App**:
    ```bash
    cd ../AppTimeTracker/src-tauri
    cargo build
    ```

4. **Run the App**:
    ```bash
    cd ../AppTimeTracker
    npm tauri dev
    ```

## Usage

1. **Start the App**:
    - Run the Tauri app which starts the Python script in the background.
    - The app UI will show the screen time from the moment it starts.

2. **Track Screen Time**:
    - The app captures the active window title and executable file name to calculate usage time.

3. **Enable App on Startup**(Still Work in Progress):
    - Toggle the switch in the UI to enable or disable the app on system startup.

## Current Limitations

- **Stopping the Python Script**: Currently, the Python script does not stop running unless the system is restarted. This is a known issue and will be addressed in future updates.

## Future Plans

- **Enhanced UI**: Improve the UI/UX for better visualization of screen time.
- **Real-time Database**: Store and retrieve screen time data for detailed analysis.
- **Advanced Features**: Integrate LLM for categorizing app usage and providing productivity insights.:)
- **Optimize Performance**: Transition backend logic to Rust for more efficiency.

## Acknowledgments

A big thanks to GPT-4 for its invaluable assistance and to the traditional resources like StackOverflow, Reddit, and various tutorials for providing additional insights. Special mention to the Tauri community for their robust framework and support.

## Final Thoughts

Creating AppTimeTracker was an exciting journey from basic Python knowledge to developing a functional desktop app. This project highlights the balance between leveraging AI tools like GPT-4 and traditional learning methods for rapid development and personal growth. While the code may not be perfect, my idea was good.😊
