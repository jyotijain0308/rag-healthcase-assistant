"use server";
import { cookies } from "next/headers";

export async function login(email: string, password: string) {
    const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
        throw new Error("Login failed");
    }

    const data = await res.json();

    const cookieStore = await cookies();
    cookieStore.set("token", data.access_token, {
        httpOnly: true,
        path: "/",
        secure: true,
    });

    return data; // should return { access_token }
}