export interface Incident {
  id: number;
  erp_reference: string;
  incident_type: string;
  status: string;
  description: string;
  created_at: string;
  replay_summary?: string;
  replay_details?: string;
  replay_conclusion?: string;
  replayed_at?: string;
}

export interface IncidentCreate {
  erp_reference: string;
  incident_type: string;
  description: string;
}
