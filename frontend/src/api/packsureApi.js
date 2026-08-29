// packsureApi.js
// Dual-mode API client: Toggle USE_MOCK to true for instant demoing/testing,
// or false to route through the live FastAPI backend.

const USE_MOCK = false;
const BASE_URL = import.meta.env?.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

// In-memory store to simulate active inspection state during mock mode
let mockInspectionStore = null;

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { Accept: "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`PackSure API error ${res.status}: ${body || res.statusText}`);
  }
  return res.json();
}

/**
 * Upload a captured/selected product image for inspection.
 */
export async function uploadInspectionImage(file) {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 800)); // Simulate network latency
    const localImageUrl = URL.createObjectURL(file);
    const mockId = `insp_${Date.now()}`;

    mockInspectionStore = {
      inspectionId: mockId,
      imageUrl: localImageUrl,
      aiConfidence: 0.94,
      riskScore: {
        value: 28,
        max: 100,
        band: "Low Risk - Minor Non-Compliance",
      },
      boundingBoxes: [
        { id: "box-1", label: "MRP", x: 62, y: 38, width: 28, height: 8, status: "flagged" },
        { id: "box-2", label: "Net Quantity", x: 14, y: 72, width: 22, height: 7, status: "pass" },
        { id: "box-3", label: "Mfg Date & Batch", x: 58, y: 72, width: 32, height: 9, status: "pass" },
        { id: "box-4", label: "Consumer Care", x: 12, y: 82, width: 44, height: 12, status: "pass" },
        { id: "box-5", label: "Barcode (EAN-13)", x: 68, y: 84, width: 24, height: 10, status: "pass" }
      ],
      extractedFields: [
        {
          parameter: "Maximum Retail Price (MRP)",
          detectedValue: "Rs. 149.00",
          expectedValue: "₹ 149.00 (Incl. of all taxes)",
          status: "flagged"
        },
        {
          parameter: "Net Quantity",
          detectedValue: "200 g",
          expectedValue: "Standard SI unit (g / kg / ml)",
          status: "pass"
        },
        {
          parameter: "Date of Manufacture / Packing",
          detectedValue: "07/2026",
          expectedValue: "MM/YYYY format visible",
          status: "pass"
        },
        {
          parameter: "Batch / Lot Number",
          detectedValue: "BN-IN-9821A",
          expectedValue: "Valid Batch Identifier",
          status: "pass"
        },
        {
          parameter: "Country of Origin",
          detectedValue: "Made in India",
          expectedValue: "Clear declaration on principal display",
          status: "pass"
        },
        {
          parameter: "Consumer Care Details",
          detectedValue: "care@packsure.in | 1800-111-999",
          expectedValue: "Name, address, tel/email of contact",
          status: "pass"
        }
      ],
      violations: [
        {
          rule: "Rule 6(1)(e) - Legal Metrology (Packaged Commodities) Rules, 2011",
          description: "MRP declaration does not contain the mandatory '(Inclusive of all taxes)' suffix or official ₹ currency symbol.",
          severity: "Medium"
        }
      ]
    };

    return { inspectionId: mockId, imageUrl: localImageUrl, status: "processing" };
  }

  const formData = new FormData();
  formData.append("file", file);
  return request("/inspections", { method: "POST", body: formData });
}

/**
 * Poll / fetch the compliance-engine output for a given inspection.
 */
export async function fetchComplianceReport(inspectionId) {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 600));
    return mockInspectionStore || { status: "not_found" };
  }
  return request(`/inspections/${inspectionId}/report`);
}

/**
 * Trigger a de-glare / crop / zoom enhancement pass.
 */
export async function enhanceImage(inspectionId, operation, params = {}) {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return { success: true, operation, message: `Enhanced with ${operation}` };
  }
  return request(`/inspections/${inspectionId}/enhance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ operation, params }),
  });
}

/**
 * Re-sync with a connected camera / scanning device.
 */
export async function syncCapture(inspectionId) {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return { synced: true, timestamp: new Date().toISOString() };
  }
  return request(`/inspections/${inspectionId}/sync`, { method: "POST" });
}

/**
 * Generate a downloadable PDF compliance report.
 */
export async function generateReport(inspectionId) {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 400));
    alert(`[SIH Demo] Compliance Audit Report generated for ${inspectionId}. Ready for download.`);
    return { pdfUrl: "#" };
  }
  return request(`/inspections/${inspectionId}/report/pdf`);
}

/**
 * Escalate a flagged inspection to a human compliance officer.
 */
export async function escalateInspection(inspectionId, note = "") {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 400));
    alert(`[SIH Demo] Inspection ${inspectionId} escalated to Senior Metrology Officer. Note: "${note || 'Manual review required'}"`);
    return { escalated: true };
  }
  return request(`/inspections/${inspectionId}/escalate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note }),
  });
}

/**
 * Confirm the human-reviewed result and log it as final.
 */
export async function confirmAndLog(inspectionId, overrides = {}) {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 400));
    alert(`[SIH Demo] Inspection ${inspectionId} confirmed and permanently logged to the digital audit trail.`);
    return { logged: true, timestamp: new Date().toISOString() };
  }
  return request(`/inspections/${inspectionId}/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ overrides }),
  });
}