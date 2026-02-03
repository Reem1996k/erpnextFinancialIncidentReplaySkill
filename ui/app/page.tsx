'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createIncident } from '../lib/api';

export default function CreateIncidentPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    erp_reference: '',
    incident_type: 'invoice_discrepancy',
    description: '',
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.erp_reference.trim()) {
      setError('ERP Reference is required');
      return;
    }

    if (!formData.description.trim()) {
      setError('Description is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const incident = await createIncident(formData);
      router.push(`/incidents/${incident.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create incident');
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <div className="form-card">
        {/* Title */}
        <h1 className="page-title">
          Create Financial Incident
        </h1>

        {/* Subtitle */}
        <p className="page-subtitle">
          Analyze invoice discrepancies with AI-powered insights
        </p>

        {/* Error Message */}
        {error && (
          <div className="error-box">
            <p className="error-text">{error}</p>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit}>
          {/* ERP Reference */}
          <div className="form-group">
            <label className="form-label">ERP Reference</label>
            <input
              type="text"
              id="erp_reference"
              name="erp_reference"
              value={formData.erp_reference}
              onChange={handleInputChange}
              placeholder="e.g., INV-2024-001234"
              disabled={loading}
              className="form-input"
              required
            />
          </div>

          {/* Incident Type */}
          <div className="form-group">
            <label className="form-label">Incident Type</label>
            <select
              id="incident_type"
              name="incident_type"
              value={formData.incident_type}
              onChange={handleInputChange}
              disabled={loading}
              className="form-input"
            >
              <option value="invoice_discrepancy">Invoice Discrepancy</option>
              <option value="payment_mismatch">Payment Mismatch</option>
              <option value="tax_calculation_error">Tax Calculation Error</option>
              <option value="journal_entry_issue">Journal Entry Issue</option>
            </select>
          </div>

          {/* Description */}
          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Describe the issue in detail. Include amounts, dates, and any relevant transaction information..."
              disabled={loading}
              className="form-textarea"
              required
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="form-button"
          >
            {loading ? 'Analyzing...' : 'Create & Analyze'}
          </button>
        </form>
      </div>

      <style jsx>{`
        .page-wrapper {
          background-color: #f1f5f9;
          min-height: 100vh;
          padding: 40px 20px;
        }

        .form-card {
          max-width: 900px;
          margin: 40px auto;
          padding: 32px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }

        .page-title {
          font-size: 32px;
          font-weight: 700;
          color: #111827;
          text-align: center;
          margin-bottom: 6px;
        }

        .page-subtitle {
          font-size: 14px;
          color: #64748b;
          text-align: center;
          margin-top: 0;
          margin-bottom: 32px;
          font-weight: 400;
        }

        .error-box {
          margin-bottom: 24px;
          padding: 16px;
          background-color: #fee2e2;
          border: 1px solid #fca5a5;
          border-radius: 8px;
        }

        .error-text {
          font-size: 14px;
          color: #991b1b;
          margin: 0;
        }

        .form-group {
          margin-bottom: 28px;
        }

        .form-label {
          display: block;
          font-size: 14px;
          font-weight: 600;
          color: #111827;
          margin-bottom: 8px;
        }

        .form-input,
        .form-textarea {
          width: 100%;
          padding: 12px 16px;
          border: 1px solid #d1d5db;
          border-radius: 8px;
          font-size: 14px;
          color: #111827;
          background: white;
          transition: all 0.2s;
          font-family: inherit;
        }

        .form-input::placeholder,
        .form-textarea::placeholder {
          color: #9ca3af;
        }

        .form-input:focus,
        .form-textarea:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .form-input:hover,
        .form-textarea:hover {
          border-color: #9ca3af;
        }

        .form-textarea {
          min-height: 140px;
          resize: vertical;
        }

        .form-button {
          width: 100%;
          padding: 12px 24px;
          margin-top: 40px;
          background-color: #2563eb;
          color: white;
          font-size: 14px;
          font-weight: 600;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .form-button:hover:not(:disabled) {
          background-color: #1d4ed8;
        }

        .form-button:disabled {
          background-color: #9ca3af;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}
