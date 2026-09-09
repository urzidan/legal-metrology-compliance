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
 * Rows of extracted data with status.
 * @param {object} props
 * @param {Array} props.fields - Array of {parameter, detectedValue, expectedValue, status}
 */
export default function ComplianceTable({ fields = [] }) {
  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-lg overflow-hidden">
      <div className="bg-surface-container-low px-4 py-2 border-b border-outline-variant">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
          EXTRACTED DATA VERIFICATION
        </h3>
      </div>
      <table className="w-full text-left text-sm">
        <thead className="bg-surface-dim/30">
          <tr>
            <th className="p-4 font-semibold text-on-surface">PARAMETER</th>
            <th className="p-4 font-semibold text-on-surface">DETECTED VALUE</th>
            <th className="p-4 font-semibold text-on-surface">STANDARD / EXPECTED</th>
            <th className="p-4 font-semibold text-on-surface">STATUS</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant/50">
          {fields.length === 0 && (
            <tr>
              <td colSpan={4} className="p-4 text-center text-on-surface-variant">
                No data extracted yet — upload an image to begin.
              </td>
            </tr>
          )}
          {fields.map((row) => (
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