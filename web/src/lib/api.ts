async function throwApiError(res: Response, fallback: string): Promise<never> {
  const raw = await res.text();
  const parsed = raw ? safeParseJson(raw) : null;
  const message = parsed?.error?.message ?? parsed?.detail ?? parsed?.message ?? raw ?? fallback;
  throw new Error(message || fallback);
}

function safeParseJson(raw: string): any {
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export interface SymptomEntry {
  symptom: string;
  severity: number;
  date: string;
}

export interface AnalyzeResponse {
  analysis: {
    condition: string;
    confidence: number;
    recommendation: string;
  }[];
}

export async function analyzeSymptoms(petId: string, symptoms: SymptomEntry[]): Promise<AnalyzeResponse> {
  const res = await fetch(`/api/ai/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pet_id: petId, symptoms })
  });
  if (!res.ok) {
    await throwApiError(res, "Failed to analyze symptoms");
  }
  return res.json();
}

export async function getPet(petId: string) {
  const res = await fetch(`/api/pets/${petId}`);
  if (!res.ok) {
    await throwApiError(res, "Failed to fetch pet profile");
  }
  return res.json();
}
