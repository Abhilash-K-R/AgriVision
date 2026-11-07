export type DiseaseClass = "healthy" | "early_blight" | "late_blight";

export interface DiagnosisResponse {
  prediction_id: string;
  disease_class: DiseaseClass | null;
  confidence: number | null;
  rejected: boolean;
  rejection_reason?: string | null;
  care_advice?: string | null;
  timestamp: string;
}

export interface PredictionHistoryItem {
  prediction_id: string;
  disease_class?: string | null;
  confidence?: number | null;
  rejected: boolean;
  timestamp: string;
  feedback_given?: boolean | null;
}

export interface PredictionHistoryResponse {
  predictions: PredictionHistoryItem[];
  total_count: number;
  page: number;
  page_size: number;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  database_connected: boolean;
  timestamp: string;
}

export interface FeedbackRequest {
  prediction_id: string;
  is_correct: boolean;
  notes?: string | null;
}

export interface AppError {
  message: string;
  code?: string;
  details?: unknown;
}
