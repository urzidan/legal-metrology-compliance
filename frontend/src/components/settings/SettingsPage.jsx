import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import useTheme from "../../hooks/useTheme";

export default function SettingsPage() {
  const navigate = useNavigate();
  const [theme, setTheme] = useTheme();
  const [settings, setSettings] = useState({
    notifications: true,
    emailAlerts: true,
    autoSync: false,
    language: "en",
    dateFormat: "MM/DD/YYYY",
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (name === "theme") {
      setTheme(value);
    } else {
      const newValue = type === "checkbox" ? checked : value;
      setSettings((prev) => ({
        ...prev,
        [name]: newValue,
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, you would send this to a backend API
    alert("Settings saved successfully!");
    // Optionally, navigate back to dashboard
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background text-on-background">
      {/* Top navigation bar for settings page */}
      <header className="sticky top-0 z-50 flex justify-between items-center w-full px-8 py-4 bg-surface border-b border-outline-variant">
        <div className="flex items-center gap-6">
          <h1 className="text-3xl font-bold tracking-tight text-on-background">PackSure</h1>
          <span className="bg-primary-container text-on-primary-container text-xs font-semibold px-2 py-1 rounded-full uppercase tracking-wide">
            SIH 2026 | Team Innovate Ninjas
          </span>
        </div>

        <div className="flex items-center gap-3">
          <button onClick={() => navigate("/")} className="text-primary hover:bg-surface-container-low p-2 rounded-full transition-colors">
            ← Back to Dashboard
          </button>
        </div>
      </header>

      <main className="p-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-6">Settings</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <div>
                <label className="block text-sm font-medium mb-2">Theme</label>
                <select
                  name="theme"
                  value={theme}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="auto">Auto (System)</option>
                </select>
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    name="notifications"
                    checked={settings.notifications}
                    onChange={handleChange}
                    className="h-4 w-4 text-primary focus:ring-primary border-outline-variant rounded"
                  />
                  Enable Notifications
                </label>
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    name="emailAlerts"
                    checked={settings.emailAlerts}
                    onChange={handleChange}
                    className="h-4 w-4 text-primary focus:ring-primary border-outline-variant rounded"
                  />
                  Email Alerts
                </label>
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    name="autoSync"
                    checked={settings.autoSync}
                    onChange={handleChange}
                    className="h-4 w-4 text-primary focus:ring-primary border-outline-variant rounded"
                  />
                  Auto-scan when device connected
                </label>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Language</label>
                <select
                  name="language"
                  value={settings.language}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Date Format</label>
                <select
                  name="dateFormat"
                  value={settings.dateFormat}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                className="bg-primary text-on-primary px-6 py-3 rounded text-xs font-semibold uppercase tracking-wider hover:bg-primary-container hover:text-on-primary-container transition-colors"
              >
                Save Settings
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}