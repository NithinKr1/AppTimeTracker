// activity-tracker.js

const { app, BrowserWindow } = require('electron');
const activeWindow = require('active-win');
const express = require('express');
const cors = require('cors');

class ScreenActivityTracker {
  constructor() {
    this.processTime = {};
    this.timestamp = {};
    this.doRun = true;
  }

  async getActiveWindowTitle() {
    try {
      const result = await activeWindow();
      return result ? result.title : null;
    } catch (e) {
      console.error(`Error getting active window title: ${e}`);
      return null;
    }
  }

  async trackActivity(sleepTime) {
    while (this.doRun) {
      try {
        const activeWindow = await this.getActiveWindowTitle();
        if (activeWindow) {
          const currentTimestamp = Math.floor(Date.now() / 1000);
          
          if (!(activeWindow in this.processTime)) {
            this.processTime[activeWindow] = 0;
          }
          
          if (activeWindow in this.timestamp) {
            this.processTime[activeWindow] += currentTimestamp - this.timestamp[activeWindow];
          }
          
          this.timestamp[activeWindow] = currentTimestamp;
          
          // Split window title and track individual parts
          const parts = activeWindow.split(/\s-\s|\s—\s/);
          for (const part of parts) {
            const titleCasePart = part.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
            if (!(titleCasePart in this.processTime)) {
              this.processTime[titleCasePart] = 0;
            }
            this.processTime[titleCasePart] += currentTimestamp - this.timestamp[activeWindow];
          }
        }
        
        await new Promise(resolve => setTimeout(resolve, sleepTime * 1000));
      } catch (e) {
        console.error(`Error tracking activity: ${e}`);
      }
    }
  }

  getSortedProcessTime() {
    return Object.fromEntries(
      Object.entries(this.processTime).sort(([,a],[,b]) => b-a)
    );
  }
}

function createApp(tracker) {
  const app = express();
  app.use(cors());

  app.get('/data', (req, res) => {
    res.json(tracker.getSortedProcessTime());
  });

  return app;
}

function main() {
  const tracker = new ScreenActivityTracker();
  const expressApp = createApp(tracker);

  // Start tracking in the background
  tracker.trackActivity(1);

  // Start express server
  const port = 5000;
  expressApp.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
  });

  // Create Electron window
  app.whenReady().then(() => {
    const win = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
      }
    });

    win.loadURL('http://localhost:5173'); // Assuming your Svelte app runs on this port
  });
}

main();