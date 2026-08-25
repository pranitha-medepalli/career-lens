import React from "react";
import { useRef, useState } from "react";

function FileUpload({ onAnalyze, loading }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);

  const selectFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (
      !allowedTypes.includes(selectedFile.type) &&
      !selectedFile.name.toLowerCase().endsWith(".pdf") &&
      !selectedFile.name.toLowerCase().endsWith(".docx")
    ) {
      alert("Please upload a PDF or DOCX file.");
      return;
    }

    setFile(selectedFile);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);

    const droppedFile =
      event.dataTransfer.files[0];

    selectFile(droppedFile);
  };

  const handleFileInput = (event) => {
    const selectedFile =
      event.target.files[0];

    selectFile(selectedFile);
  };

  const handleAnalyze = () => {
    if (!file) {
      alert("Please select your resume first.");
      return;
    }

    onAnalyze(file);
  };

  return (
    <div className="upload-section">
      <div
        className={`drop-zone ${
          dragging ? "dragging" : ""
        }`}
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => {
          setDragging(false);
        }}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileInput}
          hidden
        />

        <div className="upload-icon">
          ↑
        </div>

        <h3>
          Drop your resume here
        </h3>

        <p>
          or click to browse
        </p>

        <span>
          PDF or DOCX
        </span>
      </div>

      {file && (
        <div className="selected-file">
          <div>
            <strong>{file.name}</strong>
            <p>
              {(file.size / 1024).toFixed(1)} KB
            </p>
          </div>

          <button
            className="remove-button"
            onClick={() => setFile(null)}
          >
            ×
          </button>
        </div>
      )}

      <button
        className="primary-button"
        onClick={handleAnalyze}
        disabled={!file || loading}
      >
        {loading
          ? "Analyzing Resume..."
          : "Analyze Resume"}
      </button>
    </div>
  );
}

export default FileUpload;