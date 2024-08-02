use tauri::command;
use serde_json::Value;
use reqwest;

#[command]
async fn get_app_usage_data() -> Result<Value, String> {
    let client = reqwest::Client::new();
    let res = client.get("http://localhost:5000/data")
        .send()
        .await
        .map_err(|e| e.to_string())?;
    
    let data = res.json::<Value>()
        .await
        .map_err(|e| e.to_string())?;
    
    Ok(data)
}

#[tauri::command]
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_app_usage_data])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}