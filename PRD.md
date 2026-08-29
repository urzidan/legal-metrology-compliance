# Project Requirements Document (PRD)

## 1. Project Title

Software System to Check Compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by Scanning Products, Images and Labels.

---

## 2. Problem Statement

Develop an AI-assisted software system that can analyze packaged commodity images and labels and assist in checking whether the required declarations are present and properly represented according to the applicable Legal Metrology (Packaged Commodities) Rules, 2011 and subsequent applicable amendments/notifications.

---

## 3. Objective

The system should:

1. Accept images of packaged commodities.
2. Detect relevant regions of the package.
3. Extract text using OCR.
4. Identify important declarations and product information.
5. Determine which requirements are applicable.
6. Validate extracted information against structured compliance rules.
7. Identify missing, incorrect, or uncertain declarations.
8. Generate an understandable compliance report.
9. Provide visual evidence wherever possible.

---

## 4. Target Users

### Primary Users

- Legal Metrology inspection teams
- Government officers
- Compliance teams
- Manufacturers
- Packers
- Importers

### Secondary Users

- Retailers
- Consumers
- Researchers
- Educational institutions

---

## 5. Core System Flow

Product Image
↓
Image Validation
↓
Image Preprocessing
↓
YOLO Detection
↓
Relevant Region Cropping
↓
OCR
↓
Text Processing
↓
Field Extraction
↓
Product/Category Identification
↓
Applicable Rule Selection
↓
Compliance Validation
↓
Compliance Report

---

## 6. Core Features

### 6.1 Product Scanning

- Upload product images.
- Capture images using a camera.
- Support multiple images for different sides of a package.
- Validate image format and quality.

### 6.2 Computer Vision

The system should use computer vision to:

- Detect the package.
- Detect relevant declaration regions.
- Locate text/label regions.
- Crop relevant areas.
- Handle rotation where possible.
- Handle perspective distortion where possible.

### 6.3 OCR

Extract text from relevant package regions.

Potential information includes:

- MRP
- Net quantity
- Manufacturer
- Packer
- Importer
- Country of origin
- Consumer care information
- Date-related declarations
- Product/category information
- Other applicable declarations

### 6.4 Information Extraction

Convert OCR output into structured data.

Example:

```json
{
  "mrp": {
    "value": "₹120",
    "confidence": 0.94
  },
  "net_quantity": {
    "value": "500 g",
    "confidence": 0.91
  },
  "manufacturer": {
    "value": "ABC Foods Pvt Ltd",
    "confidence": 0.88
  }
}