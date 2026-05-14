// lib/auth-server.ts
import { cookies } from "next/headers";
import { jwtVerify } from "jose";

const SECRET = new TextEncoder().encode("your-secret");

export async function getUserFromServer() {
    const token = (await cookies()).get("token")?.value;
    if (!token) return null;

    try {
        const { payload } = await jwtVerify(token, SECRET);
        return payload;
    } catch {
        return null;
    }
}

export async function isUserAuthenticated() {
    const token = (await cookies()).get("token")?.value;
    if (!token) return null;

    try {
        await jwtVerify(token, SECRET);
        return true;
    } catch {
        return false;
    }
}

export async function getUserTokenFromServer() {
    const token = (await cookies()).get("token")?.value;
    if (!token) return null;
    return token;
}
