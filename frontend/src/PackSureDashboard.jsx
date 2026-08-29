import React, { useState } from "react";
import TopNavBar from "./components/TopNavBar";
import InspectionCanvas from "./components/InspectionCanvas";
import RiskScoreGauge from "./components/RiskScoreGauge";
import ComplianceTable from "./components/ComplianceTable";
import ViolationsList from "./components/ViolationsList";
import StickyActionBar from "./components/StickyActionBar";
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
  const [currentImage, setCurrentImage] = useState(null);
  const [inspectionId, setInspectionId] = useState(null);
  const [boundingBoxes, setBoundingBoxes] = useState([]);
  const [extractedFields, setExtractedFields] = useState([]);
  const [violations, setViolations] = useState([]);
  const [riskScore, setRiskScore] = useState(0);
  const [riskBand, setRiskBand] = useState("");
  const [aiConfidence, setAiConfidence] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Statistics counters
  const [stats, setStats] = useState({
    audited: 0,
    passRate: 0.0,
    pending: 0,
  });

  // Handle image upload & fetch report
  const handleUpload = async (file) => {
    try {
      setIsLoading(true);
      const data = await uploadInspectionImage(file);

      // Populate states directly from the FastAPI response
      setCurrentImage(data.imageUrl || URL.createObjectURL(file));
      setInspectionId(data.inspectionId);
      setBoundingBoxes(data.boundingBoxes || []);
      setExtractedFields(data.extractedFields || []);
      setViolations(data.violations || []);
      setRiskScore(data.riskScore?.value || 0);
      setRiskBand(data.riskScore?.band || "");
      setAiConfidence(
        data.aiConfidence ? data.aiConfidence * 100 : 94.0
      );

      setStats((prev) => ({
        ...prev,
        audited: prev.audited + 1,
        passRate: 92.5,
        pending: (data.violations?.length || 0) > 0 ? prev.pending + 1 : prev.pending,
      }));
    } catch (err) {
      console.error("Inspection error:", err);
    } finally {
      setIsLoading(false);
    }
  };
  // Complete Reset / Delete handler
  const handleClear = () => {
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

  const handleGenerateReport = async () => {
    if (!inspectionId) return;
    await generateReport(inspectionId);
  };

  const handleEscalate = async () => {
    if (!inspectionId) return;
    await escalateInspection(inspectionId, "Flagged under Section 6 review");
  };

  const handleConfirmAndLog = async () => {
    if (!inspectionId) return;
    await confirmAndLog(inspectionId, {});
  };

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <TopNavBar
        totalAudited={stats.audited}
        passRate={stats.passRate}
        pending={stats.pending}
      />

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
        onConfirm={handleConfirmAndLog}
      />
    </div>
  );
}