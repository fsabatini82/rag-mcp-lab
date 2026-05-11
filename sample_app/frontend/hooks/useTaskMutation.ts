// Hook used by the Kanban board to move tasks between columns.
//
// NOTE FOR THE LAB: this file contains a deliberately buggy mutation
// (the `useQuickStatusChange` hook below) that mirrors BUG-503. Demo 3
// shows how Mnemo helps GHCP recognize the pattern and propose the fix.

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { patchTaskStatus, type TaskStatus } from "../api/tasksClient";

/**
 * Canonical hook — follows ADR-004 ("no fire-and-forget mutations").
 * After BUG-503 every kanban interaction must go through this.
 */
export function useTaskStatusMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ taskId, status }: { taskId: string; status: TaskStatus }) =>
      patchTaskStatus(taskId, status),
    onError: (_err, variables, _ctx) => {
      // Revert optimistic UI: tell the board to put the card back.
      window.dispatchEvent(
        new CustomEvent("kanban:revert", { detail: variables }),
      );
      // Toast with retry button is mounted in <Toast/> root.
      window.dispatchEvent(
        new CustomEvent("toast:error", {
          detail: { message: "Aggiornamento fallito", retry: variables },
        }),
      );
    },
    onSettled: () => qc.invalidateQueries({ queryKey: ["tasks"] }),
  });
}

/**
 * "Quick" hook added later by a different developer for a contextual
 * menu action. It bypasses the canonical hook and re-introduces the
 * fire-and-forget anti-pattern that BUG-503 fixed.
 *
 * Demo 3: GHCP discovers BUG-503 via Mnemo, locates *this* hook, and
 * proposes refactoring it to delegate to useTaskStatusMutation.
 */
export function useQuickStatusChange() {
  return (taskId: string, status: TaskStatus): void => {
    // FIXME: fire-and-forget — no await, no .catch, no UI feedback on error.
    // This is exactly the pattern that caused BUG-503.
    void patchTaskStatus(taskId, status);
  };
}
