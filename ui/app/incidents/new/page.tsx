'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { IncidentCreate } from '@/app/types';

export default function CreateIncident() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<IncidentCreate>({
    erp_reference: '',
    incident_type: 'Pricing_Issue',
    description: '',
  });

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/incidents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || 'Failed to create incident'
        );
      }

      const data = await response.json();
      router.push(`/incidents/${data.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Create New Incident</h1>
      {error && <div className="message message-error">Error: {error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="erp_reference">ERP Reference *</label>
          <input
            type="text"
            id="erp_reference"
            name="erp_reference"
            value={formData.erp_reference}
            onChange={handleChange}
            required
            placeholder="e.g., ERR-001"
          />
        </div>

        <div className="form-group">
          <label htmlFor="incident_type">Incident Type *</label>
          <select
            id="incident_type"
            name="incident_type"
            value={formData.incident_type}
            onChange={handleChange}
            required
          >
            <option value="Pricing_Issue">Pricing Issue</option>
            <option value="Duplicate_Invoice">Duplicate Invoice</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            placeholder="Describe the incident..."
          ></textarea>
        </div>

        <button
          type="submit"
          className="btn-primary"
          disabled={loading}
        >
          {loading ? 'Creating...' : 'Create Incident'}
        </button>
      </form>
    </div>
  );
}
