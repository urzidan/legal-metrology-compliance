import { TriangleAlert, FileText, Flag, CheckCheck, Loader2 } from "lucide-react";

/**
 * StickyActionBar
 * Fixed footer with the human-in-the-loop status flag and the three
 * terminal actions for an inspection.
 *
 * @param {object} props
 * @param {boolean} props.reviewRequired
 * @param {boolean} [props.busy]           - disables buttons while a request is in flight
 * @param {() => void} props.onGenerateReport
 * @param {() => void} props.onEscalate
 * @param {() => void} props.onConfirmAndLog
 */
export default function StickyActionBar({
  reviewRequired = true,
  busy = false,
  onGenerateReport,
  onEscalate,
  onConfirmAndLog,
}) {
  return (
    <div className="fixed bottom-0 left-0 w-full z-40 flex justify-between items-center px-8 py-4 bg-inverse-surface backdrop-blur-md shadow-md">
      <div className="flex items-center gap-4">
        {reviewRequired && (
          <span className="bg-error-container text-on-error-container text-xs font-semibold px-3 py-1.5 rounded flex items-center gap-2 border border-error/20">
            <TriangleAlert size={16} /> Human-in-the-Loop Review Required
          </span>
        )}
      </div>
      <div className="flex gap-2">
        <button
          onClick={onGenerateReport}
          disabled={busy}
          className="bg-surface-container-lowest text-primary px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider border border-outline-variant hover:bg-surface-container-low transition-colors flex items-center gap-2 disabled:opacity-50"
        >
          <FileText size={16} /> Generate Report
        </button>
        <button
          onClick={onEscalate}
          disabled={busy}
          className="bg-error text-on-error px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider hover:opacity-90 transition-opacity flex items-center gap-2 disabled:opacity-50"
        >
          <Flag size={16} /> Escalate
        </button>
        <button
          onClick={onConfirmAndLog}
          disabled={busy}
          className="bg-primary text-on-primary px-6 py-2 rounded text-xs font-semibold uppercase tracking-wider hover:bg-primary-container hover:text-on-primary-container transition-colors flex items-center gap-2 disabled:opacity-50"
        >
          {busy ? <Loader2 size={16} className="animate-spin" /> : <CheckCheck size={16} />}
          Confirm &amp; Log
        </button>
      </div>
    </div>
  );
}
