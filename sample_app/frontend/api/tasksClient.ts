// Thin HTTP client for the Task API. Used by hooks/components.

export type TaskStatus = "open" | "in_progress" | "done" | "archived";

export interface Task {
  id: string;
  project_id: string;
  title: string;
  description: string;
  status: TaskStatus;
  assignee_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface ApiEnvelope<T> {
  data: T | null;
  error: { code: string; message: string } | null;
  meta: Record<string, unknown> | null;
}

const BASE = "/api/v1";

export async function patchTaskStatus(
  taskId: string,
  status: TaskStatus,
): Promise<Task> {
  const res = await fetch(`${BASE}/tasks/${taskId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    const body = (await res.json().catch(() => ({}))) as Partial<ApiEnvelope<Task>>;
    throw new Error(body.error?.message ?? `PATCH failed: ${res.status}`);
  }
  const env = (await res.json()) as ApiEnvelope<Task>;
  if (!env.data) throw new Error("PATCH succeeded but returned no data");
  return env.data;
}
