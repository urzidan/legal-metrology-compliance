import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ProfilePage() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    organization: "",
    role: "",
    phone: "",
    address: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, you would send this to a backend API
    alert("Profile saved successfully!");
    // Optionally, navigate back to dashboard
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background text-on-background">
      {/* Top navigation bar for profile page */}
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
          <h2 className="text-2xl font-bold mb-6">Profile Settings</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <div>
                <label className="block text-sm font-medium mb-2">Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={profile.name}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={profile.email}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Enter your email"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Organization</label>
                <input
                  type="text"
                  name="organization"
                  value={profile.organization}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Enter your organization"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Role</label>
                <input
                  type="text"
                  name="role"
                  value={profile.role}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Enter your role"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Phone Number</label>
                <input
                  type="tel"
                  name="phone"
                  value={profile.phone}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Enter your phone number"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Address</label>
                <textarea
                  name="address"
                  value={profile.address}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-outline-variant rounded bg-surface text-on-background focus:outline-none focus:ring-2 focus:ring-primary"
                  rows="3"
                  placeholder="Enter your address"
                />
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                className="bg-primary text-on-primary px-6 py-3 rounded text-xs font-semibold uppercase tracking-wider hover:bg-primary-container hover:text-on-primary-container transition-colors"
              >
                Save Profile
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
