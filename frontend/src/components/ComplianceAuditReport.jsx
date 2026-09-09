import React from "react";

/**
 * ComplianceAuditReport
 * A printable A4‑style report.
 * Props:
 *   onBack – function to call when the user wants to return to the dashboard.
 */
export default function ComplianceAuditReport({ onBack }) {
  const today = new Date().toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  const auditId = "PACKSURE-AUDIT-2026-09-09-001";
  const overallStatus = "Minor Non-Compliance (Requires Human-in-the-Loop Review)";
  const riskScore = "28 / 100";

  const extractedRows = [
    {
      parameter: "Net Quantity",
      detected: "40 g",
      expected: "Standard SI unit (g / kg / ml)",
      status: "Pass",
    },
    {
      parameter: "Mfg Date",
      detected: "27 MAR 2026",
      expected: "DD MMM YYYY format",
      status: "Pass",
    },
    {
      parameter: "Expiry Date",
      detected: "26 MAR 2028",
      expected: "Valid Date > Mfg Date",
      status: "Pass",
    },
    {
      parameter: "Batch Number",
      detected: "AB201059",
      expected: "Valid Alphanumeric Identifier",
      status: "Pass",
    },
    {
      parameter: "MRP",
      detected: "99.00",
      expected: "Must include ₹ and '(Incl. of all taxes)'",
      status: "Flagged",
    },
  ];

  const violation = {
    framework: "Legal Metrology (Packaged Commodities) Rules, 2011",
    rule: "Rule 6(1)(e)",
    description:
      "The MRP declaration does not contain the mandatory suffix \"(Inclusive of all taxes)\" or the official Indian Rupee currency symbol (₹).",
    action:
      "Escalate to the Packaging Artwork Team. Update the label design to read \"MRP ₹ 99.00 (Incl. of all taxes)\" before the next production run.",
  };

  return (
    <div
      className="
        min-h-screen
        flex
        items-center
        justify-center
        bg-gray-50
        p-4
      "
      role="dialog"
      aria-modal="true"
    >
      <div
        className="
          w-[210mm]
          h-[297mm]
          bg-white
          shadow-2xl
          p-6
          break-inside-avoid
          relative
        "
      >
        {/* ← Back to Dashboard button (top‑left) */}
        <button
          onClick={onBack}
          className="
            absolute
            top-2
            left-2
            flex
            items-center
            gap-1
            text-gray-600
            hover:text-gray-800
            focus:outline-none
          "
          aria-label="Back to dashboard"
        >
          ← Back to Dashboard
        </button>

        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              PackSure
            </h1>
            <p className="text-sm text-gray-600">
              Audit ID: <span className="font-medium">{auditId}</span> &nbsp;|&nbsp;
              Date: <span className="font-medium">{today}</span>
            </p>
          </div>
          {/* Print / Download PDF button (top‑right) */}
          <button
            onClick={() => window.print()}
            className="
              px-4
              py-2
              bg-blue-600
              text-white
              rounded
              hover:bg-blue-700
              focus:outline-none
              focus:ring-2
              focus:ring-blue-500
              focus:ring-offset-2
              transition-colors
            "
          >
            Print / Download PDF
          </button>
        </div>

        {/* Divider */}
        <hr className="border-t border-gray-300 mb-6" />

        {/* Overall Status & Risk Score */}
        <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
          <div>
            <p className="font-medium text-gray-700">Overall Status:</p>
            <p className="text-gray-900">{overallStatus}</p>
          </div>
          <div>
            <p className="font-medium text-gray-700">Overall Risk Score:</p>
            <p className="text-gray-900">{riskScore}</p>
          </div>
        </div>

        {/* Section 1: Extracted Data Verification */}
        <section className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Section 1: Extracted Data Verification
          </h2>
          <div className="overflow-x-auto">
            <table className="
              min-w-full
              border-collapse
              border
              border-gray-300
              text-sm
              leading-tight
            ">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left font-medium text-gray-700 border-b border-gray-300">
                    Parameter
                  </th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700 border-b border-gray-300">
                    Detected
                  </th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700 border-b border-gray-300">
                    Expected
                  </th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700 border-b border-gray-300">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-300">
                {extractedRows.map((row, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="px-4 py-2 text-left font-medium text-gray-800">
                      {row.parameter}
                    </td>
                    <td className="px-4 py-2 text-left text-gray-700">{row.detected}</td>
                    <td className="px-4 py-2 text-left text-gray-700">{row.expected}</td>
                    <td className="px-4 py-2 text-left">
                      {row.status === "Pass" ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Pass
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                          Flagged
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Section 2: Compliance Violations Detected */}
        <section className="bg-red-50 border-l-4 border-red-500 p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Section 2: Compliance Violations Detected
          </h2>
          <p className="mb-2 text-gray-700">
            <span className="font-medium">Regulatory Framework:</span>
            {violation.framework}
          </p>
          <p className="mb-2 text-gray-700">
            <span className="font-medium">Rule Triggered:</span>
            {violation.rule}
          </p>
          <p className="mb-2 text-gray-700">
            <span className="font-medium">Violation Description:</span>
            {violation.description}
          </p>
          <p className="text-gray-700">
            <span className="font-medium">Recommended Action:</span>
            {violation.action}
          </p>
        </section>

        {/* Footer note (optional) */}
        <p className="mt-8 text-xs text-gray-500 text-center">
          This report is generated by PackSure – a Smart India Hackathon prototype.
        </p>
      </div>
    </div>
  );
}