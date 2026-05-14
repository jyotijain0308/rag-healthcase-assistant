import { cookies } from "next/headers";
import { jwtVerify } from "jose";

const SECRET = new TextEncoder().encode(process.env.JWT_SECRET);

export async function GET() {
    const token = (await cookies()).get("token")?.value;

    if (!token) {
        return Response.json(null, { status: 401 });
    }

    try {
        const { payload } = await jwtVerify(token, SECRET);
        console.log("payload", payload);
        return Response.json(payload);
    } catch (error) {
        console.log("error", error);
        return Response.json(null, { status: 401 });
    }
}