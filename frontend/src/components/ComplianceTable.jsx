import { CheckCircle2, AlertCircle, Clock } from "lucide-react";

const statusIcon = {
  pass: <CheckCircle2 size={16} />,
  flagged: <AlertCircle size={16} />,
  pending: <Clock size={16} />,
};

const statusStyle = {
  pass: "text-secondary",
  flagged: "text-error",
  pending: "text-on-surface-variant",
};

/**
 * ComplianceTable
 * Renders the OCR-extracted fields next to the Legal Metrology expected
 * values, with a pass/flagged/pending status per row.
 *
 * @param {object} props
 * @param {Array<{parameter:string, detectedValue:string, expectedValue:string, status:'pass'|'flagged'|'pending'}>} props.rows
 */
export default function ComplianceTable({ rows = [] }) {
  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-lg overflow-hidden">
      <div className="bg-surface-container-low px-4 py-2 border-b border-outline-variant">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
          Extracted Data Verification
        </h3>
      </div>
      <table className="w-full text-left text-sm">
        <thead className="bg-surface-dim/30">
          <tr>
            <th className="p-4 font-semibold text-on-surface">Parameter</th>
            <th className="p-4 font-semibold text-on-surface">Detected Value</th>
            <th className="p-4 font-semibold text-on-surface">Standard/Expected</th>
            <th className="p-4 font-semibold text-on-surface">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant/50">
          {rows.length === 0 && (
            <tr>
              <td colSpan={4} className="p-4 text-center text-on-surface-variant">
                No data extracted yet — upload an image to begin.
              </td>
            </tr>
          )}
          {rows.map((row) => (
            <tr
              key={row.parameter}
              className={`hover:bg-surface-container-lowest transition-colors ${
                row.status === "flagged" ? "bg-error-container/10" : ""
              }`}
            >
              <td className={`p-4 font-medium ${row.status === "flagged" ? "text-error" : ""}`}>
                {row.parameter}
              </td>
              <td className={`p-4 font-mono text-[13px] ${row.status === "flagged" ? "text-error" : ""}`}>
                {row.detectedValue}
              </td>
              <td className="p-4 text-on-surface-variant">{row.expectedValue}</td>
              <td className="p-4">
                <span className={`inline-flex items-center gap-1 ${statusStyle[row.status]}`}>
                  {statusIcon[row.status]}
                  {row.status === "pass" ? "Pass" : row.status === "flagged" ? "Flagged" : "Pending"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
