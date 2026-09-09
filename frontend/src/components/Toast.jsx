import React from "react";

/**
 * Toast – simple auto‑dismissable notification.
 * Props:
 *   message: string – text to show
 *   onClose: () => void – called when the toast should disappear
 */
export default function Toast({ message, onClose }) {
  return (
    <div
      className="
        fixed
        top-4
        left-1/2
        transform
        -translate-x-1/2
        flex
        items-center
        px-4
        py-2
        bg-green-600
        text-white
        rounded-md
        shadow-lg
        z-50
      "
      role="alert"
      onClick={onClose}
    >
      {/* Optional check‑mark – you can replace with an icon if you have one */}
      <span className="mr-2">✓</span>
      <span>{message}</span>
    </div>
  );
}