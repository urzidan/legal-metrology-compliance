import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PackSureDashboard from "./PackSureDashboard";
import ProfilePage from "./components/profile/ProfilePage";
import SettingsPage from "./components/settings/SettingsPage";
import useTheme from "./hooks/useTheme";

function App() {
  const [theme] = useTheme(); // Initialize theme (sets dark mode class on root)

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-on-background">
        <Routes>
          <Route path="/" element={<PackSureDashboard />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;