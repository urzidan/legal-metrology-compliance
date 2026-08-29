import { useState } from "react";
import { Gavel, ChevronDown } from "lucide-react";

/**
 * ViolationsList
 * Collapsible card listing Legal Metrology (Packaged Commodities) Rules
 * 2011 clause violations detected in the current inspection.
 *
 * @param {object} props
 * @param {Array<{rule:string, description:string}>} props.violations
 */
export default function ViolationsList({ violations = [] }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-4">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex justify-between items-center cursor-pointer"
      >
        <h3 className="text-xl font-semibold text-on-surface flex items-center gap-2">
          <Gavel className="text-error" size={20} /> Legal Metrology Rules 2011 Violations
        </h3>
        <ChevronDown
          className={`text-on-surface-variant transition-transform ${open ? "rotate-180" : ""}`}
          size={20}
        />
      </button>

      {open && (
        <div className="mt-4 flex flex-col gap-2">
          {violations.length === 0 ? (
            <p className="text-sm text-on-surface-variant">No violations detected.</p>
          ) : (
            violations.map((v) => (
              <div
                key={v.rule}
                className="border border-error-container bg-error-container/20 rounded p-2 flex gap-2"
              >
                <div className="w-1 bg-error rounded shrink-0" />
                <div>
                  <p className="text-xs text-error font-bold">{v.rule}</p>
                  <p className="text-sm text-on-surface">{v.description}</p>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
