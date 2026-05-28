/**
 * API Client for Teach Authoring API
 *
 * Reusable HTTP client module for Deno scripts.
 *
 * Environment:
 *   TEACH_API_URL - Base URL for the API (default: http://localhost:4100/api)
 */

// === CONFIGURATION ===

export const API_BASE =
  Deno.env.get("TEACH_API_URL") || "http://localhost:4100/api";

// === TYPES ===

export interface Course {
  id: string;
  title: string;
  description: string;
  version: string;
  status: "draft" | "published" | "archived";
  createdAt: string;
  updatedAt: string;
}

export interface Unit {
  id: string;
  courseId: string;
  title: string;
  description: string;
  order: number;
  createdAt: string;
  updatedAt: string;
}

export interface Lesson {
  id: string;
  unitId: string;
  title: string;
  description: string;
  order: number;
  content: {
    type: "markdown" | "html";
    body: string;
  };
  audienceLayer: "general" | "practitioner" | "specialist" | null;
  createdAt: string;
  updatedAt: string;
}

export interface CompetencyCluster {
  id: string;
  courseId: string;
  name: string;
  description: string;
  order: number;
  createdAt: string;
  updatedAt: string;
}

export interface Competency {
  id: string;
  clusterId: string;
  name: string;
  description: string;
  order: number;
  createdAt: string;
  updatedAt: string;
}

export interface ApiError {
  error: string;
  message?: string;
}

// === HTTP METHODS ===

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorBody = await response.text();
    let errorMessage: string;
    try {
      const errorJson = JSON.parse(errorBody) as ApiError;
      errorMessage = errorJson.message || errorJson.error || errorBody;
    } catch {
      errorMessage = errorBody;
    }
    throw new Error(`API Error ${response.status}: ${errorMessage}`);
  }
  return response.json() as Promise<T>;
}

export async function apiGet<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return handleResponse<T>(response);
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return handleResponse<T>(response);
}

export async function apiPut<T>(path: string, body: unknown): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return handleResponse<T>(response);
}

export async function apiDelete(path: string): Promise<void> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API Error ${response.status}: ${errorBody}`);
  }
}

// === COURSE API ===

export async function listCourses(): Promise<Course[]> {
  return apiGet<Course[]>("/courses");
}

export async function getCourse(id: string): Promise<Course> {
  return apiGet<Course>(`/courses/${id}`);
}

export async function createCourse(data: {
  title: string;
  description?: string;
  version?: string;
}): Promise<Course> {
  return apiPost<Course>("/courses", {
    title: data.title,
    description: data.description || "",
    version: data.version || "1.0.0",
  });
}

export async function updateCourse(
  id: string,
  data: Partial<{
    title: string;
    description: string;
    version: string;
    status: "draft" | "published" | "archived";
  }>
): Promise<Course> {
  return apiPut<Course>(`/courses/${id}`, data);
}

export async function deleteCourse(id: string): Promise<void> {
  return apiDelete(`/courses/${id}`);
}

// === UNIT API ===

export async function listUnits(courseId: string): Promise<Unit[]> {
  return apiGet<Unit[]>(`/courses/${courseId}/units`);
}

export async function getUnit(id: string): Promise<Unit> {
  return apiGet<Unit>(`/units/${id}`);
}

export async function createUnit(
  courseId: string,
  data: {
    title: string;
    description?: string;
    order?: number;
  }
): Promise<Unit> {
  return apiPost<Unit>(`/courses/${courseId}/units`, {
    title: data.title,
    description: data.description || "",
    order: data.order,
  });
}

export async function updateUnit(
  id: string,
  data: Partial<{
    title: string;
    description: string;
    order: number;
  }>
): Promise<Unit> {
  return apiPut<Unit>(`/units/${id}`, data);
}

export async function deleteUnit(id: string): Promise<void> {
  return apiDelete(`/units/${id}`);
}

// === LESSON API ===

export async function listLessons(unitId: string): Promise<Lesson[]> {
  return apiGet<Lesson[]>(`/units/${unitId}/lessons`);
}

export async function getLesson(id: string): Promise<Lesson> {
  return apiGet<Lesson>(`/lessons/${id}`);
}

export async function createLesson(
  unitId: string,
  data: {
    title: string;
    description?: string;
    order?: number;
    content?: { type: "markdown" | "html"; body: string };
    audienceLayer?: "general" | "practitioner" | "specialist" | null;
  }
): Promise<Lesson> {
  return apiPost<Lesson>(`/units/${unitId}/lessons`, {
    title: data.title,
    description: data.description || "",
    order: data.order,
    contentType: data.content?.type || "markdown",
    contentBody: data.content?.body || "",
    audienceLayer: data.audienceLayer || null,
  });
}

export async function updateLesson(
  id: string,
  data: Partial<{
    title: string;
    description: string;
    order: number;
    content: { type: "markdown" | "html"; body: string };
    audienceLayer: "general" | "practitioner" | "specialist" | null;
  }>
): Promise<Lesson> {
  // Transform content object to flat fields for API
  const apiData: Record<string, unknown> = { ...data };
  if (data.content) {
    apiData.contentType = data.content.type;
    apiData.contentBody = data.content.body;
    delete apiData.content;
  }
  return apiPut<Lesson>(`/lessons/${id}`, apiData);
}

export async function deleteLesson(id: string): Promise<void> {
  return apiDelete(`/lessons/${id}`);
}

// === COMPETENCY CLUSTER API ===

export async function listCompetencyClusters(
  courseId: string
): Promise<CompetencyCluster[]> {
  return apiGet<CompetencyCluster[]>(`/courses/${courseId}/competency-clusters`);
}

export async function getCompetencyCluster(
  id: string
): Promise<CompetencyCluster> {
  return apiGet<CompetencyCluster>(`/competency-clusters/${id}`);
}

export async function createCompetencyCluster(
  courseId: string,
  data: {
    name: string;
    description?: string;
    order?: number;
  }
): Promise<CompetencyCluster> {
  return apiPost<CompetencyCluster>(`/courses/${courseId}/competency-clusters`, {
    name: data.name,
    description: data.description || "",
    order: data.order,
  });
}

// === COMPETENCY API ===

export async function listCompetencies(
  clusterId: string
): Promise<Competency[]> {
  return apiGet<Competency[]>(`/competency-clusters/${clusterId}/competencies`);
}

export async function getCompetency(id: string): Promise<Competency> {
  return apiGet<Competency>(`/competencies/${id}`);
}

export async function createCompetency(
  clusterId: string,
  data: {
    name: string;
    description?: string;
    order?: number;
  }
): Promise<Competency> {
  return apiPost<Competency>(`/competency-clusters/${clusterId}/competencies`, {
    name: data.name,
    description: data.description || "",
    order: data.order,
  });
}

// === UTILITIES ===

export function parseArgs(args: string[]): Map<string, string | boolean> {
  const result = new Map<string, string | boolean>();
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const nextArg = args[i + 1];
      if (nextArg && !nextArg.startsWith("--")) {
        result.set(key, nextArg);
        i++;
      } else {
        result.set(key, true);
      }
    } else if (!args[i - 1]?.startsWith("--")) {
      // Positional argument
      if (!result.has("_positional")) {
        result.set("_positional", arg);
      }
    }
  }
  return result;
}

export function showHelp(name: string, usage: string, options: string): void {
  console.log(`${name}

${usage}

Options:
${options}
  --json       Output as JSON
  --help, -h   Show this help message
`);
}
