import { Configuration } from "../configuration";

const headers: HeadersInit = {
    "Accept": "application/json",
    "Content-Type": "application/json",
};

export class Intercom {

    private static url: string = Configuration.API_URL;

    static async get<T = unknown>(endpoint: string, options?: RequestInit): Promise<T> {
        const response = await fetch(`${this.url}${endpoint}`, {
            method: "GET",
            headers: { ...headers, ...options?.headers },
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json() as Promise<T>;
    }

    static async post<T = unknown>(endpoint: string, body?: unknown, options?: RequestInit): Promise<T> {
        const response = await fetch(`${this.url}${endpoint}`, {
            method: "POST",
            headers: { ...headers, ...options?.headers },
            body: body ? JSON.stringify(body) : undefined,
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json() as Promise<T>;
    }

    static async upload<T = unknown>(endpoint: string, file: File, fieldName = "file", extraData?: Record<string, string>, options?: RequestInit): Promise<T> {
        const formData = new FormData();
        formData.append(fieldName, file);

        if (extraData) {
            Object.entries(extraData).forEach(([key, value]) => formData.append(key, value));
        }

        const response = await fetch(`${this.url}${endpoint}`, {
            method: "POST",
            body: formData,
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json() as Promise<T>;
    }

}