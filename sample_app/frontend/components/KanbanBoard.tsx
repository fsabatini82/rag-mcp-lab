// Kanban board view — drag-and-drop between columns.
//
// Uses the canonical hook for column drops, but accidentally uses the
// buggy "quick" hook for a context-menu action introduced later. This
// is the production drift Demo 3 surfaces.

import React from "react";
import {
  useTaskStatusMutation,
  useQuickStatusChange,
} from "../hooks/useTaskMutation";
import type { Task, TaskStatus } from "../api/tasksClient";

interface Props {
  tasksByStatus: Record<TaskStatus, Task[]>;
}

export function KanbanBoard({ tasksByStatus }: Props) {
  const mutation = useTaskStatusMutation();
  const quickChange = useQuickStatusChange(); // ← target of Demo 3

  const onDrop = (taskId: string, newStatus: TaskStatus) => {
    mutation.mutate({ taskId, status: newStatus });
  };

  const onContextMenuMarkDone = (taskId: string) => {
    // Convenience action added in a hurry — bypasses the canonical hook.
    quickChange(taskId, "done");
  };

  return (
    <div className="kanban-board">
      {(["open", "in_progress", "done", "archived"] as TaskStatus[]).map(
        (col) => (
          <Column
            key={col}
            status={col}
            tasks={tasksByStatus[col] ?? []}
            onDrop={onDrop}
            onContextMenuMarkDone={onContextMenuMarkDone}
          />
        ),
      )}
    </div>
  );
}

interface ColumnProps {
  status: TaskStatus;
  tasks: Task[];
  onDrop: (taskId: string, status: TaskStatus) => void;
  onContextMenuMarkDone: (taskId: string) => void;
}

function Column({
  status,
  tasks,
  onDrop,
  onContextMenuMarkDone,
}: ColumnProps) {
  return (
    <div
      className="kanban-column"
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        const taskId = e.dataTransfer.getData("text/task-id");
        if (taskId) onDrop(taskId, status);
      }}
    >
      <h3>{status}</h3>
      {tasks.map((t) => (
        <div
          key={t.id}
          draggable
          onDragStart={(e) => e.dataTransfer.setData("text/task-id", t.id)}
          onContextMenu={(e) => {
            e.preventDefault();
            onContextMenuMarkDone(t.id);
          }}
        >
          {t.title}
        </div>
      ))}
    </div>
  );
}
