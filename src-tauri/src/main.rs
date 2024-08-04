// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Child};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;
use tauri::Manager;

fn start_python_script() -> Result<Child, String> {
    Command::new("python")
        .arg("apptracker_main.py") // Change this to the actual path of your Python script
        .spawn()
        .map_err(|e| e.to_string())
}

fn main() {
    // Start the Python script
    match start_python_script() {
        Ok(child) => {
            println!("Python script started successfully");

            // Use Arc and Mutex to safely share the child process handle
            let child_arc = Arc::new(Mutex::new(Some(child)));

            // Run the Tauri application
            tauri::Builder::default()
                .setup(move |app| {
                    let handle = app.handle();
                    let child_arc_clone = Arc::clone(&child_arc);

                    // Ensure the Python script is killed when the Tauri app exits
                    handle.listen_global("exit", move |_| {
                        let mut locked_child = child_arc_clone.lock().unwrap();
                        if let Some(mut child) = locked_child.take() {
                            if let Err(e) = child.kill() {
                                eprintln!("Failed to kill Python script process: {}", e);
                            }
                        }
                    });

                    // Optionally, wait a few seconds to ensure the Python server is up
                    thread::sleep(Duration::from_secs(1));

                    Ok(())
                })
                .run(tauri::generate_context!())
                .expect("error while running tauri application");
        }
        Err(e) => eprintln!("Failed to start Python script: {}", e),
    }
}