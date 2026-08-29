import { useRef } from "react";
import { Upload, Camera, ZoomIn, Crop, SunDim, Cpu, Loader2, Trash2 } from "lucide-react";

/**
 * InspectionCanvas
 * Left-hand panel: shows the uploaded product image with AI-detected
 * bounding boxes for each compliance field, plus upload/sync/enhance controls.
 *
 * @param {object} props
 * @param {string|null} props.imageUrl
 * @param {Array<{id:string,label:string,x:number,y:number,width:number,height:number,status:'pass'|'flagged'}>} props.boundingBoxes
 * @param {number|null} props.aiConfidence   - 0-100
 * @param {boolean} props.loading
 * @param {(file: File) => void} props.onUpload
 * @param {() => void} props.onClear
 * @param {() => void} props.onSync
 * @param {(op: 'zoom'|'crop'|'deglare') => void} props.onEnhance
 */
export default function InspectionCanvas({
  imageUrl = null,
  boundingBoxes = [],
  aiConfidence = null,
  loading = false,
  onUpload,
  onClear,
  onSync,
  onEnhance,
}) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file && onUpload) onUpload(file);
  };

  const handleRemove = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    if (onClear) onClear();
  };

  return (
    <section className="md:col-span-5 flex flex-col gap-4">
      <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-4 flex justify-between items-center">
        <h2 className="text-xl font-semibold text-on-surface">Inspection Canvas</h2>
        <div className="flex gap-2 items-center">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileChange}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="bg-surface-container-low text-primary px-3 py-1.5 rounded text-sm font-medium border border-outline-variant hover:bg-surface-container transition-colors flex items-center gap-1"
          >
            <Upload size={16} /> Upload
          </button>
          <button
            onClick={onSync}
            className="bg-surface-container-low text-primary px-3 py-1.5 rounded text-sm font-medium border border-outline-variant hover:bg-surface-container transition-colors flex items-center gap-1"
          >
            <Camera size={16} /> Sync
          </button>
          {imageUrl && (
            <button
              onClick={handleRemove}
              className="bg-error-container text-on-error-container px-3 py-1.5 rounded text-sm font-medium border border-error/30 hover:bg-error/20 transition-colors flex items-center gap-1"
              title="Remove image and reset inspection"
            >
              <Trash2 size={16} /> Remove
            </button>
          )}
        </div>
      </div>

      <div className="relative bg-surface-container-low border border-outline-variant rounded-lg overflow-hidden flex-1 min-h-[500px]">
        {loading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-surface/70">
            <Loader2 className="animate-spin text-primary" size={32} />
          </div>
        )}

        {imageUrl ? (
          <img
            src={imageUrl}
            alt="Product under inspection"
            className="absolute inset-0 w-full h-full object-cover opacity-90"
          />
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 text-on-surface-variant">
            <Upload size={32} />
            <p className="text-sm">Upload a product image to begin inspection</p>
          </div>
        )}

        {boundingBoxes.map((box) => (
          <div
            key={box.id}
            className={`absolute flex items-start justify-end p-1 border-2 ${
              box.status === "flagged"
                ? "border-error bg-error/10"
                : "border-secondary bg-secondary/10"
            }`}
            style={{
              top: `${box.y}%`,
              left: `${box.x}%`,
              width: `${box.width}px`,
              height: `${box.height}px`,
            }}
          >
            <span
              className={`text-xs px-1 rounded font-medium ${
                box.status === "flagged"
                  ? "bg-error text-on-error"
                  : "bg-secondary text-on-secondary"
              }`}
            >
              {box.label}
            </span>
          </div>
        ))}

        {aiConfidence !== null && (
          <div className="absolute bottom-4 left-4">
            <span className="bg-secondary-container text-on-secondary-container text-xs font-semibold px-3 py-1.5 rounded shadow-sm flex items-center gap-2">
              <Cpu size={14} /> AI Confidence: {aiConfidence.toFixed(1)}%
            </span>
          </div>
        )}

        <div className="absolute bottom-4 right-4 flex bg-surface-container-lowest border border-outline-variant rounded shadow-sm">
          <button
            onClick={() => onEnhance?.("zoom")}
            className="p-2 text-on-surface-variant hover:bg-surface-container-low transition-colors"
            title="Zoom"
          >
            <ZoomIn size={18} />
          </button>
          <div className="w-px bg-outline-variant my-1" />
          <button
            onClick={() => onEnhance?.("crop")}
            className="p-2 text-on-surface-variant hover:bg-surface-container-low transition-colors"
            title="Crop"
          >
            <Crop size={18} />
          </button>
          <div className="w-px bg-outline-variant my-1" />
          <button
            onClick={() => onEnhance?.("deglare")}
            className="p-2 text-on-surface-variant hover:bg-surface-container-low transition-colors"
            title="De-glare"
          >
            <SunDim size={18} />
          </button>
        </div>
      </div>
    </section>
  );
}