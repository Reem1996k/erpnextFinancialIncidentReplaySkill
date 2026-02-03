/**
 * API service for incidents
 * Handles all communication with the backend
 */

import { Incident, IncidentsResponse, ReplayResponse, ApiError } from "@/lib/types";

const API_BASE_URL = "http://localhost:8000";

/**
 * Handle API error responses
 */
function handleApiError(response: Response, data: unknown): never {
  const error = data as ApiError;
  const message = error?.detail || error?.message || `API error: ${response.status}`;
  throw new Error(message);
}

/**
 * Get all incidents
 */
export async function fetchIncidents(): Promise<IncidentsResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/incidents`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const data = await response.json();
      handleApiError(response, data);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching incidents:", error);
    throw error;
  }
}

/**
 * Get a specific incident by ID
 */
export async function fetchIncidentById(id: number): Promise<Incident> {
  try {
    const response = await fetch(`${API_BASE_URL}/incidents/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const data = await response.json();
      handleApiError(response, data);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching incident ${id}:`, error);
    throw error;
  }
}

/**
 * Run replay analysis for an incident
 */
export async function runReplayAnalysis(id: number): Promise<ReplayResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/incidents/${id}/replay`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const data = await response.json();
      handleApiError(response, data);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error running replay for incident ${id}:`, error);
    throw error;
  }
}
