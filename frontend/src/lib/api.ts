import { getUserTokenFromServer } from "./auth-server";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
    const token = await getUserTokenFromServer();

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            Authorization: token ? `Bearer ${token}` : "",
            ...(options.headers || {}),
        },
    });

    // Handle expired/invalid token
    if (response.status === 401) {
        try {
            const data = await response.json();

            console.log("JWT ERROR:", data);

            // FastAPI can return detail or code
            const isExpired =
                data?.code === "ERR_JWT_EXPIRED" ||
                data?.detail?.includes?.("expired");

            if (isExpired) {
                await fetch("/api/logout", { method: "POST" });
                return;
            }
        } catch (e) {
            await fetch("/api/logout", { method: "POST" });
            return;
        }
    }

    return response;
}