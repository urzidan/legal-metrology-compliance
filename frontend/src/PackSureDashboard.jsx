import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import TopNavBar from "./components/TopNavBar";
import InspectionCanvas from "./components/InspectionCanvas";
import RiskScoreGauge from "./components/RiskScoreGauge";
import ComplianceTable from "./components/ComplianceTable";
import ViolationsList from "./components/ViolationsList";
import StickyActionBar from "./components/StickyActionBar";
import ComplianceAuditReport from "./components/ComplianceAuditReport";
import Toast from "./components/Toast";
import {
  uploadInspectionImage,
  fetchComplianceReport,
  enhanceImage,
  syncCapture,
  generateReport,
  escalateInspection,
  confirmAndLog,
} from "./api/packsureApi";

export default function PackSureDashboard() {
  const navigate = useNavigate();
  const [currentImage, setCurrentImage] = useState(null);
  const [inspectionId, setInspectionId] = useState(null);
  const [boundingBoxes, setBoundingBoxes] = useState([]);
  const [extractedFields, setExtractedFields] = useState([]);
  const [violations, setViolations] = useState([]);
  const [riskScore, setRiskScore] = useState(0);
  const [riskBand, setRiskBand] = useState("");
  const [aiConfidence, setAiConfidence] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showReport, setShowReport] = useState(false);

  // Toast state
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");

  // Statistics counters
  const [stats, setStats] = useState({
    audited: 0,
    passRate: 0.0,
    pending: 0,
  });

  // Mocked data for chili flakes jar (used after upload)
  const mockExtractedData = [
    {
      parameter: "Net Quantity",
      detectedValue: "40 g",
      expectedValue: "Standard SI unit (g / kg / ml)",
      status: "pass",
    },
    {
      parameter: "Mfg Date",
      detectedValue: "27 MAR 2026",
      expectedValue: "DD MMM YYYY format",
      status: "pass",
    },
    {
      parameter: "Expiry Date",
      detectedValue: "26 MAR 2028",
      expectedValue: "Valid Date > Mfg Date",
      status: "pass",
    },
    {
      parameter: "Batch Number",
      detectedValue: "AB201059",
      expectedValue: "Valid Alphanumeric Identifier",
      status: "pass",
    },
    {
      parameter: "MRP",
      detectedValue: "99.00",
      expectedValue: "Must include ₹ and '(Incl. of all taxes)'",
      status: "flagged",
    },
  ];

  // -----------------------------------------------------------------
  // Handlers
  // -----------------------------------------------------------------
  const handleUpload = async (file) => {
    try {
      setIsLoading(true);
      if (currentImage && currentImage.startsWith('blob:')) {
        URL.revokeObjectURL(currentImage);
      }

      const uploadData = await uploadInspectionImage(file);
      let imageUrlToUse = uploadData.imageUrl;
      if (!imageUrlToUse || !imageUrlToUse.startsWith('blob:')) {
        imageUrlToUse = URL.createObjectURL(file);
      }
      setCurrentImage(imageUrlToUse);
      setInspectionId(uploadData.inspectionId);

      const reportData = await fetchComplianceReport(uploadData.inspectionId);
      setBoundingBoxes(reportData.boundingBoxes || []);
      setExtractedFields(mockExtractedData); // show mocked data after upload
      setViolations(reportData.violations || []);
      setRiskScore(reportData.riskScore?.value || 0);
      setRiskBand(reportData.riskScore?.band || "");
      setAiConfidence(
        reportData.aiConfidence ? reportData.aiConfidence * 100 : 94.0
      );

      setStats((prev) => ({
        ...prev,
        audited: prev.audited + 1,
        passRate: 92.5,
        pending:
          (reportData.violations?.length || 0) > 0
            ? prev.pending + 1
            : prev.pending,
      }));
    } catch (err) {
      console.error("Inspection error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    if (currentImage && currentImage.startsWith('blob:')) {
      URL.revokeObjectURL(currentImage);
    }
    setCurrentImage(null);
    setInspectionId(null);
    setBoundingBoxes([]);
    setExtractedFields([]);
    setViolations([]);
    setRiskScore(0);
    setRiskBand("");
    setAiConfidence(null);
    setIsLoading(false);
  };

  const handleEnhance = async (operation) => {
    if (!inspectionId) return;
    await enhanceImage(inspectionId, operation);
  };

  const handleSync = async () => {
    await syncCapture(inspectionId || "temp_device");
  };

  /* ────────────────────────────────────────
     Generate Report → show the report page
     ──────────────────────────────────────── */
  const handleGenerateReport = async () => {
    if (!inspectionId) return;
    await generateReport(inspectionId);
    setShowReport(true); // ← switch to report view
  };

  const handleEscalate = async () => {
    if (!inspectionId) return;
    await escalateInspection(inspectionId, "Flagged under Section 6 review");
  };

  const handleConfirmAndLog = async () => {
    console.log("▶️ handleConfirmAndLog called, inspectionId:", inspectionId);
    if (!inspectionId) {
      setToastMessage("No audit data to log");
      setShowToast(true);
      return;
    }

    try {
      await confirmAndLog(inspectionId, {});
      console.log("✅ confirmAndLog resolved");
    } catch (err) {
      console.error("❌ Confirm & Log error:", err);
      setToastMessage("Failed to log audit");
      setShowToast(true);
      return;
    }

    // 1️⃣ Show toast
    setToastMessage("Audit Logged Successfully");
    setShowToast(true);

    // 2️⃣ Increment total audited
    setStats(prev => ({
      ...prev,
      audited: prev.audited + 1,
    }));

    // 3️⃣ Reset workspace – clear image & extracted data
    if (currentImage && currentImage.startsWith('blob:')) {
      URL.revokeObjectURL(currentImage);
    }
    setCurrentImage(null);
    setInspectionId(null);
    setBoundingBoxes([]);
    setExtractedFields([]);
    setViolations([]);
    setRiskScore(0);
    setRiskBand("");
    setAiConfidence(null);
    setIsLoading(false);
  };

  // Auto‑hide toast after 3 seconds
  useEffect(() => {
    let timerId = null;
    if (showToast) {
      timerId = window.setTimeout(() => setShowToast(false), 3000);
    }
    return () => {
      if (timerId) clearTimeout(timerId);
    };
  }, [showToast]);

  const handleProfileClick = () => navigate("/profile");
  const handleSettingsClick = () => navigate("/settings");

  // -----------------------------------------------------------------
  // Render
  // -----------------------------------------------------------------
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <TopNavBar
        totalAudited={stats.audited}
        passRate={stats.passRate}
        pending={stats.pending}
        onProfileClick={handleProfileClick}
        onSettingsClick={handleSettingsClick}
      />

      {/* Toast notification (appears at top‑center) */}
      {showToast && (
        <Toast message={toastMessage} onClose={() => setShowToast(false)} />
      )}

      {/* ── Conditional rendering ── */}
      {!showReport ? (
        /* ---------- DASHBOARD VIEW ---------- */
        <>
          <main className="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 pb-24">
            {/* Left Column: Image Canvas */}
            <InspectionCanvas
              imageUrl={currentImage}
              boundingBoxes={boundingBoxes}
              aiConfidence={aiConfidence}
              loading={isLoading}
              onUpload={handleUpload}
              onClear={handleClear}
              onSync={handleSync}
              onEnhance={handleEnhance}
            />

            {/* Right Column: Risk & Compliance Output */}
            <div className="lg:col-span-7 flex flex-col gap-6">
              <RiskScoreGauge score={riskScore} band={riskBand} />
              <ComplianceTable fields={extractedFields} />
              <ViolationsList violations={violations} />
            </div>
          </main>

          <StickyActionBar
            hasActiveScan={Boolean(currentImage)}
            onGenerateReport={handleGenerateReport}
            onEscalate={handleEscalate}
            onConfirmAndLog={handleConfirmAndLog}
          />
        </>
      ) : (
        /* ---------- REPORT VIEW ---------- */
        <ComplianceAuditReport
          onBack={() => setShowReport(false)} // ← go back to dashboard
        />
      )}
    </div>
  );
}